import pickle
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Callable

import requests
from bs4 import BeautifulSoup
from decouple import config

from weather.constants import IO


def cache(ttl: int = 5 * 60) -> Callable[[Callable[[str], str]], Callable[[str], str]]:
    def decorator(func: Callable[[str], str]) -> Callable[[str], str]:
        @wraps(func)
        def wrapper(city: str) -> str:
            cache_file_name = config('CACHE_FILE')
            if Path(cache_file_name).is_file():
                with Path(cache_file_name).open('rb') as handle:
                    results = pickle.load(handle)
                if (
                    city in results
                    and (datetime.now() - results[city]['time']).total_seconds() <= ttl
                ):
                    return results[city]['temperature']
            results = {}
            temperature = func(city)
            if temperature != IO.didnt_find_weather:
                results[city] = {'temperature': temperature, 'time': datetime.now()}
                with Path(cache_file_name).open('wb') as results_cache:
                    pickle.dump(results, results_cache, protocol=pickle.HIGHEST_PROTOCOL)
            return temperature

        return wrapper

    return decorator


@cache(ttl=5 * 60)
def get_weather_for_city(city: str) -> str:
    try:
        req = requests.get(f'{config("WEATHER_URL")}{city}')
        soup = BeautifulSoup(req.content, 'html.parser')
        return soup.find('div', {'id': 'weather-now-number'}).get_text()
    except Exception:  # кажется, здесь уместен общий Exception
        return IO.didnt_find_weather.value
