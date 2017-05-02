==========================
django-codenerix-invoicing
==========================

Codenerix Invoicing is a module that enables `CODENERIX.com <http://www.codenerix.com/>`_  to manage bills.

.. image:: http://www.centrologic.com/wp-content/uploads/2017/01/logo-codenerix.png
    :target: http://www.codenerix.com
    :alt: Try our demo with Centrologic Cloud

****
Demo
****

Coming soon...

**********
Quickstart
**********

1. Install this package::

    For python 2: sudo pip2 install django-codenerix-invoicing
    For python 3: sudo pip3 install django-codenerix-invoicing

2. Add "codenerix_extensions", "codenerix_products", "codenerix_storages" and "codenerix_invoicing" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'codenerix_extensions',
        'codenerix_products',
        'codenerix_storages',
        'codenerix_invoicing',
    ]

3. Add the param in setting::

    CDNX_INVOICING_URL_COMMON = 'invoicing'
    CDNX_INVOICING_URL_PURCHASES = 'purchases'
    CDNX_INVOICING_URL_SALES = 'sales'

4. Since Codenerix Invoicing is a library, you only need to import its parts into your project and use them.

*************
Documentation
*************

Coming soon... do you help us? `Centrologic <http://www.centrologic.com/>`_

******************
Commercial support
******************

This project is backed by `Centrologic <http://www.centrologic.com/>`_. You can discover more in `CODENERIX.com <http://www.codenerix.com/>`_.
If you need help implementing or hosting django-codenerix-invoicing, please contact us:
http://www.centrologic.com/contacto/

.. image:: http://www.centrologic.com/wp-content/uploads/2015/09/logo-centrologic.png
    :target: http://www.centrologic.com
    :alt: Centrologic is supported mainly by Centrologic Computational Logistic Center
