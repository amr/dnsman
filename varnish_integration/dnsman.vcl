# This VCL is an example configuration file for varnish that ships with DNSMan's
# varnish integration application. If you are using Varnish specifically for
# DNSMan, then most probably you can use this file as a drop-in replacement to
# your distro's default varnish configuration and expect it to work with DNSMan.
#
# Otherwise, you should manually review the subroutines below and merge them
# with your existing ones.
#
# See the vcl(7) man page for details on VCL syntax and semantics.
#
# At the bottom you will find a commented-out copy of the default VCL logic.
# The default version of a subroutine is always appended to redefined versions.

# Default backend definition.  Set this to point to your content
# server.
backend default {
.host = "127.0.0.1";
.port = "8001";
}

sub vcl_recv {
    if (req.request == "GET" && !(req.url ~ "^/dnsman-admin") && !(req.url ~ "^/dnsman-media")) {
        lookup;
    }    
}

sub vcl_fetch {
    if (obj.http.X-Varnish-Can-Cache) {
        unset obj.http.X-Varnish-Can-Cache;
        if (req.request == "GET" && obj.status < 400 && !(req.url ~ "^/dnsman-admin") && !(req.url ~ "^/dnsman-media")) {
      	    set obj.ttl = 4h;
       	    deliver;
    	}
    }
}

#Below is a commented-out copy of the default VCL logic.  If you
#redefine any of these subroutines, the built-in logic will be
#appended to your code.
#
#sub vcl_recv {
#    if (req.request != "GET" &&
#      req.request != "HEAD" &&
#      req.request != "PUT" &&
#      req.request != "POST" &&
#      req.request != "TRACE" &&
#      req.request != "OPTIONS" &&
#      req.request != "DELETE") {
#        /* Non-RFC2616 or CONNECT which is weird. */
#        return (pipe);
#    }
#    if (req.request != "GET" && req.request != "HEAD") {
#        /* We only deal with GET and HEAD by default */
#        return (pass);
#    }
#    if (req.http.Authorization || req.http.Cookie) {
#        /* Not cacheable by default */
#        return (pass);
#    }
#    return (lookup);
#}
#
#sub vcl_pipe {
#    # Note that only the first request to the backend will have
#    # X-Forwarded-For set.  If you use X-Forwarded-For and want to
#    # have it set for all requests, make sure to have:
#    # set req.http.connection = "close";
#    # here.  It is not set by default as it might break some broken web
#    # applications, like IIS with NTLM authentication.
#    return (pipe);
#}
#
#sub vcl_pass {
#    return (pass);
#}
#
#sub vcl_hash {
#    set req.hash += req.url;
#    if (req.http.host) {
#        set req.hash += req.http.host;
#    } else {
#        set req.hash += server.ip;
#    }
#    return (hash);
#}
#
#sub vcl_hit {
#    if (!obj.cacheable) {
#        return (pass);
#    }
#    return (deliver);
#}
#
#sub vcl_miss {
#    return (fetch);
#}
#
#sub vcl_fetch {
#    if (!obj.cacheable) {
#        return (pass);
#    }
#    if (obj.http.Set-Cookie) {
#        return (pass);
#    }
#    set obj.prefetch =  -30s;
#    return (deliver);
#}
#
#sub vcl_deliver {
#    return (deliver);
#}
#
#sub vcl_discard {
#    /* XXX: Do not redefine vcl_discard{}, it is not yet supported */
#    return (discard);
#}
#
#sub vcl_prefetch {
#    /* XXX: Do not redefine vcl_prefetch{}, it is not yet supported */
#    return (fetch);
#}
#
#sub vcl_timeout {
#    /* XXX: Do not redefine vcl_timeout{}, it is not yet supported */
#    return (discard);
#}
#
#sub vcl_error {
#    set obj.http.Content-Type = "text/html; charset=utf-8";
#    synthetic {"
#<?xml version="1.0" encoding="utf-8"?>
#<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
# "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
#<html>
#  <head>
#    <title>"} obj.status " " obj.response {"</title>
#  </head>
#  <body>
#    <h1>Error "} obj.status " " obj.response {"</h1>
#    <p>"} obj.response {"</p>
#    <h3>Guru Meditation:</h3>
#    <p>XID: "} req.xid {"</p>
#    <address>
#       <a href="http://www.varnish-cache.org/">Varnish</a>
#    </address>
#  </body>
#</html>
#"};
#    return (deliver);
#}
