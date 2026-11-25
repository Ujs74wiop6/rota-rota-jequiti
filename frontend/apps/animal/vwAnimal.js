// ---- Funções que consomem as APIs de animal ----
const getAllAnimal = () => apiFetch('/animal');
const getAnimalByID = (id) => apiFetch(`/animal/${id}`);
const insertAnimal = (dados) => apiFetch('/animal', { method: 'POST', body: JSON.stringify(dados) });
const updateAnimal = (id, dados) => apiFetch(`/animal/${id}`, { method: 'PUT', body: JSON.stringify(dados) });
const deleteAnimal = (id) => apiFetch(`/animal/${id}`, { method: 'DELETE' });

// ---- Tela ----
if (document.body.dataset.app === 'animal') {
  iniciarCrud({
    titulo: 'Animais',
    singular: 'animal',
    idCampo: 'animalid',
    colunas: [
      { campo: 'animalid', rotulo: 'ID' },
      { campo: 'nome', rotulo: 'Nome' },
      { campo: 'datanasc', rotulo: 'Nascimento', fmt: (v) => fmtData(v) },
    ],
    campos: [
      { nome: 'nome', rotulo: 'Nome', tipo: 'text', obrigatorio: true },
      { nome: 'datanasc', rotulo: 'Data de nascimento', tipo: 'date', obrigatorio: true },
    ],
    api: { getAll: getAllAnimal, getById: getAnimalByID, insert: insertAnimal, update: updateAnimal, delete: deleteAnimal },
  });
}
