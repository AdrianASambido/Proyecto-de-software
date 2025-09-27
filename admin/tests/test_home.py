from src.web import create_app


app = create_app(env="testing")
app.testing = True
client = app.test_client()


def test_home():
    response = client.get("/")
    assert response.status_code == 200
