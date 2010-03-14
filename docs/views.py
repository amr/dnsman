from django.template import loader, RequestContext
from django.shortcuts import render_to_response

def simple_doc(request, uri):
    """
    A generic view for rendering simple doc pages from their templates.
    """
    if uri is None:
        uri = ''

    templates = (
        'docs/' + uri.strip('/') + '.html',
        'docs/' + uri.strip('/') + '/index.html'
    )
    
    return render_to_response(templates, context_instance=RequestContext(request))
