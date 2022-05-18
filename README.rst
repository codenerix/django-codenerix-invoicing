==========================
django-codenerix-invoicing
==========================

Codenerix Invoicing is a module that enables `CODENERIX <https://www.codenerix.com/>`_  to manage bills.

.. image:: https://github.com/codenerix/django-codenerix/raw/master/codenerix/static/codenerix/img/codenerix.png
    :target: https://www.codenerix.com
    :alt: Try our demo with Codenerix Cloud

*********
Changelog
*********

2018-01-17 - Codenerix Invoicing v1.x is incompatible with v2.x, `what has changed and how to migrate to v2.x? <https://github.com/codenerix/django-codenerix-invoicing/wiki/Codenerix-Invoicing-version-1.x-is-icompatible-with-2.x>`_.

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

    CDNX_INVOICING_LOGICAL_DELETION = True  # Mark registers as 'removed', but it doesn't really delete them.
    
    # Code format
    CDNX_INVOICING_CODE_FORMAT_BUDGET = 'B{year}{day}{month}-{hour}{minute}-{serial}-{pk}'
    CDNX_INVOICING_CODE_FORMAT_WISHLIST = 'W{year}{day}{month}-{hour}{minute}-{serial}-{pk}'
    CDNX_INVOICING_CODE_FORMAT_SHOPPINGCART = 'S{year}{day}{month}-{hour}{minute}-{serial}-{pk}'
    CDNX_INVOICING_CODE_FORMAT_ORDER = 'O{year}{day}{month}-{hour}{minute}-{serial}-{pk}'
    CDNX_INVOICING_CODE_FORMAT_ALBARAN = 'A{year}{day}{month}-{hour}{minute}-{serial}-{pk}'
    CDNX_INVOICING_CODE_FORMAT_TICKET = 'T{year}{day}{month}-{hour}{minute}-{serial}-{pk}'
    CDNX_INVOICING_CODE_FORMAT_TICKETRECTIFICATION = 'TR{year}{day}{month}-{hour}{minute}-{serial}-{pk}'
    CDNX_INVOICING_CODE_FORMAT_INVOICE = 'I{year}{day}{month}-{hour}{minute}-{serial}-{pk}'
    CDNX_INVOICING_CODE_FORMAT_INVOICERECTIFCATION = 'IT{year}{day}{month}-{hour}{minute}-{serial}-{pk}'

    CDNX_INVOICING_CURRENCY_MAX_DIGITS = 10  # 99.999.999,?
    CDNX_INVOICING_CURRENCY_DECIMAL_PLACES = 2  # ?,99

    # Force stock of products when you create SalesLines
    CDNX_INVOICING_FORCE_STOCK_IN_BUDGET = True

4. Since Codenerix Invoicing is a library, you only need to import its parts into your project and use them.

*************
Documentation
*************

Coming soon... do you help us?

You can get in touch with us `here <https://codenerix.com/contact/>`_.
