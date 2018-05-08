import os
from setuptools import setup

import codenerix_invoicing

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-codenerix-invoicing',
    version=codenerix_invoicing.__version__,
    packages=["codenerix_invoicing"],
    include_package_data=True,
    zip_safe=False,
    license='Apache License Version 2.0',
    description='Codenerix Invoicing is a module that enables CODENERIX to manage bills.',
    long_description=README,
    url='https://github.com/codenerix/django-codenerix-invoicing',
    author=", ".join(codenerix_invoicing.__authors__),
    keywords=['django', 'codenerix', 'management', 'erp', 'crm', 'invoicing', 'sales', 'purchases', 'cash', 'cashdiary', 'diary'],
    platforms=['OS Independent'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django-codenerix',
        'django-codenerix-extensions',
        'django-codenerix-products',
        'django-codenerix-storages',
        'django-codenerix-pos',
        'xhtml2pdf==0.2b1',
    ]
)
