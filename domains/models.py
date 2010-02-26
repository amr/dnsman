from django.db import models

class Domain(models.Model):
    name = models.CharField('Name', unique=True, max_length=253, help_text='The domain name, e.g. "example.com"')

    def __unicode__(self):
        return self.name

    def redirections_count(self):
        return self.redirections.count()
    redirections_count.short_description = 'Redirections #'
