from django import template

from ..logic.data_processing import get_family_composition
from ..models import Family, Person

register = template.Library()


@register.simple_tag(name='tag_children')
def children(id_father: int, id_mother: int):
    return Family.get_children(id_father, id_mother)


@register.inclusion_tag('site/family_composition.html')
def show_family_composition(person: Person, family: Family) -> dict:
    families = get_family_composition(person, family)
    return {'families': families}
