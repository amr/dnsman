from django.contrib import admin
from django.contrib.admin.util import unquote, flatten_fieldsets, get_deleted_objects
from django.forms.models import modelform_factory
from django import template, views
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import curry
from django.utils._os import safe_join
from django.core.urlresolvers import reverse

from dnsman.parking.models import ParkingPage
from dnsman.parking.forms import ParkingPageAddForm, ParkingPageChangeForm, ParkingPageDeleteForm
from dnsman.parking import PARKING_PAGES_URL
from dnsman.lib.filetree import filetree_virtualroot
from dnsman.parking.filetree import ExternalResourcesServer

import os

class ParkingPageAdmin(admin.ModelAdmin):    
    # See: self.get_form() and self.get_fieldsets()
    add_form = ParkingPageAddForm
    add_fieldsets = [
        ('', {'fields': ['name']}),
        ('Advanced', {'fields': ['resources_dir'], 'classes': ['collapse', 'advanced']}),
    ]
    change_form = ParkingPageChangeForm
    change_fieldsets = [
        ('Basic information', {'fields': ['name'], 'classes': ['collapse', 'basic']}),
        ('Template', {'fields': ['template', 'template_file'], 'classes': ['template']}),
        ('Advanced', {'fields': ['resources_dir', 'extends'], 'classes': ['collapse', 'advanced']}),
    ]

    list_display = ('name', 'extends', 'formatted_last_modified', 'used_in')
    list_filter = ['extends']
    search_fields = ['name']

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        urls = super(ParkingPageAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^(.+)/external-resources/$', self.admin_site.admin_view(self.extresources_view), name='parkingpages_extresources'),
            url(r'^(.+)/external-resources/filetree$', self.admin_site.admin_view(self.filetree_view), name='parkingpages_filetree'),
            url(r'^(.+)/preview/$', self.admin_site.admin_view(self.preview_view), name='parkingpages_preview'),
        )
        return my_urls + urls

    def extresources_view(self, request, object_id, extra_context=None):
        "The external-resources admin view for parking pages."
        model = self.model
        opts = model._meta

        object = get_object_or_404(model, pk=unquote(object_id))

        if not self.has_change_permission(request, object):
            raise PermissionDenied

        context = {
            'title': _('External resources: %s') % force_unicode(object),
            'is_popup': False,
            'object': object,
            'media': mark_safe(self.media),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
            'opts': opts,
            'filetree': {
                'backend_url': reverse('admin:parkingpages_filetree', args=[object_id]),
                'hrefPrefix': PARKING_PAGES_URL,
                'rootPath': filetree_virtualroot(object.resources_dir),
                'rootText': os.path.basename(object.resources_dir),
            },
        }
        context.update(extra_context or {})

        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response("admin/%s/%s/external_resources.html" % (opts.app_label, opts.object_name.lower()),
                                  context, context_instance=context_instance)

    def filetree_view(self, request, object_id, extra_context=None):
        """FileTreePanel backend"""
        parkingPage = get_object_or_404(self.model, pk=unquote(object_id))

        if not self.has_change_permission(request, parkingPage):
            raise PermissionDenied

        filetree = ExternalResourcesServer(parkingPage.resources_dir_fullpath)
        return filetree.serve(request)
    filetree_view.csrf_exempt = True

    def preview_view(self, request, object_id, extra_context=None):
        """Preview parking pages"""
        parkingPage = get_object_or_404(self.model, pk=unquote(object_id))

        if not self.has_change_permission(request, parkingPage):
            raise PermissionDenied
        
        class ExampleDomain(object):
            name = "example.com"
            parking_page = parkingPage
        domain = ExampleDomain()

        return parkingPage.to_response(request, domain)

    # We override this to give different forms for add and change
    def get_form(self, request, obj=None, **kwargs):
        try:
            if obj is None:
                form = self.add_form
            else:
                form = self.change_form
        except AttributeError:
            raise ImproperlyConfigured("%s must have add_form and change_form defined" % self.__name__)
        
        if self.declared_fieldsets:
            fields = flatten_fieldsets(self.declared_fieldsets)
        else:
            fields = None
        if self.exclude is None:
            exclude = []
        else:
            exclude = list(self.exclude)
        exclude.extend(kwargs.get("exclude", []))
        exclude.extend(self.get_readonly_fields(request, obj))
        # if exclude is an empty list we pass None to be consistant with the
        # default on modelform_factory
        exclude = exclude or None
        defaults = {
            "form": form,
            "fields": fields,
            "exclude": exclude,
            "formfield_callback": curry(self.formfield_for_dbfield, request=request),
        }
        defaults.update(kwargs)
        return modelform_factory(self.model, **defaults)

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self.add_fieldsets
        else:
            return self.change_fieldsets

    @admin.options.csrf_protect_m
    def delete_view(self, request, object_id, extra_context=None):
        "The 'delete' admin view for this model."
        opts = self.model._meta
        app_label = opts.app_label

        obj = self.get_object(request, unquote(object_id))

        if not self.has_delete_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        # Populate deleted_objects, a data structure of all related objects that
        # will also be deleted.
        (deleted_objects, perms_needed) = get_deleted_objects((obj,), opts, request.user, self.admin_site)

        if request.method == 'POST': # The user has already confirmed the deletion.
            if perms_needed:
                raise PermissionDenied
            form = ParkingPageDeleteForm(request.POST)
            if form.is_valid():
                obj_display = force_unicode(obj)
                self.log_deletion(request, obj, obj_display)
                obj.delete(keep_resources=form.cleaned_data['keep_resources'])

                self.message_user(request, _('The %(name)s "%(obj)s" was deleted successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj_display)})

                if not self.has_change_permission(request, None):
                    return HttpResponseRedirect("../../../../")
                return HttpResponseRedirect("../../")

        form = ParkingPageDeleteForm()

        context = {
            "title": _("Are you sure?"),
            "object_name": force_unicode(opts.verbose_name),
            "object": obj,
            "form": form,
            "deleted_objects": deleted_objects,
            "perms_lacking": perms_needed,
            "opts": opts,
            "root_path": self.admin_site.root_path,
            "app_label": app_label,
        }
        context.update(extra_context or {})
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(self.delete_confirmation_template or [
            "admin/%s/%s/delete_confirmation.html" % (app_label, opts.object_name.lower()),
            "admin/%s/delete_confirmation.html" % app_label,
            "admin/delete_confirmation.html"
        ], context, context_instance=context_instance)

    # We are overriding it just to change the continue message
    def response_add(self, request, obj, post_url_continue='../%s/'):
        """
        Determines the HttpResponse for the add_view stage.
        """
        opts = obj._meta
        pk_value = obj._get_pk_val()

        msg = _('The %(name)s "%(obj)s" was added successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj)}
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.
        if request.POST.has_key("_continue"):
            self.message_user(request, msg + ' ' + _("You may now edit it below."))
            if request.POST.has_key("_popup"):
                post_url_continue += "?_popup=1"
            return HttpResponseRedirect(post_url_continue % pk_value)

        if request.POST.has_key("_popup"):
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                # escape() calls force_unicode.
                (escape(pk_value), escape(obj)))
        elif request.POST.has_key("_addanother"):
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(opts.verbose_name)))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)

            # Figure out where to redirect. If the user has change permission,
            # redirect to the change-list page for this object. Otherwise,
            # redirect to the admin index.
            if self.has_change_permission(request, None):
                post_url = '../'
            else:
                post_url = '../../../'
            return HttpResponseRedirect(post_url)

admin.site.register(ParkingPage, ParkingPageAdmin)
