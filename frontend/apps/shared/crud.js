// Renderizador genérico de CRUD: tabela + formulário (dialog).
// Cada módulo (vwPasto.js etc.) só descreve colunas, campos e as 5 funções de API.
async function iniciarCrud(cfg) {
  const raiz = document.getElementById('conteudo');
  raiz.innerHTML = `
    <div class="cabecalho">
      <h1>${esc(cfg.titulo)}</h1>
      <button id="btnNovo" class="btn">+ Novo</button>
    </div>
    <div id="aviso" class="aviso" hidden></div>
    <div class="tabela-wrap"><table>
      <thead><tr>${cfg.colunas.map((c) => `<th>${esc(c.rotulo)}</th>`).join('')}<th class="acoes">Ações</th></tr></thead>
      <tbody id="linhas"></tbody>
    </table></div>
    <dialog id="dlg">
      <form id="form" method="dialog">
        <h2 id="dlgTitulo"></h2>
        <div id="campos"></div>
        <div id="erroForm" class="aviso erro" hidden></div>
        <div class="rodape-dlg">
          <button type="button" id="btnCancelar" class="btn-sec">Cancelar</button>
          <button type="submit" class="btn">Salvar</button>
        </div>
      </form>
    </dialog>`;

  const $ = (id) => document.getElementById(id);
  let editandoId = null;

  function aviso(msg, erro = false) {
    const el = $('aviso');
    el.textContent = msg;
    el.className = 'aviso' + (erro ? ' erro' : '');
    el.hidden = !msg;
  }

  async function carregar() {
    try {
      aviso('');
      const ctx = cfg.contexto ? await cfg.contexto() : {};
      const dados = await cfg.api.getAll();
      $('linhas').innerHTML = dados.length
        ? dados.map((l) => `<tr>
            ${cfg.colunas.map((c) => `<td>${c.fmt ? c.fmt(l[c.campo], l, ctx) : esc(l[c.campo])}</td>`).join('')}
            <td class="acoes">
              <button class="btn-sec" data-acao="editar" data-id="${l[cfg.idCampo]}">Editar</button>
              <button class="btn-perigo" data-acao="excluir" data-id="${l[cfg.idCampo]}">Excluir</button>
            </td></tr>`).join('')
        : `<tr><td colspan="${cfg.colunas.length + 1}" class="vazio">Nenhum registro cadastrado.</td></tr>`;
    } catch (e) {
      aviso(e.message, true);
    }
  }

  async function desenharCampos(valores = {}) {
    let html = '';
    for (const c of cfg.campos) {
      const v = valores[c.nome] ?? '';
      const req = c.obrigatorio ? 'required' : '';
      if (c.tipo === 'select') {
        const ops = await c.opcoes();
        html += `<label>${esc(c.rotulo)}<select name="${c.nome}" ${req}>
          <option value="">Selecione...</option>
          ${ops.map((o) => `<option value="${o.valor}" ${String(o.valor) === String(v) ? 'selected' : ''}>${esc(o.texto)}</option>`).join('')}
        </select></label>`;
      } else {
        const extra = c.tipo === 'number' ? `step="${c.step || 'any'}"` : '';
        const val = c.tipo === 'date' ? String(v).slice(0, 10) : v;
        html += `<label>${esc(c.rotulo)}<input type="${c.tipo}" name="${c.nome}" value="${esc(val)}" ${extra} ${req}></label>`;
      }
    }
    $('campos').innerHTML = html;
  }

  async function abrirForm(id = null) {
    $('erroForm').hidden = true;
    editandoId = id;
    try {
      const valores = id ? await cfg.api.getById(id) : {};
      $('dlgTitulo').textContent = (id ? 'Editar ' : 'Novo ') + cfg.singular;
      await desenharCampos(valores);
      $('dlg').showModal();
    } catch (e) {
      aviso(e.message, true);
    }
  }

  $('btnNovo').addEventListener('click', () => abrirForm());
  $('btnCancelar').addEventListener('click', () => $('dlg').close());

  $('linhas').addEventListener('click', async (ev) => {
    const btn = ev.target.closest('button[data-acao]');
    if (!btn) return;
    const id = btn.dataset.id;
    if (btn.dataset.acao === 'editar') return abrirForm(id);
    if (confirm(`Excluir este registro de ${cfg.singular}?`)) {
      try {
        await cfg.api.delete(id);
        aviso('Registro excluído.');
        carregar();
      } catch (e) {
        aviso(e.message, true);
      }
    }
  });

  $('form').addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const fd = new FormData($('form'));
    const dados = {};
    for (const c of cfg.campos) {
      let v = fd.get(c.nome);
      if (v === '' || v === null) v = null;
      else if (c.tipo === 'number' || c.tipo === 'select') v = Number(v);
      dados[c.nome] = v;
    }
    try {
      if (cfg.validar) cfg.validar(dados);
      if (editandoId) await cfg.api.update(editandoId, dados);
      else await cfg.api.insert(dados);
      $('dlg').close();
      aviso('Registro salvo com sucesso.');
      carregar();
    } catch (e) {
      $('erroForm').textContent = e.message;
      $('erroForm').hidden = false;
    }
  });

  carregar();
}
