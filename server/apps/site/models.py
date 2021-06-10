from typing import Final, final

from django.db import models

#: That's how constants should be defined.
_MAX_LENGTH_LONG: Final = 100
_MAX_LENGTH_SHORT: Final = 30


@final
class Family(models.Model):
    """
    The model contains the surname of the spouses (by husband),
    id of the husband and wife (by the Person model)

    """

    surname = models.CharField(max_length=_MAX_LENGTH_SHORT)
    id_husband = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='id_husband', blank=True)
    id_wife = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='id_wife', blank=True)
    slug = models.SlugField(max_length=_MAX_LENGTH_SHORT, unique=True)

    class Meta(object):
        ordering = ('surname',)
        verbose_name = 'Family'  # You can probably use `gettext` for this
        verbose_name_plural = 'Families'

    def __str__(self) -> str:
        """Return surname(id husband, id wife)"""
        return f'{self.surname}({self.id_husband},{self.id_wife})'


@final
class Person(models.Model):
    """
        The model contains the surname of the spouses (by husband),
        id of the husband and wife (by the Person model)

        """

    parent_id = models.ForeignKey(Family, on_delete=models.CASCADE)
    name = models.CharField(max_length=_MAX_LENGTH_SHORT)
    surname = models.CharField(max_length=_MAX_LENGTH_SHORT, blank=True)
    patronymic = models.CharField(max_length=_MAX_LENGTH_SHORT, blank=True)
    date_of_birth = models.DateField(blank=True)
    place_of_birth = models.CharField(max_length=_MAX_LENGTH_LONG, blank=True)
    date_of_death = models.DateField(blank=True)

    class Meta(object):
        ordering = ('surname',)
        verbose_name = 'Person'  # You can probably use `gettext` for this
        verbose_name_plural = 'Persons'

    def __str__(self) -> str:
        """Return surname(id husband, id wife)"""
        return f'{self.surname} {self.name}'
