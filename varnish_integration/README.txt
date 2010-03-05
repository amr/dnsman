OVERVIEW
========

  DNSMan includes integration with Varnish, thanks to python-varnish and
  django-varnish package by Justin Quick. Normally, you don't need any explicit
  integration between the application and the front-end reverse proxy cache.
  However, the Varnish integration in DNSMan allows it to monitor redirection
  rules, and when they are updated, it will purge the redirection's cache on
  Varnish. Such precision is typically not possible without such explicit
  integration.

  This ensures that resources are served blazingly fast (from Varnish cache),
  and yet are always up to date.


SO HOW IT WORKS?
================

  It communicates with Varnish on its management port (telnet), and purges the
  cached resources for the redirections when they are updated.


INSTALLATION
============

  * Install python-varnish: http://github.com/justquick/python-varnish

  * Install django-varnish: http://github.com/justquick/django-varnish

  * Open local_settings.py and enable Varnish integration:

      VARNISH_MANAGEMENT = True

  * You also need to adjust VARNISH_MANAGEMENT_ADDRS if your Varnish management
    port is something other than the default which is 127.0.0.1:6082


  Enjoy!
