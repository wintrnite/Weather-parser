from datetime import datetime

import pytest
from requests import codes

from tests.constants import Temperature


@pytest.fixture()
def good_requests_mock(mocker):
    req_mock = mocker.patch('requests.get')
    req_mock.return_value.content = (
        f'<div id="weather-now-number">{Temperature.from_request}<span>°</span></div>'
    )
    req_mock.return_value.status_code = codes['OK']
    return req_mock


@pytest.fixture()
def bad_requests_mock(mocker):
    req_mock = mocker.patch('requests.get')
    req_mock.return_value.status_code = codes['not_found']
    return req_mock


@pytest.fixture(autouse=True)
def load_cache_mock(mocker):
    cache_mock = mocker.patch('pickle.load')
    cache_mock.return_value = {
        'moscow': {'temperature': f'{Temperature.from_cache}°', 'time': datetime.now()}
    }
    return cache_mock
