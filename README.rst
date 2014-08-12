devpi-findlinks: find-links view for devpi-server
=================================================

This plugin adds a new view to each index which lists all packages uploaded on that index or any index inherited except root/pypi.

Installation
------------

``devpi-findlinks`` needs to be installed alongside ``devpi-server``.

You can install it with::

    pip install devpi-findlinks

There is no configuration needed as ``devpi-server`` will automatically discover the plugin through calling hooks using the setuptools entry points mechanism.

Usage
-----

In a default installation with a user named ``user1`` which has an index named ``dev``, the view would be accessible at ``http://localhost:3141/user1/dev/+findlinks``.

Use such an url with the ``--find-links`` option of ``pip`` or ``easy_install``.

The view uses absolute URLs, to make it possible to use this view via proxy at any location for migration of old environments.
