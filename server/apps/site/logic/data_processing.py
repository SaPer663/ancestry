from django.db.models import Q, QuerySet

from server.apps.site.models import Family, Person


def get_family_queryset(id_spouse: int, surname=None) -> QuerySet:
    if surname is None:
        return Family.objects.filter(Q(id_husband=id_spouse) | Q(id_wife=id_spouse)) \
            .select_related('id_husband', 'id_wife').order_by('id')
    else:
        return Family.objects.filter((Q(id_husband=id_spouse) | Q(id_wife=id_spouse))) \
            .select_related('id_husband', 'id_wife').order_by('id') \
            .filter(surname=surname)


def is_wife(id_person: int, family: Family) -> bool:
    return True if family.id_wife.id == id_person else False


def get_partners(id_spouse: int, surname=None) -> dict:
    partners = {'husbands': [],
                'wives': []
                }
    if id_spouse is None:
        return {}
    if surname is None:
        families = get_family_queryset(id_spouse)
    else:
        families = get_family_queryset(id_spouse, surname=surname)
    for family in families:
        if is_wife(id_spouse, family):
            partners['husbands'].append(family.id_husband)
        else:
            partners['wives'].append(family.id_wife)

    return partners


def get_children(id_father: int = None, id_mother: int = None, id_family: int = None) -> QuerySet:
    """\
        get_children(id_father: int = None, id_mother: int = None, id_family: int = None) -> QuerySet
        id_father id of the father of children from Person,
        id_mother id of the mother of children from Person,
        id_family id of the family of spouse( father and mother) from Family
    """
    if id_family is None:
        id_family = Family.objects.filter(id_husband=id_father, id_wife=id_mother).first()
    return Person.objects.filter(parent_id=id_family).order_by('year_of_birth')


def is_alone(id_person) -> bool:
    """
    is_alone(id_person) -> bool
    return True if the person has a family
    """
    result = Family.objects.filter(Q(id_husband=id_person) | Q(id_wife=id_person))
    return True if len(result) > 0 else False


def get_family_composition(id_person: int) -> list:
    result = []
    partners = get_partners(id_person)
    if partners:
        for partner in partners:
            children = list(get_children(id_person, partner.id))
            result.append({'partner': partner, 'children': children})
    else:
        pass

    return result


def show_family(id_person):
    s = get_family_composition(id_person)
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
                    show_family(child.id)
