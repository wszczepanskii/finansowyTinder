/** Adres HTTP backendu – po wdrożeniu na Render/Railway podmień na publiczny URL. */
const BACKEND_HTTP_URL = "https://finansowy-tinder-api.onrender.com/";

/**
 * Zamienia adres HTTP backendu na WebSocket (ws:// / wss://).
 * @param {string} [path="/"] ścieżka WebSocket, np. "/ws/host"
 * @returns {string}
 */
function getWsUrl(path = "/") {
  const base = BACKEND_HTTP_URL.replace(/\/$/, "");
  const wsBase = base.replace(/^http:\/\//i, "ws://").replace(/^https:\/\//i, "wss://");
  const normalized = path.startsWith("/") ? path : `/${path}`;
  return `${wsBase}${normalized}`;
}
