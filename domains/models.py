from django.db import models

class Domain(models.Model):
    name = models.CharField('Domain name', max_length=253)

    def __unicode__(self):
        return self.name

    def redirection_rules(self):
        return self.redirection_set.count()
