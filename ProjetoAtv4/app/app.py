import os
from types import resolve_bases
from fastapi import FastAPI, status, Response
from uvicorn import Config, Server
from pydantic import BaseModel
from time import sleep, time
import time
import uuid

PORT = os.environ.get('PORT')
app = FastAPI()

class Peer(BaseModel):
    id: str
    nome: str
    url: str

class Data(BaseModel):
    server_name: str
    server_endpoint: str
    descricao: str
    versao: str
    status: str
    tipo_de_eleicao_ativa: str

class gera_Recurso(BaseModel):
    codigo_acesso: str
    valor: int
    validade: int
        
data = Data(
    server_name = "Joao Pedro de Gois Pinto",
    server_endpoint = "https://sd-joaopedrop-20212.herokuapp.com/ ",
    descricao = "Projeto de SD. Os seguintes servicos estao implementados... "
    "GET/info, PUT/info/, GET/peers, POST/peers, GET/peers{id}, PUT/peers{id}, DELETE/peers{id}",
    versao = "0.1",
    status = "online",
    tipo_de_eleicao_ativa = "ring"
)

recurso = gera_Recurso(
    codigo_acesso = uuid.uuid4,
    valor = 1,
    validade = 0
)


@app.get('/info', status_code=200)
def info():

   return data

@app.put('/info', status_code=200)
def info(status: str, eleicao: str, response: Response):

    data.status = status

    data.tipo_de_eleicao_ativa = eleicao

    if status is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    if eleicao is None:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data

peers = [
    Peer(id="201720295", nome="Allana Dos Santos Campos", url="https://sd-ascampos-20212.herokuapp.com/"),
    Peer(id="201512136", nome="Annya Rita De Souza Ourives", url="https://sd-annyaourives-20212.herokuapp.com/hello"),
    Peer(id="201512137", nome="Daniel Andrade Penêdo Santos", url=""),
    Peer(id="201710375", nome="Emmanuel Norberto Ribeiro Dos Santos", url="https://sd-emmanuel.herokuapp.com/"),
    Peer(id="201420373", nome="Gabriel Figueiredo Góes", url=""),
    Peer(id="201710377", nome="Hiago Rios Cordeiro", url="https://sd-api-uesc.herokuapp.com/"),
    Peer(id="201810665", nome="Jenilson Ramos Santos", url="https://jenilsonramos-sd-20211.herokuapp.com/"),
    Peer(id="201610327", nome="Joao Pedro De Gois Pinto", url="https://sd-joaopedrop-20212.herokuapp.com/"),
    Peer(id="201610337", nome="Luis Carlos Santos Camara", url="https://sd-20212-luiscarlos.herokuapp.com/"),
    Peer(id="201620181", nome="Matheus Santos Rodrigues", url=""),
    Peer(id="201620400", nome="Nassim Maron Rihan", url="https://sd-nassimrihan-2021-2.herokuapp.com/"),
    Peer(id="201710396", nome="Robert Morais Santos Broketa", url="https://pratica-sd.herokuapp.com/"),
    Peer(id="201720308", nome="Victor Dos Santos Santana", url="https://sd-victor-20212.herokuapp.com/")
]

@app.get('/peers')
def get_peers():

    return peers

@app.post('/peers', status_code=200)
def post_peers(peer: Peer, response: Response ):
    for p in peers:
        if p.id == peer.id:
            response.status_code = status.HTTP_409_CONFLICT
            return response
        if p.nome == peer.nome:
            response.status_code = status.HTTP_409_CONFLICT
            return response

    if peer.nome.isdigit():
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response

    if not peer.url.startswith("http"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response

    if peer.id is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response

    if peer.nome is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response

    if peer.url is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response

    peers.append(peer)
    response.status_code = status.HTTP_200_OK
    return peers

@app.get('/peers/{id}', status_code=200)
def get_peers_id(id: str, response: Response):
    for p in peers:
        if p.id == id:
            return p

    response.status_code = status.HTTP_404_NOT_FOUND
    return response

@app.put('/peers/{id}',status_code=200)
def put_peers_id(peer: Peer, response: Response):
    for indice, p in enumerate(peers):
        if p.id == peer.id:
            peers[indice] = peer
            return peer

    response.status_code = status.HTTP_404_NOT_FOUND
    return response

@app.delete('/peers/{id}', status_code=200)
def delete_peers_id(id: str, response: Response):
    for indice, p in enumerate(peers):
        if p.id == id:
            del peers[indice]
            response.status_code = status.HTTP_200_OK
            return response

    response.status_code = status.HTTP_404_NOT_FOUND
    return response


@app.get('/recurso',status_code=200)
def get_recurso(codigo_usuario: str, response: Response):
    if(recurso.validade < int(time.time())):
        recurso.validade = 0
        response.status_code = status.HTTP_401_ACCESS_DENIED
        return response

    if (codigo_usuario == recurso.codigo_acesso):
        return recurso.valor

    response.status_code = status.HTTP_401_ACCESS_DENIED
    return response


@app.put('/recurso',status_code=200)
def put_recurso(codigo_usuario: str, valor: int, response: Response):
    if(recurso.validade < int(time.time())):
        recurso.validade = 0
        response.status_code = status.HTTP_401_ACCESS_DENIED
        return response

    if(codigo_usuario == recurso.codigo_acesso):
        recurso.valor = valor
        return response

    response.status_code = status.HTTP_401_ACCESS_DENIED
    return response


@app.post('/recurso',status_code=200)
def post_recurso(codigo_usuario: str, response: Response):
    if(codigo_usuario == recurso.codigo_acesso and recurso.validade == 0):

        recurso.validade = int(time.time()) + 5
        return response

    response.status_code = status.HTTP_409_CONFLICT
    return response

@app.delete('recurso',status_code=200)
def delete_recurso(codigo_usuario: str, response: Response):
    if(recurso.validade < int(time.time())):
        recurso.validade = 0
        response.status_code = status.HTTP_410_GONE
        return response

    if(codigo_usuario == recurso.codigo_acesso):    
        recurso.validade = 0
        return response

    response.status_code = status.HTTP_410_GONE
    return response



def main():
    config = Config(app=app, host='0.0.0.0', port=PORT, debug=True)
    server = Server(config=config)
    server.run()


if __name__ == '__main__':
    main()