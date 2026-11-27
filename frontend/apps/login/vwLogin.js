// POST /login -> { token, usuario }
async function login(loginUsuario, senha) {
  return apiFetch('/login', {
    method: 'POST',
    body: JSON.stringify({ login: loginUsuario, senha }),
  });
}

if (Auth.token()) window.location.replace('/apps/home/home.html');

const formLogin = document.getElementById('formLogin');
const carregando = document.getElementById('carregando');
const botaoEntrar = formLogin.querySelector('button[type="submit"]');

function limparCarregamento() {
  carregando.hidden = true;
  botaoEntrar.disabled = false;
  formLogin.removeAttribute('aria-busy');
}

window.addEventListener('pageshow', (ev) => {
  if (Auth.token()) {
    if (ev.persisted) window.location.replace('/apps/home/home.html');
    return;
  }
  limparCarregamento();
});

formLogin.addEventListener('submit', async (ev) => {
  ev.preventDefault();
  const erro = document.getElementById('erro');
  erro.hidden = true;
  carregando.hidden = false;
  botaoEntrar.disabled = true;
  formLogin.setAttribute('aria-busy', 'true');
  const aguardarAnimacao = new Promise((resolve) => window.setTimeout(resolve, 3000));
  let redirecionarParaHome = false;

  try {
    const r = await login(
      document.getElementById('login').value.trim(),
      document.getElementById('senha').value
    );
    await aguardarAnimacao;
    Auth.salvar(r.token, r.usuario);
    redirecionarParaHome = true;
  } catch (e) {
    await aguardarAnimacao;
    erro.textContent = e.message;
    erro.hidden = false;
  } finally {
    limparCarregamento();
  }

  if (redirecionarParaHome) window.location.replace('/apps/home/home.html');
});
