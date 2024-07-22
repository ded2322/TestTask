"""
Задача 2:
Написать функцию, которая вернёт список объектов строительства, у каждого объекта строительства необходимо посчитать
стоимость всех работ и стоимость всех материалов.

Для решения использовал следующие шаги:

1. Получить все объекты строительства.
2. Для каждого объекта строительства вычислить общую стоимость всех работ и материалов.
3. Вернуть список объектов строительства, где каждый объект содержит его ID, стоимость всех работ и стоимость всех материалов.
"""
from django.db.models import Sum, F
from django.db import models

from myapp.models import Building, Expenditure, Section

def get_buildings() -> list[dict]:
    # Шаг 1: Получить все объекты строительства вместе с их секциями и расходами
    buildings = Building.objects.prefetch_related('sections__expenditures').all()

    result = []

    # Шаг 2: Для каждого объекта строительства вычислить стоимость всех работ и материалов
    for building in buildings:
        # Получаем все секции, связанные с данным объектом строительства
        sections = building.sections.all()

        # Собираем все расходы для секций
        expenditures = Expenditure.objects.filter(section__in=sections)

        # Разделяем расходы на работы и материалы и вычисляем их общую стоимость
        works_amount = expenditures.filter(type=Expenditure.Types.WORK).aggregate(
            total_work=Sum(F('count') * F('price'))
        )['total_work'] or 0

        materials_amount = expenditures.filter(type=Expenditure.Types.MATERIAL).aggregate(
            total_material=Sum(F('count') * F('price'))
        )['total_material'] or 0

        # Добавляем результаты в итоговый список
        result.append({
            'id': building.id,
            'works_amount': works_amount,
            'materials_amount': materials_amount
        })

    # Шаг 3: Возвращаем список объектов строительства с рассчитанными стоимостями
    return result
