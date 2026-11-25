"""Logika pokoi i rozgrywki – stan w pamięci RAM."""

from __future__ import annotations

import asyncio
import random
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from fastapi import WebSocket

from cards import CARDS, get_card_by_id, public_card

CARDS_PER_PLAYER = 15
CORRECT_POINTS = 100
STREAK_BONUS = 30
STREAK_THRESHOLD = 3
WRONG_PENALTY = 50
LOCKOUT_SECONDS = 2.0
FINISH_BONUSES = (300, 200, 100)  # 1., 2., 3. miejsce


@dataclass
class Player:
    player_id: str
    nick: str
    websocket: WebSocket | None = None
    score: int = 0
    streak: int = 0
    deck: list[dict] = field(default_factory=list)
    current_index: int = 0
    answered: int = 0
    finished: bool = False
    finish_place: int | None = None
    finish_seconds: float | None = None
    locked_until: float = 0.0
    connected: bool = True

    def progress_payload(self) -> dict[str, Any]:
        total = len(self.deck) or CARDS_PER_PLAYER
        return {
            "player_id": self.player_id,
            "nick": self.nick,
            "score": self.score,
            "streak": self.streak,
            "answered": self.answered,
            "total": total,
            "finished": self.finished,
            "finish_place": self.finish_place,
            "finish_seconds": self.finish_seconds,
            "locked": time.time() < self.locked_until,
            "connected": self.connected,
        }


@dataclass
class Room:
    pin: str
    host_ws: WebSocket | None
    players: dict[str, Player] = field(default_factory=dict)  # player_id -> Player
    nicks: set[str] = field(default_factory=set)
    state: str = "lobby"  # lobby | playing | finished
    finish_order: list[str] = field(default_factory=list)
    started_at: float | None = None

    def leaderboard(self) -> list[dict[str, Any]]:
        ordered = sorted(
            self.players.values(),
            key=lambda p: (
                -p.answered,
                -p.score,
                p.finish_place if p.finish_place is not None else 999,
                p.nick.lower(),
            ),
        )
        return [p.progress_payload() for p in ordered]


