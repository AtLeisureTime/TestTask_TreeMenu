from django.db import models
from django.core.exceptions import ValidationError


class Menu(models.Model):
    NAME_LEN = 80

    name = models.CharField(max_length=NAME_LEN, blank=False, unique=True)

    def __str__(self):
        return f'{self.name}'


class Element(models.Model):
    """ Elements of menus."""
    VALUE_LEN = 80
    URL_LEN = 200

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, blank=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    value = models.CharField(max_length=VALUE_LEN, blank=False)
    url = models.URLField(max_length=URL_LEN, blank=True)
    namedUrl = models.CharField(max_length=VALUE_LEN, blank=True)

    def __str__(self):
        return self.value

    def clean(self):
        super().clean()
        if self.url and self.namedUrl:
            raise ValidationError({'namedUrl': 'Only url or namedUrl should have a value.'})
