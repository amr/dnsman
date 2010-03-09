from dnsman.redirections.models import Redirection
from dnsman.domains.models import Domain
from dnsman.redirections.forms import RedirectionForm
from dnsman.redirections.forms import RedirectionBulkAdd

from django.contrib import admin
from django.utils.translation import ugettext as _

from django import template
from django.contrib import admin
from django.db import models, transaction
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied, ValidationError
from django.views.decorators.csrf import csrf_protect
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response
from django.utils.translation import ungettext

class RedirectionAdmin(admin.ModelAdmin):
    form = RedirectionForm
    fieldsets = [
        (None, {'fields': ['from_domain', 'to_domain']}),
        ('Advanced options', {'fields': ['full_uri', 'code', 'weight', 'enabled'], 'classes': ['collapse']}),
    ]
    list_display = ('from_domain', 'to_domain', 'full_uri', 'code', 'weight', 'enabled', 'formatted_last_modified')
    list_filter = ['code', 'full_uri', 'enabled']
    search_fields = ['to_domain__name', 'from_domain__name']
    ordering = ['-weight']

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        urls = super(RedirectionAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^bulk-add/$', self.admin_site.admin_view(self.bulkadd_view), name='redirections_bulkadd')
        )
        return my_urls + urls

    # The view is csrf-protected as it's wrapped with admin_view
    @transaction.commit_manually
    def bulkadd_view(self, request, form_url='', extra_context=None):
        "The bulk-add admin view for domains."
        model = self.model
        opts = model._meta

        if not self.has_add_permission(request):
            raise PermissionDenied

        if request.method == 'POST':
            form = RedirectionBulkAdd(request.POST)
            if form.is_valid():
                from_domains = form.cleaned_data['from_domains'].splitlines()
                # Trim
                from_domains = [s.strip() for s in from_domains]
                # Remove empty items
                from_domains = filter(None, from_domains)
                
                added_redirects = []
                remaining_redirects = []
                for domain in from_domains:
                    try:
                        try:
                            from_domain = Domain.objects.get(name=domain)
                        except Domain.DoesNotExist:
                            from_domain = Domain(name=domain)
                            from_domain.full_clean()
                            from_domain.save()
                            self.log_addition(request, from_domain)
                        r = Redirection(to_domain=form.cleaned_data['to_domain'], from_domain=from_domain)
                        r.full_clean()
                        r.save()
                        self.log_addition(request, r)
                        added_redirects.append(domain)
                    except ValidationError, e:
                        remaining_redirects.append(domain)
                        form._errors.setdefault('from_domains', form.error_class()).extend(["%s: %s" % (domain, error) for error in e.messages])

                # Commit if there were no errors, or there were partial errors
                # and the ignore_errors flag is off.
                if form.errors and not form.cleaned_data['ignore_errors']:
                    transaction.rollback()
                else:
                    transaction.commit()
                    # Remove the successfully added redirections
                    data = request.POST.copy()
                    data['from_domains'] = "\n".join(remaining_redirects)
                    form.data = data
                    self.message_user(request, ungettext("%d redirection to %s was added successfully.",
                                                         "%d redirections to %s were added successfully.",
                                                         len(added_redirects)) % (len(added_redirects), form.cleaned_data['to_domain']))
                
                if not form.errors:
                    return HttpResponseRedirect('../')
        else:
            # Prepare the dict of initial data from the request.
            initial = dict(request.GET.items())
            form = RedirectionBulkAdd(initial=initial)
    
        fieldsets = [(None, {'fields': form.base_fields.keys()})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, self.prepopulated_fields)
        media = self.media + adminForm.media

        context = {
            'title': _('Add multiple %s') % force_unicode(opts.verbose_name_plural),
            'add': True,
            'change': True,
            'adminform': adminForm,
            'is_popup': False,
            'has_add_permission': True,
            'has_change_permission': self.has_change_permission(request),
            'has_delete_permission': False,
            'media': mark_safe(media),
            'inline_admin_formsets': [],
            'errors': admin.helpers.AdminErrorList(form, []),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
            'opts': opts,
        }
        context.update(extra_context or {})

        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response([
            "admin/%s/%s/bulkdadd_form.html" % (opts.app_label, opts.object_name.lower()),
            "admin/%s/bulkadd_form.html" % opts.app_label,
            "admin/bulkadd_form.html"
        ], context, context_instance=context_instance)
        return self.render_change_form(request, context, form_url=form_url, add=True)

admin.site.register(Redirection, RedirectionAdmin)
