⚠️ INFORMAÇÃO IMPORTANTE
ESSE PROJETO SÓ FUNCIONA SE OS EQUIPAMENTOS EXEBIREM O TEMPO OFFLINE
Quero mostrar um projeto que estou fazendo com o objetivo de ajudar os #provedores a fazer a remoção de ONU inativas na rede.
Como sabemos, alguns processos no dia a dia podem não ser feitos corretamente ou até mesmo a comunicação entre os setores pode falhar, e acaba que as ONUs não sejam removidas dos equipamentos — gerando transtornos, tanto quando são reutilizadas quanto para identificar eventos na rede GPON.

🔄 Projeto em versão beta
Esse projeto atualmente está na versão beta, utilizando uma Base de dados em Excel e arquivos .log, com a seguinte estrutura:

📁 Pasta backup_OLT
Armazena todos os dados recolhidos da OLT, gerando um arquivo com o IP, DATA, HORA
Exemplo:

<img width="500" height="51" alt="image" src="https://github.com/user-attachments/assets/9095fdbe-59e0-4f06-9488-d2da0823057b" />


📁 Pasta Excel
Armazena os dados Excel do projeto
Exemplo:

<img width="523" height="161" alt="image" src="https://github.com/user-attachments/assets/ec522c5b-7535-4948-84fd-1d369a4d0dbc" />

📁 Pasta File_log
Armazena os arquivos .log do projeto
Exemplo:

<img width="510" height="133" alt="image" src="https://github.com/user-attachments/assets/1ec7a9c4-fe1f-42b7-97eb-ab07e62553d6" />

📄 Arquivos principais do projeto
excel.py = Fica armazenado todos os dados de criação e manipulação dos dados do projeto (o Excel será removido no futuro)

ssh.py = Tem todos os comandos para pegar as informações da OLT

paths.py = Ficam as rotas dos arquivos do projeto, como .log e excel

Exemplo:

<img width="1194" height="654" alt="image" src="https://github.com/user-attachments/assets/327b2a9b-14ee-47c1-928f-4db3fe9fb531" />

⚙️ Instalação das dependências
Para o projeto funcionar é necessário instalar as dependências que estão no arquivo requirements.txt
Exemplo:

<img width="388" height="307" alt="image" src="https://github.com/user-attachments/assets/5d648114-f196-4f6a-b076-7f91695e4005" />

🔧 Ajustes necessários
📌 Dados da OLT (arquivo ssh.py)
Esses campos precisam ser alterados para adicionar os dados da OLT DATACOM

Exemplo:

<img width="386" height="340" alt="image" src="https://github.com/user-attachments/assets/1e52d43d-cbea-4694-b18a-ea7f935da940" />

📌 ONUs de redes parceiras (arquivo excel.py)
Caso a rede tenha equipamentos de redes parceiras e as ONUs tenham nomes como, por exemplo, 001234_TESTENET, é necessário colocar nesse campo abaixo para não remover os clientes da rede parceira.
Porém, esses equipamentos estarão no Excel para informar a rede parceira.

Exemplo:

<img width="1387" height="351" alt="image" src="https://github.com/user-attachments/assets/55101053-7f5c-4d91-84a7-4a97ff732923" />

