// ---- Funções que consomem as APIs de pasto ----
const getAllPasto = () => apiFetch('/pasto');
const getPastoByID = (id) => apiFetch(`/pasto/${id}`);
const insertPasto = (dados) => apiFetch('/pasto', { method: 'POST', body: JSON.stringify(dados) });
const updatePasto = (id, dados) => apiFetch(`/pasto/${id}`, { method: 'PUT', body: JSON.stringify(dados) });
const deletePasto = (id) => apiFetch(`/pasto/${id}`, { method: 'DELETE' });

// ---- Tela ----
if (document.body.dataset.app === 'pasto') {
  iniciarCrud({
    titulo: 'Pastos',
    singular: 'pasto',
    idCampo: 'pastoid',
    colunas: [
      { campo: 'pastoid', rotulo: 'ID' },
      { campo: 'descricao', rotulo: 'Descrição' },
      { campo: 'areatotal', rotulo: 'Área total (ha)', fmt: (v) => Number(v).toLocaleString('pt-BR', { minimumFractionDigits: 2 }) },
    ],
    campos: [
      { nome: 'descricao', rotulo: 'Descrição', tipo: 'text', obrigatorio: true },
      { nome: 'areatotal', rotulo: 'Área total (ha)', tipo: 'number', step: '0.01', obrigatorio: true },
    ],
    api: { getAll: getAllPasto, getById: getPastoByID, insert: insertPasto, update: updatePasto, delete: deletePasto },
  });
}
