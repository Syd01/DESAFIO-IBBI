# DESAFIO-IBBI
DESAFIO-ALLAN EDUARDO

READ.ME
NESSE PROJETO VAMOS PRECISAR PRIMEIRO ORGANIZAR SEU AMBIENTE DE TRABALHO:
## Requisitos

- Python 3.7+
- Servidor MySQL
- FastAPI
- SQLAlchemy
- Pydantic
- Passlib
- jose
- mysql-connector-python
Baixe:
MySQL no link : https://dev.mysql.com/downloads/installer/ (escolha a versão compativel com seu windows)
NodeJS https://nodejs.org/en/download/package-manager (escolha a versão compativel com seu winsdows)
Pycham no link: https://www.jetbrains.com/pycharm/download/?section=windows (escolha a versão compativel com seu windows)
________________ANGULAR_____________________________
No terminal da sua IDE executar a instalaçao 
npm install -g @angular/cli@16
npm i (instalar as dependencias)
para ativar o server
ng serve.




Dica:
MySQL Comunity https://dev.mysql.com/downloads/mysql/ Eu sempre uso para evitar algum erro com o banco de dados(Baixe caso precise).
Para fazer testes precisos durante o processo, baixe tambem o POSTMAN link https://www.postman.com/downloads/
Você vai poder testar seus gets ,posts, deletes.

APOS INSTALADOS TODOS OS PROGRAMAS NECESSARIOS PARA ESSA ETAPA VAMOS COMEÇAR:
--Abra o MySQL workbench e crie "servidor" de banco de dados (no qual você vai conectar seu projeto para com o banco de dados).
	Dentro desse servidor você vai criar um banco de dados, vamos chamar de "restaurante".
	É importante lembrar de anotar a senha, o login vamos deixar padrao "root".
--Abra o Pycharm(Vamos utilizar os arquivos ja criados "main.py" e "test_main.http") e dentro do terminal de comandos você precisa rodas alguns comandos:
	pip install fastapi: Framework para construir APIs rápidas e eficientes.
	pip install "uvicorn[standard]": Servidor ASGI para executar aplicativos assíncronos como FastAPI.
	pip install mysql-connector-python: Driver para conectar e interagir com bancos de dados MySQL.
	pip install pydantic: Biblioteca para validação de dados e configuração, usada para definir e validar dados de forma eficiente.
	pip install SQLAlchemy: ORM para mapear classes Python a tabelas de banco de dados e facilitar operações de banco de dados.
	pip install python-jose  é uma biblioteca para Assinatura e Criptografia de Objetos JavaScript (JOSE), usada para lidar com JWTs (JSON Web Tokens) e outras tarefas semelhantes em Python.

	

AGORA VAMOS CRIAR UMA CONECÇAO COM NOSSO BANCO DE DADOS:

	SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:251292@localhost/restaurante"

	engine = create_engine(SQLALCHEMY_DATABASE_URL)
	SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

	Base = declarative_base()

 Nesse trecho do codigo usando o SQLAlchemy vamos conetar nossa aplicação com o banco de dados "restaurante".
....................PRONTO!.....................
AGORA COM A CONECÇÃO CRIADA VAMOS DAR OS COMANDOS PARA QUE O ATRAVEZ DO NOSSO CODIGO SEJA CRIADO UMA ESTRUTURA DO BANCO DE DADOS, COM COLUNAS E SUAS ESPECIFICAÇOES.
	Nosso projeto vai ser um restaurante online, portanto vamos começar criando os pratos, lembrando que o desafio exige algumas especificaçoes, nesse momento vamos precisar leva-las em consideração.

 class Pratos(Base):
		__tablename__ = "pratos"

		idpratos = Column(Integer, primary_key=True, index=True)
		nome_prato = Column(String(255), index=True)
		img_prato = Column(String(255))
		valor_prato = Column(Float)
		qtd_prato = Column(Integer)
		tipo_id = Column(Integer)
	
VAMOS REPETIR ESSE PROCESSO PARA O "TIPO" DE PRATO E PARA O "LOGIN", ONDE VAMAMOS GUARDAR OS DADOS DO NOSSO RESTAURANTE.


 class Login(Base):
    __tablename__ = "login"
	
		idlogin = Column(Integer, primary_key=True, index=True)
		login_usuario = Column(String(255), index=True)
		senha_usuario = Column(String(255), index=True)


APOS CRIAMOS OS CODIGO CORRETO É PRECISO DAR A INSTRUÇÃO PARA QUE SEJA LEVADO ESSA INFORMAÇAO ATE O BANCO DE DADOS, PRA ISSO VAMOS UTILIZAR:


 Base.metadata.create_all(bind=engine)
 
 
	Usando a "bind=egine" estamos utilizando o sqlalchemy para gerar as linhas de comando necessarias para
 criar automaticamente as colunas dentro do banco de dados.
	Click em rodar "Run" e verifique no seu banco de dados se as collunas foram inseridas, caso não estejam adicionadas, volte pro começo e refaça tudo novamente.
	
