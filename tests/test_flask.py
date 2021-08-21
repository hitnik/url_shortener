from test_main import get_short_url
from test_db import script, manager_mock
from app.db import get_db

def test_index(client, app, db_mock, captured_templates):
    print(app.config['DATABASE'])
    with app.app_context():
        resp = client.get('/')
        assert resp.status_code == 200
        db_mock.executescript(script)
        with manager_mock(db_mock, 'db.get_db', 'db.db_manager'):
            resp = client.post('/', data={'long': 'long'})
            assert resp.status_code == 200
            template, context = captured_templates[1]
            assert template.name == "index.html"
            assert "long" in context.values()        
            assert context['short'] == get_short_url('long')
            resp = client.post('/', data={'long':'https://www.google.com/', 'short':'goo.gl'})
            assert resp.status_code == 400
            template, context = captured_templates[2]
            assert template.name == "400.html"
