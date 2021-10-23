from typing import Dict, List, Optional, Union

from django.db.models import Q, QuerySet

from server.apps.site.models import Family, Person

type_get_family = List[Dict[str, Optional[List[Person]]]]


def get_family_queryset(spouse: Person) -> QuerySet:
    return Family.objects.select_related('id_husband', 'id_wife') \
        .filter(Q(id_husband=spouse.pk) | Q(id_wife=spouse.pk)).order_by('id')


def is_wife(person: Person) -> bool:
    return True if person.husband.values_list().first() is None else False


def get_partners(spouse: Person, gender: int) -> list:
    partners = []
    families = get_family_queryset(spouse)

    for family in families:
        if gender:
            partners.append(family.id_wife)
        else:
            partners.append(family.id_husband)
    return partners


def get_family_composition(obj: Union[Person, Family]) -> type_get_family:
    result: type_get_family = []
    if isinstance(obj, Person):
        families_queryset = get_family_queryset(obj)
        for family in families_queryset:
            children = list(
                family.children.prefetch_related('parent_id').order_by(
                    'year_of_birth'))
            if is_wife(obj):
                partner = family.id_husband
            else:
                partner = family.id_wife
            result.append({'partner': partner, 'children': children})
    else:
        children = list(obj.children.prefetch_related('parent_id'))
        result.append({'partner': None, 'children': children})
    return result


def get_family_composition_by_family(family: Family) -> type_get_family:
    result = []
    children = list(family.children.all())
    result.append({'partner': None, 'children': children})
    return result


def show_family(person):
    s = get_family_composition(person)
    p = 'partner'
    c = 'children'
    for family in s:
        print(family[p])
        if len(family[c]) > 0:
            print(f'len(family[c]) = {len(family[c])}')
            for child in family[c]:
                print(child.name)
                if not child.is_alone():
                    print(f'{child.name} not alone')
                    show_family(child)
