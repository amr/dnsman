from django.utils._os import safe_join
import os
import zipfile

from dnsman.lib.filetree import FileTreeServer

class ExternalResourcesServer(FileTreeServer):
    # We add support for extracting uploaded .zip files in place
    def _upload(self, request):
        path = self.expand_path(request.POST['path'])
        errors = {}
        for name, f in request.FILES.items():
            ext = os.path.splitext(f.name)[1]
            if ext == '.zip' and f.content_type == 'application/zip':
                z = zipfile.ZipFile(f)
            
                if z.testzip() is not None:
                    raise zipfile.BadZipFile()
                
                # TODO: Need more validation
                # See: http://docs.python.org/library/zipfile.html#zipfile.ZipFile.extractall
                z.extractall(path)
            else:
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
