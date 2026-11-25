// POST /login -> { token, usuario }
async function login(loginUsuario, senha) {
  return apiFetch('/login', {
    method: 'POST',
    body: JSON.stringify({ login: loginUsuario, senha }),
  });
}

if (Auth.token()) window.location.href = '/apps/home/home.html';

document.getElementById('formLogin').addEventListener('submit', async (ev) => {
  ev.preventDefault();
  const erro = document.getElementById('erro');
  erro.hidden = true;
  try {
    const r = await login(
      document.getElementById('login').value.trim(),
      document.getElementById('senha').value
    );
    Auth.salvar(r.token, r.usuario);
    window.location.href = '/apps/home/home.html';
  } catch (e) {
    erro.textContent = e.message;
    erro.hidden = false;
  }
});
