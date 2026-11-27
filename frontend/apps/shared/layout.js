// Barra de navegação comum a todas as telas (exceto login)
function esc(valor) {
  return String(valor ?? '').replace(/[&<>"']/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
}

function fmtData(valor) {
  if (!valor) return '—';
  const [ano, mes, dia] = String(valor).slice(0, 10).split('-');
  return `${dia}/${mes}/${ano}`;
}

function montarNav(ativo) {
  const itens = [
    ['home', 'Início', '/apps/home/home.html'],
    ['pasto', 'Pastos', '/apps/pasto/pasto.html'],
    ['piquete', 'Piquetes', '/apps/piquete/piquete.html'],
    ['animal', 'Animais', '/apps/animal/animal.html'],
    ['alocado', 'Alocações', '/apps/alocado/alocado.html'],
  ];
  const links = itens
    .map(([id, rotulo, url]) => `<a href="${url}" class="${id === ativo ? 'ativo' : ''}">${rotulo}</a>`)
    .join('');
  document.getElementById('nav').innerHTML = `
    <nav class="topo">
      <span class="marca">Rota-Rota Jequiti</span>
      <div class="links">${links}</div>
      <div class="usuario">${esc(Auth.usuario())} <button id="btnSair" class="btn-sec">Sair</button></div>
    </nav>`;
  document.getElementById('btnSair').addEventListener('click', Auth.sair);
}

function montarImagemSistema() {
  const principal = document.querySelector('main');
  if (!principal) return;

  const layout = document.createElement('div');
  layout.className = 'layout-sistema';

  const imagem = document.createElement('img');
  imagem.src = '/img/perfil.jpg';
  imagem.alt = 'Imagem do sistema';
  imagem.className = 'imagem-sistema';

  principal.parentNode.insertBefore(layout, principal);
  layout.appendChild(imagem);
  layout.appendChild(principal);
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('nav')) {
    Auth.exigirLogin();
    montarNav(document.body.dataset.app);
    montarImagemSistema();
  }
});