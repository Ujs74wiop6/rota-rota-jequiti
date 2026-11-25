// Única porta de saída para o back-end. Anexa o JWT em toda requisição.
async function apiFetch(caminho, opcoes = {}) {
  const headers = { 'Content-Type': 'application/json', ...(opcoes.headers || {}) };
  if (Auth.token()) headers['Authorization'] = 'Bearer ' + Auth.token();

  let resp;
  try {
    resp = await fetch(window.API_URL + caminho, { ...opcoes, headers });
  } catch (e) {
    throw new Error('Não foi possível conectar à API.');
  }

  if (resp.status === 401 && caminho !== '/login') {
    Auth.sair();
    throw new Error('Sessão expirada. Faça login novamente.');
  }

  const dados = await resp.json().catch(() => ({}));
  if (!resp.ok) throw new Error(dados.erro || dados.mensagem || `Erro ${resp.status}`);
  return dados;
}
