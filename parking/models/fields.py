from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.forms.fields import ChoiceField
from django.core.exceptions import ValidationError
import os, re

class DirectoryPathField(models.Field):
    description = _('Directory path')

    class FormField(ChoiceField):
        def __init__(self, path, match=None, required=True, widget=None,
                     label=None, initial=None, help_text=None, *args, **kwargs):
            self.path, self.match = path, match
            super(DirectoryPathField.FormField, self).__init__(choices=(),
                required=required, widget=widget, label=label,
                initial=initial, help_text=help_text, *args, **kwargs)

            if self.required:
                self.choices = []
            else:
                self.choices = [('', '---------')]

            self.choices.append(('[auto-create]', '[auto-create]'))

            if self.match is not None:
                self.match_re = re.compile(self.match)

            try:
                for d in os.listdir(self.path):
                    full_dir = os.path.join(self.path, d)
                    if os.path.isdir(full_dir) and (self.match is None or self.match_re.search(d)):
                        self.choices.append((d, d))
            except OSError:
                pass

            self.widget.choices = self.choices

    def __init__(self, verbose_name=None, name=None, path='', match=None, **kwargs):
        self.path, self.match = path, match
        kwargs['max_length'] = kwargs.get('max_length', 100)
        models.Field.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'path': self.path,
            'match': self.match,
            'form_class': DirectoryPathField.FormField
        }
        defaults.update(kwargs)
        return super(DirectoryPathField, self).formfield(**defaults)

    def validate(self, value, model_instance):
        super(DirectoryPathField, self).validate(value, model_instance)

        # If [auto-create] was selected, make sure the to-be-created directory
        # doesn't already exist.
        if value == '[auto-create]':
            if not hasattr(model_instance, 'auto_dir'):
                raise NotImplementedError("Model %s does not implement auto_dir which is required for auto-creating the directory for field %s" % (model_instance, self))

            dir_name = model_instance.auto_dir(self)
            if os.path.exists(os.path.join(self.path, dir_name)):
                raise ValidationError("Won't be able to auto-create the directory as a conflicting one already exists (%s)" % os.path.join(self.path, dir_name))

    def clean(self, value, model_instance):
        value = super(DirectoryPathField, self).clean(value, model_instance)
        
        if value == '[auto-create]':
            dir_name = model_instance.auto_dir(self)
            dir_path = os.path.join(self.path, dir_name)
            os.mkdir(dir_path)
            value = dir_path
        
        return value

    def get_internal_type(self):
        return 'FilePathField'
