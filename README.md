# WebServerSimulator

Atividade da disciplina TRABALHO INDIVIDUAL EM ENGENHARIA DE SOFTWARE.

O objetivo da atividade é simular um simples servidor que aceita requisições HTTP, GET e POST apenas.


## Instalação

Faça [download](https://github.com/Spoock01/WebServerSimulator)
ou clone o projeto:

```bash
git clone https://github.com/Spoock01/WebServerSimulator.git
```

## Como usar


No windows, execute o arquivo main.py
```bash
python main.py ou python3 main.py
```

No ubuntu, execute o arquivo main.py
```bash
python main.py ou python3 main.py ou ./main.py
```

## Como testar

O servidor aceita múltiplas requisições simultâneas(multithread).


Em algum navegador, para visualizar alguns status, utilize as seguintes rotas:


```
localhost:8081/index.html -> STATUS 200
localhost:8081/index3.html -> STATUS 404
```
Para testar o Virtual Hosting:

```
localhost:8081/site1/index.html -> Acessa o site1
localhost:8081/site2/index.html -> Acessa o site2
```


Para testar a autenticação:  
Usuário: edson,  
Senha: 12345678

```
localhost:8081/adm/index.html
```

Caso usuário ou senha não estejam certos:```STATUS 403```


Para visualizar o log do servidor, acesse a pasta Log contida no projeto e abra o arquivo ```Log-8081.txt```

#### Tipos de requisições suportadas

```
GET
POST
```

#### Lista de respostas suportadas

```
STATUS_200 = 'HTTP/1.0 200 OK'
STATUS_204 = 'HTTP/1.0 204 NO CONTENT'
STATUS_401 = 'HTTP/1.0 401 UNAUTHORIZED'
STATUS_403 = 'HTTP/1.0 403 FORBIDDEN'
STATUS_404 = 'HTTP/1.0 404 NOT FOUND'
STATUS_501 = 'HTTP/1.0 501 NOT IMPLEMENTED'
```

## Autores
Arthur Lopes  
Edson Alves  
João Vinícius  
Yure Galdino



## License
[MIT](https://choosealicense.com/licenses/mit/)
