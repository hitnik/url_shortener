from flask import url_for
from test_main import get_short_url

def test_index(client,app, captured_templates):
    with app.app_context():
        resp = client.get(url_for('index'))
        assert resp.status_code == 200
        resp = client.post('/', data={'long': 'long'})
        assert resp.status_code == 200
        template, context = captured_templates[1]
        assert template.name == "index.html"
        assert "long" in context['context'].values()
        assert context["context"]['short'] == get_short_url('long')