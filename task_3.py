"""
Задача 3:

Пользователь хочет применить скидку для секции на стоимость всех расценок внутри. Написать функцию, которая обновит
поле price у всех расценок внутри секции с учётом этой скидки.

Ход решения:
1. Получить все расценки, связанные с указанной секцией.
2. Применить скидку к каждой из расценок.
3. Обновить поле price для каждой расценки.
"""

from decimal import Decimal
from django.db import transaction

from myapp.models import Expenditure


def update_with_discount(section_id: int, discount: Decimal):
    """
    Обновляет поле price у всех расценок внутри указанной секции с учётом скидки.

    @param discount: Размер скидки в процентах от Decimal(0) до Decimal(100)
    """
    # Проверяем, что скидка в допустимом диапазоне
    if not (Decimal(0) <= discount <= Decimal(100)):
        raise ValueError("Размер скидки должен быть от 0 до 100")

    # Рассчитываем множитель скидки
    discount_multiplier = (Decimal(100) - discount) / Decimal(100)

    # Получаем все расценки для указанной секции
    expenditures = Expenditure.objects.filter(section_id=section_id)

    # Применяем скидку и обновляем цены
    with transaction.atomic():
        for expenditure in expenditures:
            new_price = expenditure.price * discount_multiplier
            expenditure.price = new_price
            expenditure.save(update_fields=['price'])
