import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

DATABASE_URL = "mysql+mysqlconnector://root:root@localhost/banks_db"

Base = declarative_base()

class Bank(Base):
    __tablename__ = 'banks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ispb = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(Integer, nullable=True)
    full_name = Column(String(255), nullable=False)

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return engine

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data_from_api(api_url):
    """Extrai dados da API e retorna uma lista de dicionários."""
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

@task
def transform_data(data):
    """Transforma os dados para o formato adequado ao modelo do banco de dados."""
    transformed_data = []
    for item in data:
        if item['code'] != None:
            transformed_data.append({
                "ispb": item["ispb"],
                "name": item["name"],
                "code": item.get("code"),
                "full_name": item["fullName"]
            })
    return transformed_data

@task
def load_data_to_mysql(data, session=None):
    """Carrega os dados transformados no banco de dados."""
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = session or Session()

    try:
        for item in data:
            bank = Bank(
                ispb=item["ispb"],
                name=item["name"],
                code=item["code"],
                full_name=item["full_name"]
            )
            session.add(bank)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


@flow
def etl_pipeline(api_url):
    """Pipeline completa de ETL usando Prefect."""
    print("Iniciando pipeline de ETL...")
    raw_data = extract_data_from_api(api_url)
    transformed_data = transform_data(raw_data)
    load_data_to_mysql(transformed_data)
    print("Pipeline concluída com sucesso!")

if __name__ == "__main__":
    API_URL = "https://brasilapi.com.br/api/banks/v1"
    etl_pipeline(API_URL)
