from typing import Final, final

from django.db import models
from django.db.models import Q, QuerySet
#: That's how constants should be defined.
from django.utils.text import slugify

_MAX_LENGTH_LONG: Final = 100
_MAX_LENGTH_SHORT: Final = 30


@final
class Family(models.Model):
    """
    The model contains the surname of the spouses (by husband),
    id of the husband and wife (by the Person model)

    """

    surname = models.CharField(max_length=_MAX_LENGTH_SHORT)
    id_husband = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
        related_name='husband',
        blank=True,
        null=True
    )
    id_wife = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
        related_name='wife',
        blank=True,
        null=True
    )
    slug = models.SlugField(
        max_length=_MAX_LENGTH_SHORT,
        unique=True, blank=True
    )

    class Meta(object):
        ordering = ('surname',)
        verbose_name = 'Family'  # You can probably use `gettext` for this
        verbose_name_plural = 'Families'

    # def get_absolute_url(self) -> str:
    #    return reverse('site:detail_family', args=[self.pk, self.slug])

    def save(self):
        super(Family, self).save()
        if not self.slug:
            self.slug = slugify(self.surname, allow_unicode=True) + '-' + str(self.pk)
            super(Family, self).save()

    @staticmethod
    def get_partners(id_spouse: int) -> list:
        list_partners = []
        families = Family.objects.filter(Q(id_husband=id_spouse) | Q(id_wife=id_spouse)) \
            .select_related('id_husband', 'id_wife').order_by('id')
        for family in families:
            if family.id_husband.id == id_spouse:
                list_partners.append(family.id_wife)
            else:
                list_partners.append(family.id_husband)
        return list_partners

    @staticmethod
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

    def children(self) -> list:
        """\
            get_children(id_father: int = None, id_mother: int = None, id_family: int = None) -> QuerySet
            id_father id of the father of children from Person,
            id_mother id of the mother of children from Person,
            id_family id of the family of spouse( father and mother) from Family
        """
        return list(self.children.prefetch_related('parent_id').order_by('year_of_birth'))

    @staticmethod
    def is_alone(id_person) -> bool:
        """
        is_alone(id_person) -> bool
        return True if the person has a family
        """
        result = Family.objects.filter(Q(id_husband=id_person) | Q(id_wife=id_person))
        return True if len(result) > 0 else False

    def __str__(self) -> str:
        """Return surname(id husband, id wife)"""
        return f'{self.surname}_{self.pk}({self.id_husband},{self.id_wife})'


@final
class Person(models.Model):
    """
        The model Person contains personal data about a person
        required fields - parent id and name
        you can specify the dates of life and death
        and if not known then at least years and also optional

        """

    parent_id = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        related_name='children'
    )
    name = models.CharField(max_length=_MAX_LENGTH_SHORT)
    surname = models.CharField(
        max_length=_MAX_LENGTH_SHORT,
        blank=True
    )
    patronymic = models.CharField(
        max_length=_MAX_LENGTH_SHORT,
        blank=True
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True
    )
    year_of_birth = models.CharField(
        max_length=_MAX_LENGTH_SHORT,
        blank=True
    )
    place_of_birth = models.CharField(
        max_length=_MAX_LENGTH_LONG,
        blank=True
    )
    date_of_death = models.DateField(
        blank=True,
        null=True
    )
    year_of_death = models.CharField(
        max_length=_MAX_LENGTH_SHORT,
        blank=True
    )
    place_of_death = models.CharField(
        max_length=_MAX_LENGTH_LONG,
        blank=True
    )
    gender = models.PositiveSmallIntegerField(choices=((1, 'мужчина'),
                                                       (0, 'женщина')))

    def is_alone(self) -> bool:
        """
        is_alone(id_person) -> bool
        return True if the person has a family
        """
        result = Family.objects.filter(Q(id_husband=self.pk) | Q(id_wife=self.pk))
        return False if len(result) > 0 else True

    class Meta(object):
        ordering = ('surname',)
        verbose_name = 'Person'  # You can probably use `gettext` for this
        verbose_name_plural = 'Persons'

    def __str__(self) -> str:
        """Return surname name patronymic"""
        return f'{self.surname} {self.name} {self.patronymic}'
