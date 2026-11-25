// ---- Funções que consomem as APIs de piquete ----
const getAllPiquete = () => apiFetch('/piquete');
const getPiqueteByID = (id) => apiFetch(`/piquete/${id}`);
const insertPiquete = (dados) => apiFetch('/piquete', { method: 'POST', body: JSON.stringify(dados) });
const updatePiquete = (id, dados) => apiFetch(`/piquete/${id}`, { method: 'PUT', body: JSON.stringify(dados) });
const deletePiquete = (id) => apiFetch(`/piquete/${id}`, { method: 'DELETE' });

// ---- Tela ----
if (document.body.dataset.app === 'piquete') {
  iniciarCrud({
    titulo: 'Piquetes',
    singular: 'piquete',
    idCampo: 'piqueteid',
    // mapa id -> descrição do pasto, para exibir o nome em vez do número
    contexto: async () => {
      const pastos = await getAllPasto();
      return { pastos: Object.fromEntries(pastos.map((p) => [p.pastoid, p.descricao])) };
    },
    colunas: [
      { campo: 'piqueteid', rotulo: 'ID' },
      { campo: 'descricao', rotulo: 'Descrição' },
      { campo: 'latitude', rotulo: 'Latitude' },
      { campo: 'longitude', rotulo: 'Longitude' },
      { campo: 'pastoidfk', rotulo: 'Pasto', fmt: (v, l, ctx) => esc(ctx.pastos[v] ?? v) },
    ],
    campos: [
      { nome: 'descricao', rotulo: 'Descrição', tipo: 'text', obrigatorio: true },
      { nome: 'latitude', rotulo: 'Latitude', tipo: 'number', step: '0.000001', obrigatorio: true },
      { nome: 'longitude', rotulo: 'Longitude', tipo: 'number', step: '0.000001', obrigatorio: true },
      {
        nome: 'pastoidfk', rotulo: 'Pasto', tipo: 'select', obrigatorio: true,
        opcoes: async () => (await getAllPasto()).map((p) => ({ valor: p.pastoid, texto: p.descricao })),
      },
    ],
    api: { getAll: getAllPiquete, getById: getPiqueteByID, insert: insertPiquete, update: updatePiquete, delete: deletePiquete },
  });
}
