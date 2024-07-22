"""
Задача 1:
Написать тело функции, которая для каждого конкретного объекта строительства будет возвращать список только родительских секций.
У каждой родительской секции необходимо посчитать бюджет (стоимость всех расценок внутри).

Шаги решения:

1. Получить все секции, которые принадлежат указанному объекту строительства (building).
2. Отфильтровать эти секции, оставив только родительские секции, то есть те, у которых parent равен None.
3. Для каждой родительской секции рассчитать бюджет, то есть сумму всех расходов (Expenditure), которые привязаны к данной секции и ее дочерним секциям.
4. Вернуть список родительских секций, где каждая секция будет содержать свой бюджет.
"""
from django.db.models import Sum, F
from django.db import models

from myapp.models import Expenditure, Section

def get_parent_sections(building_id: int) -> list[Section]:
    # Шаг 1: Получить все секции, принадлежащие указанному объекту строительства и их дочерние секции
    all_sections = Section.objects.filter(building_id=building_id).prefetch_related('children')

    # Шаг 2: Отфильтровать только родительские секции
    parent_sections = all_sections.filter(parent__isnull=True)

    # Шаг 3: Для каждой родительской секции рассчитать бюджет
    sections_with_budget = []
    for parent_section in parent_sections:
        # Получаем все расценки для текущей родительской секции и ее дочерних секций
        section_ids = [parent_section.id] + [child.id for child in parent_section.children.all()]
        expenditures = Expenditure.objects.filter(section_id__in=section_ids)

        # Рассчитываем бюджет как сумму произведений количества и цены для всех расценок
        budget = expenditures.aggregate(
            total_budget=Sum(F('count') * F('price'))
        )['total_budget'] or 0  # Если нет расценок, то бюджет 0

        # Добавляем секцию и ее бюджет в результирующий список
        sections_with_budget.append({
            'section': parent_section,
            'budget': budget
        })

    # Шаг 4: Возвращаем список родительских секций с бюджетами
    return sections_with_budget