AGORA VAMOS COMEÇAR A TRABALHAR NOS ENDS POINTS, ANTES DE CONTINUARMOS CRIANDO O BASE MODEL.
 Vamos no "test_main.http", ao abrir esse arquivo (localizado abaixo do arquivo main.py, á esquerda do seu codigo), você vai achar uma linha escrita:
	GET http://127.0.0.1:8000/
	ccept: application/json
 Essa linha de codigo cria um endpoint no seu navegador, com isso você consegue visualizar os dados inseridos, no caso acima esta apenas o servidor,pra visualizarmos nosso  banco de dados é muito simples!
 Apos a barra "/" coloque a rota que deseja acessar utilizando o metodo "GET", no caso temos 3 rotas, 
 /pratos,/tipos,/login com isso você pode acessar as informaçoes existentes.
 
 O codigo deve ficar dessa forma:
 ###PRATOS
	GET http://127.0.0.1:8000/pratos/
	Accept: application/json
 ###TIPO	
	GET http://127.0.0.1:8000/tipo/
	Accept: application/json
###LOGIN
	GET http://127.0.0.1:8000/login/
	Accept: application/json
------------------------------TESTANDO A API------------------------------------------
PRONTO! AGORA VOLTE AO "MAIN.PY" e crie sessao e uma  uma instancia usando o FasAPI:
 Utilize o codigo:
 def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

 Para criar uma sessao e fechar, depois:

 app = FastAPI()
	Depois defina um endpoint
	@app.get("/pratos/")
	async def read_pratos(db: Session = Depends(get_db)):
    return db.query(Prato).all()
	
 Pronto, para concluirmos o teste precisamos ir no banco de dados (MySQL) na tabela pratos, e adicionar os dados nas colunas.(LEMBRANDO QUE ISSO É APENAS UM TESTE, PARA SABER SE O CODIGO ESTA FUNCIONANDO COMO DEVERIA)

 Assim que inserir os dados necessarios volte ao Pycharm e click em "RUN", abra o navegador e coloque o link do seu banco de dados,"http://127.0.0.1:8000/pratos/". Nesse momento deve retornar os dados do prato adicionado, caso contrario volte e refaça.
 
 
------------------------------------------------------------------------------------------------------------------
AGORA QUE SABEMOS QUE O NOSSE CODIGO ESTA FUNCIOANDO E CONECTADO COM O BANCO DE DADOS, VAMOS INTRODUZIR INFORMAÇOES ATRAVEZ DO METODO "POST".
 Pra isso é bem simples, primeiro vou criar uma classe para definir o modelo de entrada de dados:
 
 class CriarPrato(BaseModel):
    nomeclatura: constr(max_length=255)
    imagem: constr(max_length=255)
    valor: float
    qtd: int
    tipoid: int
	
 É preciso definir as propriedades de cada item para evitar conflitos. Ássim que temos um metodo de entrada precisamos definir um medoto de retorno (Como vamos querer que seja respondido nosso input).
 
 class RespostaPrato(BaseModel):
    idpratos: int
    nome_prato: str
    img_prato: str
    valor_prato: float
    qtd_prato: int
    tipo_id: int
	
 class Config:
    orm_mode = True

 Em "RespostaPrato" usei os mesmos nomes das colunas do bd. Na primeira vez que rodei o codigo, funcionou normalmente, porem na quando fui adicionando outras funcionalidades deu um erro, um alerta dizendo que nao estava conseguindo importa o BaseModel, aparentemente estava em outra versao, refiz o codigo de varias formas, reinstalei mas nao deu jeito, entao pesquisei e achei uma linha pra forçar(converter) essa  classe pra orm_mode, foi quando voltou a funcionar.
 Para finalizar essa etepa precisamos da funçao get_db, como no teste anterior:
 


 def get_db():
     db = SessionLocal()
     try:
        yield db
     finally:
        db.close()
		
 Tambem vamos precisar criar as funçoes do end point, nesse casso vamos fazer todos de uma vez só para ser mai eficiente. GET,POST E DELETE.
 
 (A PARTIR DESSE PONTO TODOS OS TESTES ESTÃO SENDO CONDUZIDOS NO POSTMAN, UTILIZANDO OS METODOS DESEJADOS)
 
 #Endpoint para buscar uma lista de pratos, foi utilizado "response_model=List" com essa finalidade.
 

 app = FastAPI()---Use antes dos endpoints para definir 
 
 
 @app.get("/pratos/", response_model=List[RespostaPrato])
