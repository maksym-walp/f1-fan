const { createApp, ref, reactive, computed, onMounted, watch } = Vue;

const API = 'http://localhost:8000';

async function api(method, path, body) {
  const opts = { method, headers: { 'Content-Type': 'application/json' } };
  if (body !== undefined) opts.body = JSON.stringify(body);
  const res = await fetch(API + path, opts);
  if (res.status === 204) return null;
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'API error');
  return data;
}

createApp({
  setup() {
    // ── Navigation ────────────────────────────────────────────────────────
    const tabs = ['seasons', 'teams', 'pilots', 'circuits', 'grandprix', 'results'];
    const activeTab = ref(location.hash.replace('#', '') || 'seasons');
    watch(activeTab, v => { location.hash = v; });

    // ── Toasts ────────────────────────────────────────────────────────────
    const toasts = ref([]);
    function toast(msg, type = 'info') {
      const id = Date.now();
      toasts.value.push({ id, msg, type });
      setTimeout(() => { toasts.value = toasts.value.filter(t => t.id !== id); }, 3000);
    }

    // ── Generic modal state ───────────────────────────────────────────────
    const modal = reactive({ open: false, mode: 'create', entity: null, data: {} });
    function closeModal() { modal.open = false; modal.data = {}; }

    // ── Seasons ───────────────────────────────────────────────────────────
    const seasons = ref([]);
    async function loadSeasons() {
      seasons.value = await api('GET', '/seasons/');
    }
    function openSeasonModal(s = null) {
      modal.entity = 'season';
      modal.mode = s ? 'edit' : 'create';
      modal.data = s ? { id: s.id, year: s.year, regulation: s.regulation || '' } : { year: '', regulation: '' };
      modal.open = true;
    }
    async function saveSeason() {
      try {
        if (modal.mode === 'create') {
          await api('POST', '/seasons/', { year: Number(modal.data.year), regulation: modal.data.regulation || null });
          toast('Season created', 'success');
        } else {
          await api('PUT', `/seasons/${modal.data.id}`, { year: Number(modal.data.year), regulation: modal.data.regulation || null });
          toast('Season updated', 'success');
        }
        closeModal();
        loadSeasons();
      } catch (e) { toast(e.message, 'error'); }
    }
    async function deleteSeason(id) {
      if (!confirm('Delete this season?')) return;
      await api('DELETE', `/seasons/${id}`);
      toast('Deleted', 'success');
      loadSeasons();
    }

    // ── Teams ─────────────────────────────────────────────────────────────
    const teams = ref([]);
    async function loadTeams() {
      teams.value = await api('GET', '/teams/');
    }
    function openTeamModal(t = null) {
      modal.entity = 'team';
      modal.mode = t ? 'edit' : 'create';
      modal.data = t ? { id: t.id, name: t.name, country: t.country || '', director: t.director || '' } : { name: '', country: '', director: '' };
      modal.open = true;
    }
    async function saveTeam() {
      try {
        const body = { name: modal.data.name, country: modal.data.country || null, director: modal.data.director || null };
        if (modal.mode === 'create') {
          await api('POST', '/teams/', body);
          toast('Team created', 'success');
        } else {
          await api('PUT', `/teams/${modal.data.id}`, body);
          toast('Team updated', 'success');
        }
        closeModal();
        loadTeams();
      } catch (e) { toast(e.message, 'error'); }
    }
    async function deleteTeam(id) {
      if (!confirm('Delete this team?')) return;
      await api('DELETE', `/teams/${id}`);
      toast('Deleted', 'success');
      loadTeams();
    }

    // ── Pilots ────────────────────────────────────────────────────────────
    const pilots = ref([]);
    async function loadPilots() {
      pilots.value = await api('GET', '/pilots/');
    }
    function openPilotModal(p = null) {
      modal.entity = 'pilot';
      modal.mode = p ? 'edit' : 'create';
      modal.data = p ? { id: p.id, name: p.name, country: p.country || '', photo_url: p.photo_url || '', team_id: p.team_id || '' } : { name: '', country: '', photo_url: '', team_id: '' };
      modal.open = true;
    }
    async function savePilot() {
      try {
        const body = { name: modal.data.name, country: modal.data.country || null, photo_url: modal.data.photo_url || null, team_id: modal.data.team_id ? Number(modal.data.team_id) : null };
        if (modal.mode === 'create') {
          await api('POST', '/pilots/', body);
          toast('Pilot created', 'success');
        } else {
          await api('PUT', `/pilots/${modal.data.id}`, body);
          toast('Pilot updated', 'success');
        }
        closeModal();
        loadPilots();
      } catch (e) { toast(e.message, 'error'); }
    }
    async function deletePilot(id) {
      if (!confirm('Delete this pilot?')) return;
      await api('DELETE', `/pilots/${id}`);
      toast('Deleted', 'success');
      loadPilots();
    }

    // ── Circuits ──────────────────────────────────────────────────────────
    const circuits = ref([]);
    async function loadCircuits() {
      circuits.value = await api('GET', '/circuits/');
    }
    function openCircuitModal(c = null) {
      modal.entity = 'circuit';
      modal.mode = c ? 'edit' : 'create';
      modal.data = c ? { id: c.id, name: c.name, country: c.country || '', length_km: c.length_km || '' } : { name: '', country: '', length_km: '' };
      modal.open = true;
    }
    async function saveCircuit() {
      try {
        const body = { name: modal.data.name, country: modal.data.country || null, length_km: modal.data.length_km ? Number(modal.data.length_km) : null };
        if (modal.mode === 'create') {
          await api('POST', '/circuits/', body);
          toast('Circuit created', 'success');
        } else {
          await api('PUT', `/circuits/${modal.data.id}`, body);
          toast('Circuit updated', 'success');
        }
        closeModal();
        loadCircuits();
      } catch (e) { toast(e.message, 'error'); }
    }
    async function deleteCircuit(id) {
      if (!confirm('Delete this circuit?')) return;
      await api('DELETE', `/circuits/${id}`);
      toast('Deleted', 'success');
      loadCircuits();
    }

    // ── Grand Prix ────────────────────────────────────────────────────────
    const grandPrixList = ref([]);
    async function loadGrandPrix() {
      grandPrixList.value = await api('GET', '/grandprix/');
    }
    function openGPModal(gp = null) {
      modal.entity = 'grandprix';
      modal.mode = gp ? 'edit' : 'create';
      modal.data = gp ? { id: gp.id, name: gp.name, season_id: gp.season_id, circuit_id: gp.circuit_id, date: gp.date } : { name: '', season_id: '', circuit_id: '', date: '' };
      modal.open = true;
    }
    async function saveGP() {
      try {
        const body = { name: modal.data.name, season_id: Number(modal.data.season_id), circuit_id: Number(modal.data.circuit_id), date: modal.data.date };
        if (modal.mode === 'create') {
          await api('POST', '/grandprix/', body);
          toast('Grand Prix created', 'success');
        } else {
          await api('PUT', `/grandprix/${modal.data.id}`, body);
          toast('Grand Prix updated', 'success');
        }
        closeModal();
        loadGrandPrix();
      } catch (e) { toast(e.message, 'error'); }
    }
    async function deleteGP(id) {
      if (!confirm('Delete this Grand Prix?')) return;
      await api('DELETE', `/grandprix/${id}`);
      toast('Deleted', 'success');
      loadGrandPrix();
    }

    // ── Results ───────────────────────────────────────────────────────────
    const results = ref([]);
    const selectedGP = ref('');
    async function loadResults() {
      const qs = selectedGP.value ? `?grand_prix_id=${selectedGP.value}` : '';
      results.value = await api('GET', `/results/${qs}`);
    }
    watch(selectedGP, loadResults);
    function openResultModal() {
      modal.entity = 'result';
      modal.mode = 'create';
      modal.data = { grand_prix_id: selectedGP.value || '', pilot_id: '', finish_position: '', points: '', fastest_lap: false };
      modal.open = true;
    }
    async function saveResult() {
      try {
        const body = {
          grand_prix_id: Number(modal.data.grand_prix_id),
          pilot_id: Number(modal.data.pilot_id),
          finish_position: modal.data.finish_position ? Number(modal.data.finish_position) : null,
          points: modal.data.points ? Number(modal.data.points) : null,
          fastest_lap: !!modal.data.fastest_lap,
        };
        await api('POST', '/results/', body);
        toast('Result added', 'success');
        closeModal();
        loadResults();
      } catch (e) { toast(e.message, 'error'); }
    }
    async function deleteResult(id) {
      if (!confirm('Delete this result?')) return;
      await api('DELETE', `/results/${id}`);
      toast('Deleted', 'success');
      loadResults();
    }

    // ── Import / Export ───────────────────────────────────────────────────
    async function importData() {
      try {
        const res = await api('POST', '/import-json?path=data.json');
        toast(`Imported: ${JSON.stringify(res.imported)}`, 'success');
        loadSeasons(); loadTeams(); loadPilots(); loadCircuits(); loadGrandPrix(); loadResults();
      } catch (e) { toast(e.message, 'error'); }
    }
    function exportData() {
      window.open(API + '/export-json', '_blank');
    }

    // ── Modal save dispatcher ─────────────────────────────────────────────
    function saveModal() {
      const map = { season: saveSeason, team: saveTeam, pilot: savePilot, circuit: saveCircuit, grandprix: saveGP, result: saveResult };
      map[modal.entity]?.();
    }

    // ── Load on mount ─────────────────────────────────────────────────────
    onMounted(() => {
      loadSeasons(); loadTeams(); loadPilots(); loadCircuits(); loadGrandPrix(); loadResults();
    });

    return {
      tabs, activeTab,
      toasts,
      modal, closeModal, saveModal,
      seasons, openSeasonModal, deleteSeason,
      teams, openTeamModal, deleteTeam,
      pilots, openPilotModal, deletePilot,
      circuits, openCircuitModal, deleteCircuit,
      grandPrixList, selectedGP, openGPModal, deleteGP,
      results, openResultModal, deleteResult,
      importData, exportData,
    };
  }
}).mount('#app');
