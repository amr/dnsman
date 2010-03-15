OVERVIEW
========

  DNSMan currently provides a redirections service with a web UI.


INSTALLATION
============

  * Download & Install Django 1.2 from:

        http://www.djangoproject.com/download/

  * Copy local_settings.py.dist as local_settings.py and adjust its settings
    which are all well-commented and self-explanatory.

  * Run the server using: ./manage.py runserver


RUNNING USING SPAWNING
======================

  The application server bundled with DNSMan is a simple single-threaded server.
  It's used for development and quick prototyping. For production, we recommend
  using Spawning which is a multi-process, multi-threaded application server.

  To use it:

  * Install Python's setuptools package. Example on Ubuntu:

        $: sudo apt-get install python-setuptools

  * Install Spawning:

        $: sudo easy_install spawning

  * Run DNSMan under Spawning:

        $: cd <dnsman-root-dir>
        $: sudo spawn --factory=spawning.django_factory.config_factory -p 80 dnsman.settings

Enjoy!
