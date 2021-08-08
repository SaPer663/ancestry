from typing import Dict

from django import template

from ..logic.data_processing import get_family_composition
from ..models import Family, Person

register = template.Library()


@register.simple_tag(name='get_children')
def get_chil(family: Family) -> list:
    return list(family.children.prefetch_related('parent_id').order_by('year_of_birth'))


@register.inclusion_tag('site/family_composition.html')
def show_family_composition(person: Person) -> dict:
    families = get_family_composition(person)
    return {'families': families}


@register.inclusion_tag('site/get_children.html')
def get_children(family: Family) -> Dict[str, list]:
    children = list(family.children.prefetch_related('parent_id').order_by('year_of_birth'))
    return {'children': children}
