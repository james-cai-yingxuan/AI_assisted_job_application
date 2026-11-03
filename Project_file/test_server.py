import io
from unittest.mock import patch

from server import app


def test_home_serves_original_layout():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert b'AI-Assisted Job Application' in response.data
    assert b'Analyse My Fit' in response.data


def test_validation_missing_inputs():
    response = app.test_client().post('/api/analyse', data={})
    assert response.status_code == 400
    assert 'resume' in response.json['error'].lower()


def test_invalid_file_format():
    response = app.test_client().post('/api/analyse', data={
        'resume': (io.BytesIO(b'hello'), 'resume.exe'),
        'jobDescription': 'Business analyst'
    })
    assert response.status_code == 400
    assert 'PDF' in response.json['error']


def test_end_to_end_route_mocked_api():
    result = {
        'matchScore': 78,
        'strengths': ['Stakeholder management'],
        'gaps': ['SQL not demonstrated'],
        'resumeSuggestions': ['Clarify project outcomes if supported'],
        'coverLetter': 'Dear Hiring Manager, ...',
    }
    with patch('server.analyse_with_openai', return_value=result) as mock:
        response = app.test_client().post('/api/analyse', data={
            'resume': (io.BytesIO(b'Experienced in stakeholder management'), 'resume.txt'),
            'jobDescription': 'Seeking a BA with stakeholder management and SQL.',
        })
    assert response.status_code == 200
    assert response.json == result
    assert mock.call_args.args[0] == 'Experienced in stakeholder management'


def test_connection_requires_key():
    with patch.dict('os.environ', {'OPENAI_API_KEY': ''}):
        response = app.test_client().post('/api/test-connection')
    assert response.status_code == 503
    assert response.json['connected'] is False
