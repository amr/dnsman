from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import simplejson
from django.utils._os import safe_join
import os

class FileTreeServer(object):
    VALID_COMMANDS = ['get', 'rename', 'newdir', 'delete', 'upload']

    def __init__(self, root_dir):
        self.root_dir = root_dir

    def serve(self, request):
        cmd = request.POST['cmd']
        if cmd not in self.VALID_COMMANDS:
            return HttpResponseBadRequest()

        func = getattr(self, "_%s" % cmd)
        try:
            result = func(request)
        except:
            result = {'success': False, 'error': 'An error had occurred, contact the system administrator'}

        mimetype = getattr(func, 'mimetype', 'application/json')
        return HttpResponse(self.to_json(result), mimetype=mimetype)

    def _get(self, request):
        path = self.expand_path(request.POST['path'])
        result = []
        for f in os.listdir(path):
            node = FileTreeNode(os.path.join(path, f))
            result.append(node.as_dict())
        return result

    def _rename(self, request):
        newname = self.expand_path(request.POST['newname'])
        oldname = self.expand_path(request.POST['oldname'])
        if os.path.exists(newname):
            return {'success': False, 'error': 'A file or a directory with that name already exists'}
        else:
            os.rename(oldname, newname)
            return {'success': True}

    def _newdir(self, request):
        path = self.expand_path(request.POST['dir'])
        os.mkdir(path)
        return {'success': True}

    def _delete(self, request):
        path = self.expand_path(request.POST['file'])
        if os.path.isdir(path):
            import shutil
            shutil.rmtree(path)
        else:
            os.remove(path)
        return {'success': True}

    def _upload(self, request):
        path = self.expand_path(request.POST['path'])
        errors = {}
        for name, f in request.FILES.items():
            try:
                dest = open(os.path.join(path, os.path.basename(f.name)), 'wb+')
                for chunk in f.chunks():
                    dest.write(chunk)
                dest.close()
            except:
                errors[name] = "Could not upload %s" % os.path.basename(f.name)
        if len(errors):
            return {'success': False, 'errors': errors}
        else:
            return {'success': True}
    _upload.mimetype = 'text/html'

    def to_json(self, data):
        return simplejson.dumps(data)

    def expand_path(self, path):
        return safe_join(self.root_dir, path)

    def unknown_error(self):
        return {'success': False, 'error': 'An error had occurred, contact the system administrator'}


class FileTreeNode(object):
    def __init__(self, path, disabled=False):
        self.path = path
        self.options = {'disabled': disabled}

    def as_dict(self):
        return {
            'text': self.text,
            'disabled': self.options['disabled'],
            'leaf': self.leaf,
            'iconCls': self.icon_class,
        }
        
    def text(self):
        return os.path.basename(self.path)
    text = property(text)

    def leaf(self):
        return (not self.isdir)
    leaf = property(leaf)

    def icon_class(self):
        if self.isdir:
            return 'folder'
        ext = os.path.splitext(self.path)[1]
        if ext:
            return "file-%s" % ext.strip('.')
        return ''
    icon_class = property(icon_class)

    def isdir(self):
        try:
            return self._is_dir
        except AttributeError:
            self._is_dir = os.path.isdir(self.path)
            return self._is_dir
    isdir = property(isdir)
