# BoilerPlate de um WebService utilizando FastApi
> projeto de um webservice em FastApi

[![Python Version][python-image]][python-url]
[![FastApi][fastapi-image]][fastApi-url]
![Coverage][coverage-image]

Criado em Python na versão 3.12 junto ao framework FastApi.
## Pacotes

Segue a lista de pacotes utilizados no projeto.

Package                                      | Version  |
---------------------------------------------| ---------|
[FastApi][fastApi-url]                       | 0.109.2  |
[Uvicorn][uvicorn-url]                       | 0.27.1   |
[Pydantic][pydantic-url]                     | 2.6.1    |


## Instalação:

### Etapas para uso em desenvolvimento:
1. <b>(Optional)</b> Você pode rodar os comandos abaixo para subir o projeto via docker:
```sh
docker compose up --build
```
2. Ou localmente com seu ambiente python, instale a lista de pacotes.
```sh
pip install -r requeriments-dev.txt
```
3. Após isso utilize o comando:
```sh
uvicorn app.main:app
OU
make runserver
```
4. Com isso o projeto já estará funcionando.

## Exemplo de uso:
Ao subir o Projeto podemos ir no endpoint raiz que nós apresentará o swagger do projeto
Ele contem os endpoints que podem ser acessados no projeto.

Podemos utiliza-lo para fazermos os testes no projeto, ou apenas para pegar os valores
de referencia para utilização em um

Ambiente deployado: https://python-challenge-cc8a30335966.herokuapp.com/

Exemplo dos endpoints:
```sh
/api/v1/words/sort :: para retorno das palavras ordenado
/api/v1/words/vowel_count :: para contagem das vogais das palavras passadas.
```

<!-- Markdown link & img dfn's -->
[python-image]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://www.python.org/
[fastApi-image]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[fastApi-url]: https://fastapi.tiangolo.com/
[uvicorn-url]: https://www.uvicorn.org/
[pydantic-url]: https://docs.pydantic.dev/latest/
[fastapi-image]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[coverage-image]: https://coverage-badge.samuelcolvin.workers.dev/tiangolo/fastapi.svg
