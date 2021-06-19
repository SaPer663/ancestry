from django.contrib import admin

from server.apps.site.models import Family, Person


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin[Family]):
    """Admin panel example for ``BlogPost`` model."""

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('id_husband', 'id_wife')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin[Person]):
    """Admin panel example for ``BlogPost`` model."""
