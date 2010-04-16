def varnish_can_cache(response):
    """
    Patches given response with a special header indicating that Varnish can
    ignore any cache control headers and cache the response anyway.

    You must only use this if your model is being watched by Varnish and
    implements varnish_purge_hash_patterns().
    """

    response['X-Varnish-Can-Cache'] = 1
