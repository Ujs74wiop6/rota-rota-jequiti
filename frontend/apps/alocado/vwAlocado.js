// ---- Funções que consomem as APIs de alocado ----
const getAllAlocado = () => apiFetch('/alocado');
const getAlocadoByID = (id) => apiFetch(`/alocado/${id}`);
const insertAlocado = (dados) => apiFetch('/alocado', { method: 'POST', body: JSON.stringify(dados) });
const updateAlocado = (id, dados) => apiFetch(`/alocado/${id}`, { method: 'PUT', body: JSON.stringify(dados) });
const deleteAlocado = (id) => apiFetch(`/alocado/${id}`, { method: 'DELETE' });

// ---- Tela ----
if (document.body.dataset.app === 'alocado') {
  iniciarCrud({
    titulo: 'Alocações de animais em piquetes',
    singular: 'alocação',
    idCampo: 'alocadoid',
    contexto: async () => {
      const [animais, piquetes] = await Promise.all([getAllAnimal(), getAllPiquete()]);
      return {
        animais: Object.fromEntries(animais.map((a) => [a.animalid, a.nome])),
        piquetes: Object.fromEntries(piquetes.map((p) => [p.piqueteid, p.descricao])),
      };
    },
    colunas: [
      { campo: 'alocadoid', rotulo: 'ID' },
      { campo: 'animalidifk', rotulo: 'Animal', fmt: (v, l, ctx) => esc(ctx.animais[v] ?? v) },
      { campo: 'piqueteidfk', rotulo: 'Piquete', fmt: (v, l, ctx) => esc(ctx.piquetes[v] ?? v) },
      { campo: 'datainicio', rotulo: 'Início', fmt: (v) => fmtData(v) },
      //{ campo: 'datafinal', rotulo: 'Final', fmt: (v) => (v ? fmtData(v) : '...') },
      { campo: 'datafinal', rotulo: 'Final', fmt: (v) => (v ? fmtData(v) : '<img src="/img/erro.png" alt="..." title="..." class="icone">') },
    ],
    campos: [
      {
        nome: 'animalidifk', rotulo: 'Animal', tipo: 'select', obrigatorio: true,
        opcoes: async () => (await getAllAnimal()).map((a) => ({ valor: a.animalid, texto: a.nome })),
      },
      {
        nome: 'piqueteidfk', rotulo: 'Piquete', tipo: 'select', obrigatorio: true,
        opcoes: async () => (await getAllPiquete()).map((p) => ({ valor: p.piqueteid, texto: p.descricao })),
      },
      { nome: 'datainicio', rotulo: 'Data de início', tipo: 'date', obrigatorio: true },
      { nome: 'datafinal', rotulo: 'Data final (opcional)', tipo: 'date', obrigatorio: false },
    ],
    validar: (d) => {
      if (d.datafinal && d.datafinal < d.datainicio) {
        throw new Error('A data final não pode ser anterior à data de início.');
      }
    },
    api: { getAll: getAllAlocado, getById: getAlocadoByID, insert: insertAlocado, update: updateAlocado, delete: deleteAlocado },
  });
}
