
import pytest
from GippuMainController import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_start_printing(client):
    response = client.post('/start_printing')
    assert response.json['status'] == 'started'
    assert response.status_code == 200

def test_stop_printing(client):
    response = client.post('/stop_printing')
    assert response.json['status'] == 'stopped'
    assert response.status_code == 200

def test_index(client):
    response = client.get('/')
    assert b"Start Printing" in response.data
    assert b"Stop Printing" in response.data
    assert response.status_code == 200

if __name__ == '__main__':
    pytest.main()
