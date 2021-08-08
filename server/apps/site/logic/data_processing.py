from django.db import connection, reset_queries
from django.db.models import Q, QuerySet

from server.apps.site.models import Family, Person


def get_family_queryset(spouse: Person) -> QuerySet:
    return Family.objects.select_related('id_husband', 'id_wife') \
        .filter(Q(id_husband=spouse.pk) | Q(id_wife=spouse.pk)).order_by('id')


def get_family_queryset_by_wife(spouse: Person) -> QuerySet:
    return Family.objects.select_related('id_husband', 'id_wife').filter(id_wife=spouse.pk).order_by('id')


def get_family_queryset_by_husband(spouse: Person) -> QuerySet:
    return Family.objects.select_related('id_husband', 'id_wife').filter(id_husband=spouse.pk).order_by('id')


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


def get_children(family: Family) -> list:
    return list(family.children.prefetch_related('parent_id').order_by('year_of_birth'))


def get_family_composition(person: Person) -> list:
    result: list = []
    if person is not None:
        person_is_wife = is_wife(person)
        families_queryset = (get_family_queryset_by_wife(person) if person_is_wife
                             else get_family_queryset_by_husband(person))
        for family_queryset in families_queryset:
            children = list(family_queryset.children.prefetch_related('parent_id').order_by('year_of_birth'))
            if person_is_wife:
                partner = family_queryset.id_husband
            else:
                partner = family_queryset.id_wife
            result.append({'partner': partner, 'children': children})
    return result


def get_children_by_family(family: Family) -> list:
    return list(family.children.all())


def show_family_composition(person: Person, family: Family) -> list:
    families = get_family_composition(person, family)
    return families


def show_family(family):
    p = 'partner'
    c = 'children'
    result = []
    children = get_children(family)
    if children:
        for child in children:
            print(f'{c} {child}')
            if child.is_alone():
                continue
            fam = get_family_composition(child)
            for f in fam:
                print(f'{p} {f[p]}')


def get_family(person: Person):
    if person.is_alone():
        return print(person)
    print(f'81 {person}')
    fam = get_family_composition(person)
    for f in fam:
        print(f'partner {f["partner"]}')
        for child in f['children']:
            get_family(child)


def cq():
    print(len(connection.queries))


def rs():
    reset_queries()
# from server.apps.site.logic import data_processing as dp from server.apps.site.models import Family as F f = F.objects.get(id=15)

# from server.apps.site.models import Family as F

# from server.apps.site.models import  Person as P
# f = F.objects.get(id=15)
