from app.utils import URLExistsError, URLNotFoundError
from pytest import mark


@mark.parametrize('data',
                  [
                      {'long': 'long'},
                      {'long': 'youtube', 'short': 'you'},
                      {'short': 'goo.gl'},
                  ]
                  )
def test_index(client, app, captured_templates, data):
    with app.app_context():
        resp = client.get('/')
        assert resp.status_code == 200
        resp = client.post('/', data=data)
        assert resp.status_code == 200
        template, context = captured_templates[1]
        assert template.name == "index.html"


@mark.parametrize('data, error',
                  [
                      ({'long': 'https://www.google.com/',
                       'short': 'goo.gl'}, URLExistsError()),
                      ({'short': 'tube'}, URLNotFoundError()),
                  ]
                  )
def test_index_raise(client, app, captured_templates,
                      data, error
                     ):
    with app.app_context():
        resp = client.post('/', data=data)
        assert resp.status_code == 400
        template, context = captured_templates[0]
        assert template.name == "error.html"
        assert error.message in str(context['message'])


def test_index_show_message(app, client):
    with app.app_context():
        resp = client.post('/', data={'long': '', 'short': ''})
        assert resp.status_code == 200
        assert b'At least one field should be filled.' in resp.data


def test_redirect(app, client):
    with app.app_context():
        resp = client.get('/goo.gl')
        assert resp.status_code == 302
        resp = client.get('/abc')
        assert resp.status_code == 404
