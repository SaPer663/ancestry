import typing

from django import template

from ..logic.data_processing import get_family_composition
from ..models import Family, Person

register = template.Library()


@register.simple_tag(name='tag_children')
def children(id_father: int, id_mother: int):
    """Return """
    return Family.get_children(id_father, id_mother)


@register.inclusion_tag('site/family_composition.html')
def show_family_composition(person: Person, family: Family) -> dict:
    families = get_family_composition(person, family)
    return {'families': families}


@register.simple_tag(name='family_composition')
def family_composition(obj: typing.Union[Person, Family]) -> list:
    return get_family_composition(obj)
