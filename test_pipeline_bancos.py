import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pipeline import extract_data_from_api, transform_data, load_data_to_mysql, etl_pipeline, Bank, Base

@pytest.fixture
def test_engine():
    """Cria um banco de dados SQLite em memória para testes."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine) 
    return engine

@pytest.fixture
def test_session(test_engine):
    """Cria uma sessão SQLAlchemy para os testes."""
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.close()

def test_extract_data_from_api(mocker):
    """Teste para verificar a extração de dados da API."""
    mock_response = [
        {"ispb": "12345678", "name": "Banco Teste", "code": 999, "fullName": "Banco Teste Completo"}
    ]
    mocker.patch("pipeline.requests.get", return_value=MagicMock(json=lambda: mock_response, status_code=200))

    api_url = "https://fakeapi.com"
    data = extract_data_from_api(api_url)
    assert data == mock_response

def test_transform_data():
    """Teste para verificar a transformação dos dados."""
    raw_data = [
        {"ispb": "12345678", "name": "Banco Teste", "code": 999, "fullName": "Banco Teste Completo"}
    ]
    transformed_data = transform_data(raw_data)
    expected_data = [
        {"ispb": "12345678", "name": "Banco Teste", "code": 999, "full_name": "Banco Teste Completo"}
    ]
    assert transformed_data == expected_data

def test_load_data_to_mysql(test_session):
    """Teste para verificar o carregamento dos dados no banco."""
    data = [
        {"ispb": "12345678", "name": "Banco Teste", "code": 999, "full_name": "Banco Teste Completo"}
    ]
    load_data_to_mysql(data, session=test_session)

    results = test_session.query(Bank).all()
    assert len(results) == 1
    assert results[0].ispb == "12345678"
    assert results[0].name == "Banco Teste"
    assert results[0].code == 999
    assert results[0].full_name == "Banco Teste Completo"


@patch("pipeline.extract_data_from_api")
@patch("pipeline.transform_data")
@patch("pipeline.load_data_to_mysql")
def test_etl_pipeline(mock_load, mock_transform, mock_extract):
    """Teste para verificar a execução da pipeline completa."""
    mock_extract.return_value = [
        {"ispb": "12345678", "name": "Banco Teste", "code": 999, "fullName": "Banco Teste Completo"}
    ]
    mock_transform.return_value = [
        {"ispb": "12345678", "name": "Banco Teste", "code": 999, "full_name": "Banco Teste Completo"}
    ]

    etl_pipeline("https://fakeapi.com")

    mock_extract.assert_called_once_with("https://fakeapi.com")
    mock_transform.assert_called_once()
    mock_load.assert_called_once()
