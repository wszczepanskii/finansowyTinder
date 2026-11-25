"""Pula kart „Fakt czy Pułapka?” – edukacja finansowa."""

from __future__ import annotations

from typing import Any

CARDS: list[dict[str, Any]] = [
    {
        "id": 1,
        "statement": "BLIK to polski bank działający wyłącznie w aplikacji mobilnej.",
        "answer": "PULAPKA",
        "explanation": "BLIK to system płatności mobilnych, a nie bank.",
    },
    {
        "id": 2,
        "statement": "Fintech to osobna kategoria prawna instytucji finansowej w Polsce.",
        "answer": "PULAPKA",
        "explanation": "Fintech to technologia i sposób świadczenia usług, który przecina sektor bankowy i pozabankowy.",
    },
    {
        "id": 3,
        "statement": "Płatność odroczona (BNPL) bez odsetek nie jest formą zadłużenia.",
        "answer": "PULAPKA",
        "explanation": "Brak odsetek nie oznacza braku zobowiązania – trzeba je uwzględnić w budżecie.",
    },
    {
        "id": 4,
        "statement": "W Narodowym Banku Polskim każdy student może założyć darmowe konto osobiste.",
        "answer": "PULAPKA",
        "explanation": "Bank centralny (NBP) emituje pieniądz i prowadzi politykę pieniężną – nie obsługuje zwykłych klientów.",
    },
    {
        "id": 5,
        "statement": "Inwestowanie na rynku kapitałowym zawsze gwarantuje przynajmniej minimalny zysk.",
        "answer": "PULAPKA",
        "explanation": "Inwestowanie wiąże się z ryzykiem i nigdy nie gwarantuje zysku.",
    },
    {
        "id": 6,
        "statement": "Komisja Nadzoru Finansowego (KNF) udziela młodym firmom tanich kredytów na start.",
        "answer": "PULAPKA",
        "explanation": "KNF sprawuje nadzór nad rynkiem finansowym, ale nie finansuje działalności firm.",
    },
    {
        "id": 7,
        "statement": "Wysoka sprzedaż w firmie całkowicie wyklucza problemy z płynnością finansową.",
        "answer": "PULAPKA",
        "explanation": "Przychód na fakturze z odroczonym terminem nie oznacza natychmiastowej gotówki na koncie.",
    },
    {
        "id": 8,
        "statement": "Leasing pozwala korzystać ze sprzętu firmowego bez płacenia całej jego wartości od razu.",
        "answer": "FAKT",
        "explanation": "Pozwala rozłożyć koszty korzystania z komputera, aparatu czy auta w czasie.",
    },
    {
        "id": 9,
        "statement": "Faktoring polega na zamianie wystawionej faktury na gotówkę jeszcze przed terminem płatności.",
        "answer": "FAKT",
        "explanation": "Faktor wypłaca środki z nieprzeterminowanej faktury, poprawiając płynność firmy.",
    },
    {
        "id": 10,
        "statement": "Bankowy Fundusz Gwarancyjny (BFG) chroni kwalifikujące się depozyty w razie upadku banku.",
        "answer": "FAKT",
        "explanation": "BFG odpowiada za system gwarantowania depozytów w objętych nim instytucjach.",
    },
    {
        "id": 11,
        "statement": "Wszystkie usługi oferowane pod marką Revolut mają dokładnie taki sam status prawny.",
        "answer": "PULAPKA",
        "explanation": "Klasyfikacja prawna zależy od konkretnego podmiotu świadczącego daną usługę pod tą marką.",
    },
    {
        "id": 12,
        "statement": "Towarzystwa ubezpieczeniowe i firmy leasingowe to pozabankowe instytucje finansowe.",
        "answer": "FAKT",
        "explanation": "Należą do kategorii pozabankowej wyodrębnionej ze względu na specyficzne funkcje.",
    },
    {
        "id": 13,
        "statement": "Płacąc telefonem za poranną kawę, korzystasz z usług banku oraz operatora płatności.",
        "answer": "FAKT",
        "explanation": "Codzienne mikrotransakcje łączą rachunek bankowy z infrastrukturą operatora płatności.",
    },
    {
        "id": 14,
        "statement": "Firma faktoringowa zawsze wypłaca 100% wartości faktury w dniu jej wystawienia.",
        "answer": "PULAPKA",
        "explanation": "Faktor wypłaca zaliczkę (np. 80%) pomniejsą o koszty i tylko pod warunkiem akceptacji faktury.",
    },
    {
        "id": 15,
        "statement": "Banki spółdzielcze często obsługują lokalne społeczności i lokalne przedsiębiorstwa.",
        "answer": "FAKT",
        "explanation": "Działają na zasadach spółdzielczych, wspierając głównie rynek lokalny.",
    },
    {
        "id": 16,
        "statement": "Wprowadzenie płatności odroczonych w e-sklepie gwarantuje firmie wzrost sprzedaży.",
        "answer": "PULAPKA",
        "explanation": "Zwiększa wygodę klientów, ale nie gwarantuje większej sprzedaży i generuje koszty dla sklepu.",
    },
    {
        "id": 17,
        "statement": "Ubezpieczeniowy Fundusz Gwarancyjny (UFG) zajmuje się m.in. zadaniami z obszaru ubezpieczeń obowiązkowych.",
        "answer": "FAKT",
        "explanation": "Współtworzy system bezpieczeństwa i zaufania na rynku ubezpieczeniowym.",
    },
    {
        "id": 18,
        "statement": "Dom maklerski to instytucja bankowa zajmująca się głównie przyjmowaniem depozytów.",
        "answer": "PULAPKA",
        "explanation": "Dom maklerski to pozabankowa instytucja świadcząca usługi inwestycyjne.",
    },
    {
        "id": 19,
        "statement": "Pośrednictwo finansowe polega na przepływie kapitału od osób z nadwyżkami do potrzebujących środków.",
        "answer": "FAKT",
        "explanation": "Przykładem jest depozyt Julii w banku, z którego finansowany jest kredyt Michała.",
    },
    {
        "id": 20,
        "statement": "Nowa marka odzieżowa bez historii działalności bez trudu dostanie wysoki kredyt bankowy.",
        "answer": "PULAPKA",
        "explanation": "Brak historii działalności i zdolności kredytowej utrudnia uzyskanie kredytu na start.",
    },
    {
        "id": 21,
        "statement": "KNF, BFG i UFG nie udzielają pożyczek, lecz tworzą system bezpieczeństwa rynku finansowego.",
        "answer": "FAKT",
        "explanation": "Ich rolą jest nadzór, stabilność i ochrona uczestników rynku, a nie finansowanie biznesu.",
    },
    {
        "id": 22,
        "statement": "Leasing sprzętu jest zawsze tańszy w całkowitym rozrachunku niż zakup za gotówkę.",
        "answer": "PULAPKA",
        "explanation": "Leasing chroni gotówkę na start, ale zawsze trzeba porównać jego całkowity koszt z zakupem gotówkowym.",
    },
    {
        "id": 23,
        "statement": "Emisja pieniądza oraz polityka pieniężna to podstawowe zadania banku centralnego.",
        "answer": "FAKT",
        "explanation": "W Polsce odpowiada za to Narodowy Bank Polski (NBP).",
    },
    {
        "id": 24,
        "statement": "PZU jest przykładem pozabankowej instytucji działającej w sektorze ubezpieczeń.",
        "answer": "FAKT",
        "explanation": "Towarzystwa ubezpieczeniowe ograniczają finansowe skutki zdarzeń losowych.",
    },
    {
        "id": 25,
        "statement": "Instytucje płatnicze nie należą do rynku finansowego, ponieważ nie udzielają kredytów.",
        "answer": "PULAPKA",
        "explanation": "Są częścią rynku finansowego i świadczą określone ustawowo usługi płatnicze.",
    },
    {
        "id": 26,
        "statement": "Ubezpieczenie majątku firmy ogranicza skutki finansowe kradzieży, pożaru czy zalania magazynu.",
        "answer": "FAKT",
        "explanation": "To realizacja funkcji ochrony przed ryzykiem.",
    },
    {
        "id": 27,
        "statement": "Korzystanie z czterech różnych instytucji finansowych jednego dnia wymaga wizyty w placówce.",
        "answer": "PULAPKA",
        "explanation": "Bank, operator płatności, BNPL i ubezpieczyciel działają dziś w pełni cyfrowo.",
    },
    {
        "id": 28,
        "statement": "Firma faktoringowa ma prawo odmówić przyjęcia faktury do finansowania.",
        "answer": "FAKT",
        "explanation": "Wypłata środków zależy od oceny i akceptacji faktury przez faktora oraz warunków umowy.",
    },
    {
        "id": 29,
        "statement": "Przelewy, płatności kartą, telefonem i BLIK-iem realizują funkcję rozliczeniową.",
        "answer": "FAKT",
        "explanation": "To jedna z czterech głównych funkcji instytucji finansowych.",
    },
    {
        "id": 30,
        "statement": "Rachunek firmowy służy m.in. do oddzielenia finansów firmy od prywatnych pieniędzy właścicieli.",
        "answer": "FAKT",
        "explanation": "Ułatwia też bieżące rozliczenia z dostawcami i urzędami.",
    },
]


def get_card_by_id(card_id: int) -> dict[str, Any] | None:
    for card in CARDS:
        if card["id"] == card_id:
            return card
    return None


def public_card(card: dict[str, Any]) -> dict[str, Any]:
    """Karta bez odpowiedzi – do wysłania graczowi."""
    return {
        "id": card["id"],
        "statement": card["statement"],
    }
