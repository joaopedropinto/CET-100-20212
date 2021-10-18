import os
from fastapi import FastAPI, status, Response
from pydantic.errors import NumberNotMultipleError
from uvicorn import Config, Server
from pydantic import BaseModel

PORT = os.environ.get('PORT') or "8000"
app = FastAPI()

class Peer(BaseModel):
    id: str
    nome: str
    url: str

        
data = {
    "server_name": "João Pedro de Gois Pinto",
    "server_endpoint": "https://sd-joaopedrop-20212.herokuapp.com/ ",
    "descrição": "Projeto de SD. Os seguintes serviços estão implementados... "
    "GET/info, PUT/info/, GET/peers, POST/peers, GET/peers{id}, PUT/peers{id}, DELETE/peers{id}",
    "versão": "0.1",
    "status": "online",
    "tipo_de_eleição_ativa": "ring",
}


@app.get('/info', status_code=200)
def info():

   return data

@app.put('/info', status_code=200)
def info(status: str,eleicao: str, response: Response):

    data["status"] = status

    data["tipo_de_eleição_ativa"] = eleicao

    if status is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    if eleicao is None:
        response.status_code = status.HTTP_400_BAD_REQUEST


    return data

peers = {
    "201720295": Peer(id="201720295", nome="Allana Dos Santos Campos", url="https://sd-ascampos-20212.herokuapp.com/"),
    "201512136": Peer(id="201512136", nome="Annya Rita De Souza Ourives", url="https://sd-annyaourives-20212.herokuapp.com/hello"),
    "201512137": Peer(id="201512137", nome="Daniel Andrade Penêdo Santos", url=""),
    "201710375": Peer(id="201710375", nome="Emmanuel Norberto Ribeiro Dos Santos", url="https://sd-emmanuel.herokuapp.com/"),
    "201420373": Peer(id="201420373", nome="Gabriel Figueiredo Góes", url=""),
    "201710377": Peer(id="201710377", nome="Hiago Rios Cordeiro", url="https://sd-api-uesc.herokuapp.com/"),
    "201810665": Peer(id="201810665", nome="Jenilson Ramos Santos", url="https://jenilsonramos-sd-20211.herokuapp.com/"),
    "201610327": Peer(id="201610327", nome="João Pedro De Gois Pinto", url="https://sd-joaopedrop-20212.herokuapp.com/"),
    "201610337": Peer(id="201610337", nome="Luís Carlos Santos Câmara", url="https://sd-20212-luiscarlos.herokuapp.com/"),
    "201620181": Peer(id="201620181", nome="Matheus Santos Rodrigues", url=""),
    "201620400": Peer(id="201620400", nome="Nassim Maron Rihan", url="https://sd-nassimrihan-2021-2.herokuapp.com/"),
    "201710396": Peer(id="201710396", nome="Robert Morais Santos Broketa", url="https://pratica-sd.herokuapp.com/"),
    "201720308": Peer(id="201720308", nome="Victor Dos Santos Santana", url="https://sd-victor-20212.herokuapp.com/")
}

@app.get('/peers')
def get_peers():

    return peers

@app.post('/peers', status_code=400)
def post_peers(id: str, nome: str, url: str, response: Response, peers: Peer):

    if id in peers:
        response.status_code = status.HTTP_409_CONFLICT
        return peers
    if nome in peers:
        response.status_code = status.HTTP_409_CONFLICT
        return peers

    peers[id] = {"id": id, "nome": nome, "url": url}
    response.status_code = status.HTTP_200_OK
    return peers

@app.get('/peers/{id}', status_code=200)
def get_peers_id(id, response: Response):
    if id not in peers:
        response.status_code = status.HTTP_404_NOT_FOUND
    return peers

@app.put('/peers/{id}',status_code=200)
def put_peers_id(id: str, url: str, response: Response):
    if id not in peers:
        response.status_code = status.HTTP_404_NOT_FOUND
        return peers

    setattr(peers[id], "url", url)

    return peers[id]

@app.delete('/peers/{id}', status_code=200)
def delete_peers_id(id: str, response: Response):
    if id not in peers:
        response.status_code = status.HTTP_404_NOT_FOUND
        return peers
    del peers[id]
    return peers


def main():
    config = Config(app=app, host='0.0.0.0', port=int(PORT), debug=True)
    server = Server(config=config)
    server.run()


if __name__ == '__main__':
    main()