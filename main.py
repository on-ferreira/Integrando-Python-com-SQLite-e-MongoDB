import sqlalchemy
from sqlalchemy import Column, Integer, String, create_engine, inspect, select, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base, Session

Base = declarative_base()


class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True)
    cpf = Column(Integer, unique=True)
    name = Column(String)
    address = Column(String)  # Para fins didáticos endereço será tratado como campo simples

    account = relationship("Account", back_populates="client", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, cpf={self.cpf}, name={self.name}, address={self.address})"


class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    type = Column(String)
    ag = Column(String)  # Seguindo os padrões dados, mesmo agência sendo melhor representada como uma outra classe
    num = Column(Integer, unique=True)
    balance = Column(Float)
    id_cliente = Column(Integer, ForeignKey("client.id"), nullable=False)

    client = relationship("Client", back_populates="account")

    def __repr__(self):
        return f"Account(id={self.id}, type={self.type}, ag={self.ag}, num={self.num}, balance={self.balance})"


# conexão com o banco de dados
engine = create_engine("sqlite://")

# criando as classes como tabela no banco de dados
Base.metadata.create_all(engine)

# Conferindo o esquema do banco de dados
inspetor_engine = inspect(engine)
print(inspetor_engine.get_table_names())

with Session(engine) as session:
    fulano = Client(
        name="Fulano",
        cpf="12345678910",
        address="Rua um, numero um"
    )

    beltrano = Client(
        name="Beltrano",
        cpf="98765432100",
        address="Travessa da rua, complemento"
    )

    ciclano = Client(
        name="Ciclano",
        cpf="58294812300",
        address="Avenida Nida km x"
    )

    # Persistindo os dados
    session.add_all([fulano, beltrano, ciclano])

    session.commit()

# SELECT * FROM CLIENT WHERE NAME IN ('Fulano', 'Beltrano');
stmt = select(Client).where(Client.name.in_(["Fulano", "Beltrano"]))
for user in session.scalars(stmt):
    print(user)
