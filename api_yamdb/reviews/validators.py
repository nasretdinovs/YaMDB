import datetime

from django.core.validators import MaxValueValidator, RegexValidator


def this_year():
    """Вывод нынешнего года."""
    return datetime.date.today().year


def validator_year():
    """Проверка на год выпуска."""
    return MaxValueValidator(
        this_year,
        message='Год выпуска не может быть больше текущего!'
    )


def username_validator():
    """Проверка на допустимые символы в имени пользователя."""
    return RegexValidator(
        regex=r'^[\w.@+-]+$',
        message='Допускаются буквы, цифры и знаки _ @ / + - .'
    )
