OVERVIEW
========

  The zones application of DNSMan provides a basic interface for managing your
  BIND-compatible zones configuration from a web-interface, integrating with the
  rest of DNSMan's components.


CONFIGURATION
=============

  In order for DNSMan to interoperate with your BIND configuration, you need to
  have your BIND zones stored in a separate directory, and make sure DNSMan can
  read & write to that directory. Below we will show you how to do that. The
  instructions below matches the default settings of Debian/Ubuntu GNU/Linux
  distributions, you should adapt them for your own OS accordingly.

  1. Create a new directory for your zones:

    $: sudo mkdir /etc/bind/zones

  2. If you run DNSMan under non-root user (e.g. dnsman), give DNSMan permission
     to read/write that directory:

    $: sudo chown dnsman /etc/bind/zones

  3. Move all your zones inside that directory, and adjust your BIND options
     files accordingly (e.g. /etc/bind/named.conf*)

  4. Open local_settings.py and configure the path to your zones:

       ZONES_PATH = "/etc/bind/zones"


Enjoy!