class GameManager:
    def __init__(self) -> None:
        self.rooms: dict[str, Room] = {}
        self._lock = asyncio.Lock()

    def _generate_pin(self) -> str:
        for _ in range(100):
            pin = f"{random.randint(0, 9999):04d}"
            if pin not in self.rooms:
                return pin
        raise RuntimeError("Nie udało się wygenerować unikalnego PIN-u")

    async def create_room(self, host_ws: WebSocket) -> Room:
        async with self._lock:
            pin = self._generate_pin()
            room = Room(pin=pin, host_ws=host_ws)
            self.rooms[pin] = room
            return room

    def get_room(self, pin: str) -> Room | None:
        return self.rooms.get(pin)

    async def remove_room(self, pin: str) -> None:
        async with self._lock:
            self.rooms.pop(pin, None)

    async def attach_host(self, pin: str, host_ws: WebSocket) -> Room | None:
        room = self.rooms.get(pin)
        if not room:
            return None
        room.host_ws = host_ws
        return room

    def find_player_by_nick(self, room: Room, nick: str) -> Player | None:
        nick_l = nick.lower()
        for player in room.players.values():
            if player.nick.lower() == nick_l:
                return player
        return None

    async def join_player(
        self,
        pin: str,
        websocket: WebSocket,
        nick: str,
        player_id: str | None = None,
    ) -> tuple[Player | None, str | None]:
        room = self.rooms.get(pin)
        if not room:
            return None, "Pokój o podanym PIN-ie nie istnieje."

        nick = (nick or "").strip()
        if not nick:
            return None, "Nick nie może być pusty."
        if len(nick) > 16:
            return None, "Nick może mieć maksymalnie 16 znaków."

        # Odtworzenie sesji po odświeżeniu
        if player_id and player_id in room.players:
            player = room.players[player_id]
            if player.nick.lower() != nick.lower():
                return None, "Nick nie pasuje do istniejącej sesji."
            player.websocket = websocket
            player.connected = True
            await self.broadcast_host(room)
            return player, None

        existing = self.find_player_by_nick(room, nick)
        if existing:
            if existing.connected and existing.websocket is not None:
                return None, "Ten nick jest już zajęty."
            # Ponowne dołączenie po rozłączeniu – ten sam nick
            existing.websocket = websocket
            existing.connected = True
            await self.broadcast_host(room)
            return existing, None

        if room.state == "playing":
            return None, "Gra już trwa – dołącz w następnej rundzie."

        new_id = player_id or str(uuid.uuid4())
        if new_id in room.players:
            new_id = str(uuid.uuid4())

        player = Player(
            player_id=new_id, nick=nick, websocket=websocket, connected=True
        )
        room.players[new_id] = player
        room.nicks.add(nick.lower())
        await self.broadcast_host(room)
        return player, None

    async def disconnect_player(self, pin: str, player_id: str) -> None:
        room = self.rooms.get(pin)
        if not room or player_id not in room.players:
            return
        player = room.players[player_id]
        player.websocket = None
        player.connected = False
        await self.broadcast_host(room)

    async def disconnect_host(self, pin: str) -> None:
        room = self.rooms.get(pin)
        if not room:
            return
        room.host_ws = None
        # Informuj graczy, że host się rozłączył (pokój zostaje – host może wrócić?
        # Dla prostoty zamykamy pokój dopiero gdy host zniknie na dobre w main)
        await self.broadcast_players(room, {"type": "host_disconnected"})

    def _deal_decks(self, room: Room) -> None:
        pool = list(CARDS)
        for player in room.players.values():
            if len(pool) >= CARDS_PER_PLAYER:
                dealt = random.sample(pool, CARDS_PER_PLAYER)
            else:
                dealt = random.choices(pool, k=CARDS_PER_PLAYER)
            player.deck = dealt
            player.current_index = 0
            player.answered = 0
            player.finished = False
            player.finish_place = None
            player.finish_seconds = None
            player.streak = 0
            player.score = 0
            player.locked_until = 0.0
        room.finish_order = []
        room.started_at = time.time()

    async def start_game(self, room: Room) -> str | None:
        if room.state == "playing":
            return "Gra już trwa."
        connected = [p for p in room.players.values() if p.connected]
        if not connected:
            return "Brak graczy w pokoju."

        self._deal_decks(room)
        room.state = "playing"

        for player in room.players.values():
            if player.websocket and player.connected:
                await self._safe_send(
                    player.websocket,
                    {
                        "type": "game_started",
                        "cards": [public_card(c) for c in player.deck],
                        "score": player.score,
                    },
                )

        await self.broadcast_host(room)
        return None

    async def new_round(self, room: Room) -> str | None:
        if not room.players:
            return "Brak graczy w pokoju."

        self._deal_decks(room)
        room.state = "playing"

        for player in room.players.values():
            if player.websocket and player.connected:
                await self._safe_send(
                    player.websocket,
                    {
                        "type": "new_round",
                        "cards": [public_card(c) for c in player.deck],
                        "score": player.score,
                    },
                )

        await self.broadcast_host(room)
        return None

    async def end_round(self, room: Room) -> str | None:
        if room.state != "playing":
            return "Runda nie jest w toku."
        room.state = "finished"
        await self.broadcast_host(room)
        await self.broadcast_players(
            room,
            {"type": "round_finished", "leaderboard": room.leaderboard()},
        )
        return None

    async def submit_answer(
        self,
        room: Room,
        player: Player,
        card_id: int,
        answer: bool,
    ) -> dict[str, Any]:
        now = time.time()
        if room.state != "playing":
            return {"type": "error", "message": "Gra nie jest w toku."}

        if player.finished:
            return {"type": "error", "message": "Ukończyłeś już wszystkie karty."}

        if now < player.locked_until:
            remaining = round(player.locked_until - now, 2)
            return {
                "type": "error",
                "message": f"Blokada – poczekaj {remaining}s.",
                "locked_until": player.locked_until,
            }

        if player.current_index >= len(player.deck):
            return {"type": "error", "message": "Brak kolejnych kart."}

        current = player.deck[player.current_index]
        if current["id"] != card_id:
            return {"type": "error", "message": "To nie jest Twoja aktualna karta."}

        full = get_card_by_id(card_id) or current
        expected = str(full.get("answer", "")).upper()
        # Frontend wysyła true = FAKT, false = PULAPKA
        player_answer = "FAKT" if bool(answer) else "PULAPKA"
        correct = player_answer == expected
        bonus = 0
        lockout = 0.0

        if correct:
            player.streak += 1
            gained = CORRECT_POINTS
            if player.streak >= STREAK_THRESHOLD:
                bonus = STREAK_BONUS
                gained += bonus
            player.score += gained
        else:
            player.streak = 0
            player.score = max(0, player.score - WRONG_PENALTY)
            lockout = now + LOCKOUT_SECONDS
            player.locked_until = lockout

        player.answered += 1
        player.current_index += 1

        finish_bonus = 0
        if player.current_index >= len(player.deck):
            player.finished = True
            room.finish_order.append(player.player_id)
            place = len(room.finish_order)
            player.finish_place = place
            if room.started_at is not None:
                player.finish_seconds = round(now - room.started_at, 1)
            if place <= len(FINISH_BONUSES):
                finish_bonus = FINISH_BONUSES[place - 1]
                player.score += finish_bonus

        next_card = None
        if not player.finished and player.current_index < len(player.deck):
            next_card = public_card(player.deck[player.current_index])

        result = {
            "type": "answer_result",
            "correct": correct,
            "explanation": full.get("explanation", ""),
            "answer": expected,
            "score": player.score,
            "streak": player.streak,
            "bonus": bonus,
            "finish_bonus": finish_bonus,
            "locked_until": player.locked_until if not correct else 0,
            "finished": player.finished,
            "finish_place": player.finish_place,
            "finish_seconds": player.finish_seconds,
            "answered": player.answered,
            "total": len(player.deck),
            "next_card": next_card,
        }

        await self.broadcast_host(room)

        if all(p.finished or not p.connected for p in room.players.values()) and any(
            p.finished for p in room.players.values()
        ):
            # Gdy wszyscy połączeni skończyli – oznacz rundę jako finished
            active = [p for p in room.players.values() if p.connected]
            if active and all(p.finished for p in active):
                room.state = "finished"
                await self.broadcast_host(room)
                await self.broadcast_players(
                    room,
                    {"type": "round_finished", "leaderboard": room.leaderboard()},
                )

        return result

    async def broadcast_host(self, room: Room) -> None:
        if not room.host_ws:
            return
        payload = {
            "type": "state",
            "pin": room.pin,
            "phase": room.state,
            "players": room.leaderboard(),
            "started_at": room.started_at,
        }
        await self._safe_send(room.host_ws, payload)

    async def broadcast_players(self, room: Room, message: dict[str, Any]) -> None:
        for player in room.players.values():
            if player.websocket and player.connected:
                await self._safe_send(player.websocket, message)

    @staticmethod
    async def _safe_send(ws: WebSocket, message: dict[str, Any]) -> None:
        try:
            await ws.send_json(message)
        except Exception:
            pass


manager = GameManager()
