import enum


class Temperature(enum.Enum):
    from_cache = '-9'
    from_request = '23'

    def __str__(self):
        return self.value


class City(enum.Enum):
    from_cache = 'moscow'
    not_from_cache = 'yekaterinburg'
    not_exist = 'london'
