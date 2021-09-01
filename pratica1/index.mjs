import express from 'express';


const app = express()

app.get('/hello', (req, res) => {
  if(req.query.name) {
    res.send(`Hello ${req.query.name}!`)
  }
  else {
    res.send('Hello World!')
  }
});

app.get('/clientes', (req, res) => {
  res.send(['Joao', 'Alba', 'Pedro','Samuel', 'tester'])
});

app.get('/', (req, res) => {
  res.send('Hello Home! \n /clientes for info \n /hello to say hi')
});

app.listen(process.env.PORT, 8000 | "0.0.0.0", () => {
  console.log('App Started...');
})