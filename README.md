⚠️ INFORMAÇÃO IMPORTANTE
ESSE PROJETO SÓ FUNCIONA SE OS EQUIPAMENTOS EXEBIREM O TEMPO OFFLINE
Quero mostrar um projeto que estou fazendo com o objetivo de ajudar os #provedores a fazer a remoção de ONU inativas na rede.
Como sabemos, alguns processos no dia a dia podem não ser feitos corretamente ou até mesmo a comunicação entre os setores pode falhar, e acaba que as ONUs não sejam removidas dos equipamentos — gerando transtornos, tanto quando são reutilizadas quanto para identificar eventos na rede GPON.

🔄 Projeto em versão beta
Esse projeto atualmente está na versão beta, utilizando uma Base de dados em Excel e arquivos .log, com a seguinte estrutura:

📁 Pasta backup_OLT
Armazena todos os dados recolhidos da OLT, gerando um arquivo com o IP, DATA, HORA
Exemplo:

<img width="501" height="49" alt="image" src="https://github.com/user-attachments/assets/bb1d0fae-61f8-4bd0-9cbe-d078778ce229" />
📁 Pasta Excel
Armazena os dados Excel do projeto
Exemplo:

<img width="457" height="156" alt="image" src="https://github.com/user-attachments/assets/fcddcb2b-c45c-4b74-9e16-52d69f31201b" />
📁 Pasta File_log
Armazena os arquivos .log do projeto
Exemplo:

<img width="457" height="131" alt="image" src="https://github.com/user-attachments/assets/3dfce40a-4a1e-4478-b892-f05e2b4d2f0d" />
📄 Arquivos principais do projeto
excel.py = Fica armazenado todos os dados de criação e manipulação dos dados do projeto (o Excel será removido no futuro)

ssh.py = Tem todos os comandos para pegar as informações da OLT

paths.py = Ficam as rotas dos arquivos do projeto, como .log e excel

Exemplo:

<img width="1275" height="681" alt="image" src="https://github.com/user-attachments/assets/903c15cd-2478-409d-925c-c09361297cfb" />
⚙️ Instalação das dependências
Para o projeto funcionar é necessário instalar as dependências que estão no arquivo requirements.txt
Exemplo:

<img width="388" height="307" alt="image" src="https://github.com/user-attachments/assets/5d648114-f196-4f6a-b076-7f91695e4005" />
🔧 Ajustes necessários
📌 Dados da OLT (arquivo ssh.py)
Esses campos precisam ser alterados para adicionar os dados da OLT DATACOM

Exemplo:

<img width="564" height="284" alt="image" src="https://github.com/user-attachments/assets/a26d623e-7b74-4fb3-9750-3fed8d873964" />
📌 ONUs de redes parceiras (arquivo excel.py)
Caso a rede tenha equipamentos de redes parceiras e as ONUs tenham nomes como, por exemplo, 001234_TESTENET, é necessário colocar nesse campo abaixo para não remover os clientes da rede parceira.
Porém, esses equipamentos estarão no Excel para informar a rede parceira.

Exemplo:

<img width="1597" height="341" alt="image" src="https://github.com/user-attachments/assets/40fabb60-16f1-45d4-92f6-deace20f13c6" />
