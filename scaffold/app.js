// Minimal local-only storage (IndexedDB) + export/import + service worker registration.
// DB must be unique per app (same name as APP in sw.js): all of a user's GitHub Pages
// sites share one origin, so a shared name would mix two apps' data.
const DB = 'myapp', STORE = 'kv';
const open = () => new Promise((res, rej) => {
  const r = indexedDB.open(DB, 1);
  r.onupgradeneeded = () => r.result.createObjectStore(STORE);
  r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error);
});
async function tx(mode, fn) {
  const db = await open();
  return new Promise((res, rej) => {
    const t = db.transaction(STORE, mode), s = t.objectStore(STORE), out = fn(s);
    t.oncomplete = () => res(out && out.result); t.onerror = () => rej(t.error);
  });
}
export const get = (k) => tx('readonly', s => s.get(k));
export const set = (k, v) => tx('readwrite', s => s.put(v, k));
async function dump() {
  const db = await open();
  return new Promise((res) => {
    const out = {}, c = db.transaction(STORE).objectStore(STORE).openCursor();
    c.onsuccess = () => { const cur = c.result; if (cur) { out[cur.key] = cur.value; cur.continue(); } else res(out); };
  });
}

document.getElementById('settingsBtn').onclick = () => document.getElementById('settings').showModal();
document.getElementById('closeSettings').onclick = () => document.getElementById('settings').close();
document.getElementById('exportBtn').onclick = async () => {
  const blob = new Blob([JSON.stringify({ app: DB, exportedAt: new Date().toISOString(), data: await dump() }, null, 2)], { type: 'application/json' });
  const a = Object.assign(document.createElement('a'), { href: URL.createObjectURL(blob), download: `${DB}-backup-${new Date().toISOString().slice(0, 10)}.json` });
  a.click(); URL.revokeObjectURL(a.href);
};
document.getElementById('importFile').onchange = async (e) => {
  const file = e.target.files[0]; if (!file) return;
  const { data } = JSON.parse(await file.text());
  for (const [k, v] of Object.entries(data || {})) await set(k, v);
  alert('Backup restored.'); location.reload();
};

if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js');

// --- feature code starts here ---
document.getElementById('app').textContent = 'Hello from your own app.';
