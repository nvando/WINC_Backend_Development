import pytest

from main import app

# The test client makes requests to the application
# without running a live server:
# the test client runs the app without the need of a networking layer.
@pytest.fixture
def client():
    client = app.test_client()  # test variant van command run
    return client


def test_redirect(client):
    response = client.get("/home")
    assert response.status_code == 302
    assert response.location == "http://localhost/"


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Index</title>" in response.data
    # b for byte string, as response data is raw bytes, otherwise use:
    # assert "<title>Index</title>" in response.get_data(as_text=True)


def test_about(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"<title>About</title>" in response.data


def test_contact(client):
    response = client.get("contact")
    assert response.status_code == 200
    assert b"<title>Contact</title>" in response.data
