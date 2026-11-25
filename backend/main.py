"""Finansowy Tinder: Fakt czy Pułapka? – backend FastAPI + WebSockets."""

from __future__ import annotations

import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from game_manager import manager

app = FastAPI(title="Finansowy Tinder: Fakt czy Pułapka?")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.websocket("/ws/host")
async def ws_host(websocket: WebSocket):
    await websocket.accept()
    room = await manager.create_room(websocket)
    pin = room.pin

    try:
        await websocket.send_json({"type": "room_created", "pin": pin})
        await manager.broadcast_host(room)

        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_json(
                    {"type": "error", "message": "Nieprawidłowy JSON."}
                )
                continue

            action = data.get("action") or data.get("type")
            room = manager.get_room(pin)
            if not room:
                await websocket.send_json(
                    {"type": "error", "message": "Pokój nie istnieje."}
                )
                break

            if action == "start":
                err = await manager.start_game(room)
                if err:
                    await websocket.send_json({"type": "error", "message": err})
            elif action == "new_round":
                err = await manager.new_round(room)
                if err:
                    await websocket.send_json({"type": "error", "message": err})
            elif action == "end_round":
                err = await manager.end_round(room)
                if err:
                    await websocket.send_json({"type": "error", "message": err})
            elif action == "ping":
                await websocket.send_json({"type": "pong"})
            else:
                await websocket.send_json(
                    {"type": "error", "message": f"Nieznana akcja: {action}"}
                )

    except WebSocketDisconnect:
        pass
    finally:
        current = manager.get_room(pin)
        if current and current.host_ws is websocket:
            await manager.disconnect_host(pin)
            # Zamknij pokój i powiadom graczy
            for player in list(current.players.values()):
                if player.websocket:
                    try:
                        await player.websocket.send_json(
                            {"type": "error", "message": "Host zakończył sesję."}
                        )
                        await player.websocket.close()
                    except Exception:
                        pass
            await manager.remove_room(pin)


@app.websocket("/ws/play/{pin}")
async def ws_play(websocket: WebSocket, pin: str):
    await websocket.accept()
    pin = pin.strip()
    player = None
    room = manager.get_room(pin)

    if not room:
        await websocket.send_json(
            {"type": "error", "message": "Pokój o podanym PIN-ie nie istnieje."}
        )
        await websocket.close()
        return

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_json(
                    {"type": "error", "message": "Nieprawidłowy JSON."}
                )
                continue

            action = data.get("action") or data.get("type")
            room = manager.get_room(pin)
            if not room:
                await websocket.send_json(
                    {"type": "error", "message": "Pokój został zamknięty."}
                )
                break

            if action == "join":
                nick = data.get("nick", "")
                player_id = data.get("player_id")
                joined, err = await manager.join_player(pin, websocket, nick, player_id)
                if err:
                    await websocket.send_json({"type": "error", "message": err})
                    continue
                player = joined
                payload = {
                    "type": "joined",
                    "player_id": player.player_id,
                    "nick": player.nick,
                    "phase": room.state,
                    "score": player.score,
                }
                if room.state == "playing" and not player.finished:
                    from cards import public_card

                    remaining = [
                        public_card(c) for c in player.deck[player.current_index :]
                    ]
                    payload["cards"] = remaining
                    payload["answered"] = player.answered
                    payload["total"] = len(player.deck)
                elif room.state == "playing" and player.finished:
                    payload["finished"] = True
                    payload["cards"] = []
                await websocket.send_json(payload)

            elif action == "answer":
                if not player:
                    await websocket.send_json(
                        {"type": "error", "message": "Najpierw dołącz do pokoju."}
                    )
                    continue
                card_id = data.get("card_id")
                answer = data.get("answer")
                if card_id is None or answer is None:
                    await websocket.send_json(
                        {
                            "type": "error",
                            "message": "Wymagane: card_id oraz answer (true/false).",
                        }
                    )
                    continue
                result = await manager.submit_answer(
                    room, player, int(card_id), bool(answer)
                )
                await websocket.send_json(result)

            elif action == "ping":
                await websocket.send_json({"type": "pong"})

            else:
                await websocket.send_json(
                    {"type": "error", "message": f"Nieznana akcja: {action}"}
                )

    except WebSocketDisconnect:
        pass
    finally:
        if player:
            await manager.disconnect_player(pin, player.player_id)
