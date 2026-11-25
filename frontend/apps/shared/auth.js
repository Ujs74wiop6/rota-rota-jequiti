// Guarda o JWT e o usuário no localStorage após o login
const Auth = {
  salvar(token, usuario) {
    localStorage.setItem('token', token);
    localStorage.setItem('usuario', usuario);
  },
  token() {
    return localStorage.getItem('token');
  },
  usuario() {
    return localStorage.getItem('usuario');
  },
  sair() {
    localStorage.removeItem('token');
    localStorage.removeItem('usuario');
    window.location.href = '/apps/login/login.html';
  },
  exigirLogin() {
    if (!Auth.token()) window.location.href = '/apps/login/login.html';
  },
};
