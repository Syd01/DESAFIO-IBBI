from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, constr
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
from typing import Optional, List


# Database configuration
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:251292@localhost/restaurante"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Security configuration
SECRET_KEY = "123456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# Models
class Login(Base):
    __tablename__ = "login"

    idlogin = Column(Integer, primary_key=True, index=True)
    login_usuario = Column(String(255), index=True)
    senha_usuario = Column(String(255), index=True)


class Pratos(Base):
    __tablename__ = "pratos"
    idpratos = Column(Integer, primary_key=True, index=True)
    nome_prato = Column(String(255), index=True)
    img_prato = Column(String(255))
    valor_prato = Column(Float)
    qtd_prato = Column(Integer)
    tipo_id = Column(Integer)
    idlogin = Column(Integer)

class Tipos(Base):
    __tablename__ = "tipo"

    idtipo = Column(Integer, primary_key=True, index=True)
    descricao_prato = Column(String(255), index=True)



class Validador(Base):
    __tablename__ = "validador"
    idvalidador = Column(Integer, primary_key=True, index=True)
    login_validador = Column(String(255), unique=True, index=True)
    senha_hash = Column(String(255))

Base.metadata.create_all(bind=engine)

# Pydantic Schemas



class CriarLogin(BaseModel):
    login: str
    senha: str

class CriarValidador(BaseModel):
    login: str
    senha: str

class CriarPrato(BaseModel):
    nomeclatura: constr(max_length=255)
    imagem: constr(max_length=255)
    valor: float
    qtd: int
    tipoid: int
    idlogin:int

class PratoUpdateCompra(BaseModel):
    quantidade: int

class RespostaPrato(BaseModel):
    idpratos: int
    nome_prato: str
    img_prato: str
    valor_prato: float
    qtd_prato: int
    tipo_id: int

class CriarTipos(BaseModel):
    descricao: str

class Config:
    orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_validador(db, login_validador: str):
    return db.query(Validador).filter(Validador.login_validador == login_validador).first()

def authenticate_validador(db, login_validador: str, password: str):
    validador = get_validador(db, login_validador)
    if not validador or not verify_password(password, validador.senha_hash):
        return False
    return validador

async def get_current_validador(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login_validador: str = payload.get("sub")
        if login_validador is None:
            raise credentials_exception
        token_data = TokenData(username=login_validador)
    except JWTError:
        raise credentials_exception

    validador = get_validador(db, login_validador=login_validador)
    if validador is None:
        raise credentials_exception

    return validador

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # URL do seu frontend Angular durante o desenvolvimento
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Métodos HTTP permitidos
    allow_headers=["Authorization", "Content-Type"],  # Headers permitidos
)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    validador = authenticate_validador(db, form_data.username, form_data.password)
    if not validador:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": validador.login_validador}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/validador/")
async def create_validador(validador: CriarValidador, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(validador.senha)
    db_validador = Validador(
        login_validador=validador.login,
        senha_hash=hashed_password,
    )
    db.add(db_validador)
    db.commit()
    db.refresh(db_validador)
    return {"message": "Validador created successfully!"}

@app.get("/pratos/", response_model=List[RespostaPrato], dependencies=[Depends(get_current_validador)])
async def read_pratos(db: Session = Depends(get_db)):
    return db.query(Pratos).filter(Pratos.qtd_prato).all()

@app.post("/pratos/", response_model=RespostaPrato, dependencies=[Depends(get_current_validador)])
async def create_prato(prato: CriarPrato, db: Session = Depends(get_db)):
    db_prato = Pratos(
        nome_prato=prato.nomeclatura,
        img_prato=prato.imagem,
        valor_prato=prato.valor,
        qtd_prato=prato.qtd,
        tipo_id=prato.tipoid,
        idlogin=prato.idlogin
    )
    db.add(db_prato)
    db.commit()
    db.refresh(db_prato)
    return db_prato

@app.delete("/pratos/{id}", dependencies=[Depends(get_current_validador)])
async def delete_pratos(id: int, db: Session = Depends(get_db)):
    prato = db.query(Pratos).filter(Pratos.idpratos == id).first()
    if not prato:
        raise HTTPException(status_code=404, detail="Prato not found")
    db.delete(prato)
    db.commit()
    return {"message": "Prato deleted successfully!"}
# Endpoint para criar um novo produto (autenticado)

@app.post("/login/", dependencies=[Depends(get_current_validador)])
async def create_login(login: CriarLogin, db: SessionLocal = Depends(get_db)):
    db_login = Login(
        login_usuario=login.login,
        senha_usuario=login.senha
    )
    db.add(db_login)
    db.commit()
    db.refresh(db_login)
    return {"message": "login salvo com sucesso!"}


@app.get("/logar/{login}/{senha}", dependencies=[Depends(get_current_validador)])
async def read_login(login: str, senha: str, db: Session = Depends(get_db)):
    login_entry = db.query(Login).filter(Login.login_usuario == login, Login.senha_usuario == senha).first()
    if not login_entry:
        raise HTTPException(status_code=404, detail="Login não encontrado")
    #return login_entry
    return {"usuario": login_entry, "message": "Login realizado com sucesso"}

@app.post("/tipos/", dependencies=[Depends(get_current_validador)])
async def create_tipos(tipos: CriarTipos, db: SessionLocal = Depends(get_db)):
    db_tipos = Tipos(
        descricao_prato=tipos.descricao,

    )
    db.add(db_tipos)
    db.commit()
    db.refresh(db_tipos)
    return {"message": "Tipo salvo com sucesso!"}

@app.get("/tipos/", dependencies=[Depends(get_current_validador)])
async def read_tipos(db: Session = Depends(get_db)):
    tipos = db.query(Tipos).all()
    return tipos

@app.put("/prato_compra/{idpratos}", dependencies=[Depends(get_current_validador)])
async def update_produto(idpratos: int, prato: PratoUpdateCompra, db: SessionLocal = Depends(get_db)):
    print(f"Received data: {prato}")  # Adicione este log
    db_prato = db.query(Pratos).filter(Pratos.idpratos == idpratos).first()
    if not db_prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")

    if prato.quantidade > db_prato.qtd_prato:
        raise HTTPException(status_code=400, detail="Quantidade desejada não disponível")

    db_prato.qtd_prato -= prato.quantidade

    db.commit()
    db.refresh(db_prato)
    return {"message": "Produto Comprado com sucesso!"}
