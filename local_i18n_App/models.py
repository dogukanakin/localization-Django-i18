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
        return self.safe_translation_getter('name', str(self.id))


class Post(TranslatableModel):
    category = models.ForeignKey(
        Category, related_name='posts', on_delete=models.SET_NULL, null=True, verbose_name=_("category")
    )
    translations = TranslatedFields(
        title=models.CharField(_('title'), max_length=50),
        content=models.TextField(_('content')),
        image=models.ImageField(upload_to='post_images/',),
        description=models.TextField(verbose_name=_("description")),
    )

    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created"))

    class Meta:
        ordering = ('-created',)
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self):
        return self.title


class MovieName(models.Model):
    nameEn = models.CharField(max_length=100)
    nameTr = models.CharField(max_length=100)
    nameAr = models.CharField(max_length=100)
    nameFr = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.nameEn
