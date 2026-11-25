# Finansowy Tinder: Fakt czy Pułapka?

Multiplayer party game (WebSockets) inspirowany prezentacją MONEY TALKS / OFFLINE STUDIO.

- `backend/` — Python, FastAPI, WebSockets
- `frontend/` — statyczny HTML + Vue 3 CDN + Tailwind CDN

---

## Uruchomienie lokalne

1. **Backend** (w osobnym terminalu):

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. **Frontend** (serwer statyczny, żeby WebSocket/QR działały poprawnie):

```bash
cd frontend
python -m http.server 5500
```

3. Otwórz w przeglądarce:
   - start: http://localhost:5500/
   - host: http://localhost:5500/host.html
   - gracz: http://localhost:5500/play.html

Domyślny adres API w `frontend/config.js`: `http://localhost:8000`.

---

## Wdrożenie na Render.com (backend + frontend)

Na Render tworzysz **dwa osobne serwisy** z tego samego repozytorium.

### 1. Backend — Web Service

1. Wejdź na [render.com](https://render.com) → **New +** → **Web Service**.
2. Podłącz repozytorium GitHub.
3. Ustawienia:
   - **Name:** np. `finansowy-tinder-api`
   - **Root Directory:** `backend`
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance type:** Free
4. Po deployu skopiuj URL, np. `https://finansowy-tinder-api.onrender.com`.
5. Sprawdź: `https://…onrender.com/health` → `{"status":"ok"}`.

### 2. Frontend — Static Site

1. Najpierw w lokalnym `frontend/config.js` ustaw adres backendu z kroku 1 i wypchnij zmianę do repo:

```js
const BACKEND_HTTP_URL = "https://finansowy-tinder-api.onrender.com";
```

`getWsUrl()` samo zamieni `https://` na `wss://`.

2. Na Render: **New +** → **Static Site**.
3. To samo repozytorium, ustawienia:
   - **Name:** np. `finansowy-tinder`
   - **Root Directory:** `frontend`
   - **Build Command:** pozostaw puste (albo `echo "static"`)
   - **Publish Directory:** `.`
4. Po deployu otwórz URL static site, np. `https://finansowy-tinder.onrender.com`.
5. Host: `…/host.html` · gracz: `…/play.html` (albo strona główna z wyborem).

### Kolejność

1. Deploy backendu → skopiuj URL.  
2. Wpisz URL do `frontend/config.js` → commit + push.  
3. Deploy frontendu (Static Site).  
4. Jeśli zmienisz URL backendu później — zaktualizuj `config.js` i zrób redeploy Static Site.

---

## Alternatywa: frontend na GitHub Pages

1. W `frontend/config.js` ustaw URL backendu z Render.
2. GitHub → **Settings → Pages**.
3. Branch z kodem + folder `/frontend`.
4. Linki są względne (`./config.js`, `./play.html`, `./host.html`), więc działają też w podkatalogu Pages.

---

## Przed prezentacją

Otwórz `host.html` **2–3 minuty wcześniej** — darmowy Render (Web Service) zasypia bez ruchu i pierwsze połączenie WebSocket może potrwać dłużej (ekran hosta pokazuje wtedy „Wybudzanie serwera…”). Static Site zwykle nie zasypia tak samo, ale backend i tak trzeba wybudzić.
