# Django Internationalization Tutorial

This is a Django project that demonstrates how to implement internationalization (i18n) and localization (l10n) in a Django application. It includes examples of translating static text, templates, and database content.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Localization and Internationalization](#localization-and-internationalization)

## Requirements

Before you begin, ensure you have met the following requirements:

- Python (3.9 or higher)
- Django (3.2)
- Other dependencies as specified in the `requirements.txt` file.

## Installation

1. Clone this repository:

   git clone =>

2. Create a virtual environment and activate it:

   python -m venv venv
   source venv/bin/activate

3. Install the dependencies:

   pip install -r requirements.txt

## Usage

To run the project, use the following command:

    python manage.py runserver

## Project Structure

    The project is structured as like this:
    ├── core
    │ ├── admin.py
    │ ├── apps.py
    │ ├── models.py
    │ ├── serializers.py
    │ ├── tests.py
    │ ├── urls.py
    │ └── views.py
    ├── templates
    │
    ├── locale
    │ ├── en
    │ │ └── LC_MESSAGES
    │ │ ├── django.mo
    │ │ └── django.po
    │ ├── fr
    │ │ └── LC_MESSAGES
    │ │ ├── django.mo
    │ │ └── django.po
    │ └── es
    │ └── LC_MESSAGES
    │ ├── django.mo
    │ └── django.po
    ├── translation_tutorial
    │ ├── asgi.py
    │ ├── settings.py
    │ ├── urls.py
    │ └── wsgi.py
    ├── venv
    ├── db.sqlite3
    ├── manage.py
    ├── README.md
    └── requirements.txt

## Implementation

1. Install Django and create a new project:

   django-admin startproject translation_tutorial

2. Then command python3 -m venv venv
3. Source venv/bin/activate
4. pip install django
5. django-admin startapp core
6. Create a ursl.py in the core app:

```cpp
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from core.views import post_list, category_list
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/posts/', views.post_list),
    path('api/categories/', views.category_list),
]

```

7. Install gettext
   `sudo apt-get install gettext`

8. Create views for language-specific content in core/views.py.

this is the index page view for languages:

```cpp
def index(request):
    if request.user.is_authenticated:
        messages.success(request, _("authmessage {first} {last}").format(
            first=request.user.first_name, last=request.user.last_name), extra_tags="alert alert-success")
    else:
        messages.warning(request, _("anonmessage"),
                         extra_tags="alert alert-danger")

    # Get the language code from the request.
    language_code = request.LANGUAGE_CODE

    # Filter the posts by language code.
    posts = Post.objects.filter(translations__language_code=language_code)

    context = {'posts': posts}
    return render(request, 'index.html', context)
```

9. Define models for database content in core/models.py.

````cpp
    from django.db import models
    from django.utils.translation import gettext_lazy as _
    from parler.models import TranslatableModel, TranslatedFields


 class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=50),
    )

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name



    class Post(TranslatableModel):
    category = models.ForeignKey(Category, related_name=_(
        'category'), on_delete=models.SET_NULL, null=True)
    translations = TranslatedFields(
        title=models.CharField(_('title'), max_length=50),
        content=models.TextField(_('content')),
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self):
        return self.title
```
10. Create serializers for API views in core/serializers.py.

11. Create templates for rendering HTML pages.

    for admin page language customization:

 ```cpp

    {% extends "admin/base.html" %}

    {% load i18n %}

    {% block extrahead %}
    {{ block.super }}
    <style>
    /* Add custom styles here, if needed */
    .language-form {
      display: inline-block;
    }
    .language-label {
      display: inline-block;
      margin-right: 5px;
    }
    .language-select {
      display: inline-block;
    }
  </style>
 {% endblock %}

 {% block userlinks %}
  {{ block.super }}
  <form class="language-form" id="languageForm" method="post" action="{% url 'set_language' %}">
    {% csrf_token %}
    <label class="language-label" for="language">Lang:</label>
    <select class="language-select" name="language" onchange="changeLanguage(this.value)">
        {% get_current_language as CURRENT_LANGUAGE %}
        {% get_available_languages as AVAILABLE_LANGUAGES %}
        {% get_language_info_list for AVAILABLE_LANGUAGES as languages %}
        {% for language in languages %}
            <option value="{{ language.code }}" {% if language.code == CURRENT_LANGUAGE %}selected{% endif %}>{{ language.name_local }}</option>
        {% endfor %}
    </select>
  </form>



  <script>
    function changeLanguage(languageCode) {
      const form = document.getElementById('languageForm');
      form.elements.language.value = languageCode;
      form.submit();
    }
  </script>

  {% endblock %}
```
12. Update project settings in settings.py for language and translation configurations.

    add this to the settings.py:

```cpp

    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

        'core',
        'rosetta',
        'parler',
        "rest_framework",

    ]

    LANGUAGE_CODE = 'en'

    LANGUAGES = [
    ('en', _('English')),
    ('fa', _('Persian')),
    ('tr', _('Turkish')),
    ('fr', _('French')),
    ('es', _('Spanish')),
    ('ar', _('Arabic')),
]

    PARLER_LANGUAGES = {
    None: (
        {'code': 'en', },
        {'code': 'fa', },
        {'code': 'tr', },
        {'code': 'fr', },
        {'code': 'es', },
        {'code': 'ar', },
    ),
    'default': {
        'fallbacks': ['en'],
        'hide_untranslated': False,
        'domain_name': None,
    }
}

    'DIRS': [os.path.join(BASE_DIR / 'templates/')],
```
13. Update admin.py
    add this to the admin.py:

```cpp
    from django.contrib import admin
    from .models import *
    from parler.admin import TranslatableAdmin


    class OurAdminPanel(TranslatableAdmin):
        search_fields = ['category__translations__name__icontains',
                        'translations__title__icontains', 'translations__content__icontains']


    admin.site.register(Post, OurAdminPanel)
    admin.site.register(Category, TranslatableAdmin)

```
14. Create a locale folder:
15. Create (en, fr, es) etc. folders:
16. Run django-admin makemessages -all:
17. Add translations to the .po files:
18. Run django-admin compilemessages:

````
