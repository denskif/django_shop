from django.db import models


class PrivacyPolicy(models.Model):

    text = models.TextField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "FF %s" % self.text

    class Meta:
        verbose_name = 'Политика конфиденцияальности'
        verbose_name_plural = 'Политики конфиденцияальности'

