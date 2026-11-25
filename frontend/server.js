const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const API_URL = process.env.API_URL || 'http://localhost:5000';

// Entrega a URL da API para o navegador (o front nunca fala com o banco)
app.get('/config.js', (req, res) => {
  res.type('application/javascript').send(`window.API_URL = ${JSON.stringify(API_URL)};`);
});

app.use('/apps', express.static(path.join(__dirname, 'apps')));
app.get('/', (req, res) => res.redirect('/apps/login/login.html'));

app.listen(PORT, () => console.log(`Front-end em http://localhost:${PORT} (API: ${API_URL})`));