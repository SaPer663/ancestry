from django.contrib import admin

from server.apps.site.models import Family, Person


@admin.register(Family)
class BlogPostAdmin(admin.ModelAdmin[Family]):
    """Admin panel example for ``BlogPost`` model."""


@admin.register(Person)
class BlogPostAdmin(admin.ModelAdmin[Person]):
    """Admin panel example for ``BlogPost`` model."""