async def read_pratos(db: Session = Depends(get_db)):
    return db.query(Pratos).all()

@app.post("/pratos/", response_model=RespostaPrato)
async def create_prato(prato: CriarPrato, db: Session = Depends(get_db)):
    db_prato = Pratos(
        nome_prato=prato.nomeclatura,
        img_prato=prato.imagem,
        valor_prato=prato.valor,
        qtd_prato=prato.qtd,
        tipo_id=prato.tipoid
    )
    db.add(db_prato)
    db.commit()
    db.refresh(db_prato)
    return db_prato

 #Use sempre ID para deletar.
@app.delete("/pratos/{id}")
async def delete_pratos(id: int, db: SessionLocal = Depends(get_db)):
    prato = db.query(Pratos).filter(Pratos.idpratos == id).first()
    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")
    db.delete(prato)
    db.commit()
    return {"Prato deletado com sucesso!"}
 
 É NECESSARIO ADICIONAR OS ENDPOINTS NO ARQUIVO "teste.main.http".
	GET http://127.0.0.1:8000/login/
	 Accept: application/json

###VALIDAÇAOPOSTprato
	POST http://127.0.0.1:8000/pratos/
	 Accept: application/json

###DELETEprato
	DELETE http://127.0.0.1:8000/pratos/id
	 Accept: application/json
	 
------------------------PRONTO---------------------------
 Agora para testar basta abrir o POSTMAN no selecionar o metodo que deseja utilizar e fazer os testes, selecione JSON para respostas:
	No metodo get ira retornar todo os prato em forma de lista.
	No metodo post você precisa adicionar os dados no modelo que foi criado no codigo:
	Ex:
	 {
	 "nomeclatura": "pão",
      "imagem": "url_da_imagem_001",
      "valor": 33.99,
      "qtd": 2,
      "tipoid": 1
	 }
	
	Ele vai retornar uma lista de acordo com a lista com a [RespostaPrato] trazendo o ID, ex:
	 {
    "idpratos": 1,
    "nome_prato": "pão",
    "img_prato": "url_da_imagem_001",
    "valor_prato": 33.99,
    "qtd_prato": 2,
    "tipo_id": 1
}
	
	No metodo delete deve-se substituir {id} pelo id que deseja deletar do banco de dados.
	Ex:
	http://127.0.0.1:8000/pratos/1
	
	Ele vai retornar a resposta pre setada na funçao delete, "Prato deletado com sucesso!"
	Você pode verificar diretamente no banco de dados todas essas alterações.
_____________________________________________________________________________________________________________________
	
Endpoints
Home
Método: GET
URL: http://127.0.0.1:8000/
Aceita: application/json
Descrição: Endpoint principal para verificar se a API está ativa.

PRATOS
Listar Pratos
Método: GET
URL: http://127.0.0.1:8000/pratos/
Aceita: application/json
Descrição: Retorna a lista de todos os pratos cadastrados.

Cadastrar Prato
Método: POST
URL: http://127.0.0.1:8000/pratos/
Aceita: application/json
Descrição: Endpoint para cadastrar um novo prato.

Deletar Prato
Método: DELETE
URL: http://127.0.0.1:8000/pratos/{id}
Aceita: application/json
Descrição: Endpoint para deletar um prato pelo seu ID.

Comprar Prato
Método: PUT
URL: http://127.0.0.1:8000/prato_compra/{id}
Aceita: application/json
Descrição: Endpoint para registrar a compra de um prato pelo seu ID.

TIPOS
Listar Tipos
Método: GET
URL: http://127.0.0.1:8000/tipos/
Aceita: application/json
Descrição: Retorna a lista de todos os tipos de pratos cadastrados.

Cadastrar Tipo
Método: POST
URL: http://127.0.0.1:8000/tipos/
Aceita: application/json
Descrição: Endpoint para cadastrar um novo tipo de prato.

LOGIN
Realizar Login
Método: POST
URL: http://127.0.0.1:8000/login/
Aceita: application/json
Descrição: Endpoint para realizar login e obter token de autenticação.

Validar Login
Método: GET
URL: http://127.0.0.1:8000/logar/{nome}/{senha}
Aceita: application/json
Descrição: Endpoint para validar login com nome de usuário e senha.

VALIDAÇÃO
Validar Token
Método: POST
URL: http://127.0.0.1:8000/token/
Aceita: application/json
Descrição: Endpoint para validar o token de autenticação.

Validar Prato
Método: POST
URL: http://127.0.0.1:8000/validador/
Aceita: application/json
Descrição: Endpoint para validar as informações de um prato.

