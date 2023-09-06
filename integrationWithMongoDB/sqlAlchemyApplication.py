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
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)

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

    acc1 = Account(
        type="Corrente",
        ag="0001",
        num="1",
        balance="100",
        client_id=1
    )

    acc2 = Account(
        type="Poupança",
        ag="0001",
        num="2",
        balance="0",
        client_id=1
    )

    acc3 = Account(
        type="Corrente",
        ag="0001",
        num="11",
        balance="1000",
        client_id=2
    )

    acc4 = Account(
        type="Corrente",
        ag="0001",
        num="15",
        balance="2000",
        client_id=3
    )

    # Persistindo os dados
    session.add_all([fulano, beltrano, ciclano, acc1, acc2, acc3, acc4])

    session.commit()

print("""
SELECT * 
FROM CLIENT 
WHERE NAME IN ('Fulano', 'Beltrano');
""")
stmt = select(Client).where(Client.name.in_(["Fulano", "Ciclano"]))
for user in session.scalars(stmt):
    print(user)

print("""
SELECT *
FROM Account
ORDER BY balance DESC;
""")
stmt_order = select(Account).order_by(Account.balance.desc())
for result in session.scalars(stmt_order):
    print(result)

stmt_join = select(Client, Account).join_from(Client, Account)
print("""
SELECT *
FROM Client
INNER JOIN Account ON Client.id = Account.client_id;
""")
for result in session.scalars(stmt_join):
    print(result)

session.close()
