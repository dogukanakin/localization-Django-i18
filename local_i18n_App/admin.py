from django.contrib import admin
from .models import *
from parler.admin import TranslatableAdmin


class OurAdminPanel(TranslatableAdmin):
    search_fields = ['category__translations__name__icontains',
                     'translations__title__icontains', 'translations__content__icontains']


admin.site.register(Post, OurAdminPanel)
admin.site.register(Category, TranslatableAdmin)
