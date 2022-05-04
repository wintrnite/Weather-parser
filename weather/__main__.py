import typer

from weather.weather import get_weather_for_city


def main(city: str = typer.Argument(...)) -> None:  # pragma: no cover (trivial code)
    typer.echo(f'Current weather in {city}: {get_weather_for_city(city)}')


if __name__ == '__main__':  # pragma: no cover (trivial code)
    typer.run(main)
