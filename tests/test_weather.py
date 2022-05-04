from tests.constants import City, Temperature
from weather.constants import IO
from weather.weather import get_weather_for_city


def test_get_weather_from_request(good_requests_mock):
    weather = get_weather_for_city(City.not_from_cache.value)
    assert weather == f'{Temperature.from_request}°'


def test_get_cached_weather(good_requests_mock):
    weather = get_weather_for_city(City.from_cache.value)
    assert weather == f'{Temperature.from_cache}°'


def test_cant_get_weather_from_bad_request(bad_requests_mock):
    weather = get_weather_for_city(City.not_exist.value)
    assert weather == IO.didnt_find_weather.value
