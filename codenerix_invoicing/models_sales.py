# -*- coding: utf-8 -*-
#
# django-codenerix-invoicing
#
# Copyright 2017 Centrologic Computational Logistic Center S.L.
#
# Project URL : http://www.codenerix.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import datetime
from decimal import Decimal

from django.db import models, transaction
from django.db.models import Q, F
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from codenerix.middleware import get_current_user
from codenerix.models import GenInterface, CodenerixModel
from codenerix.models_people import GenRole
from codenerix_extensions.helpers import get_external_method
from codenerix_extensions.files.models import GenDocumentFile

from codenerix_invoicing.models import Haulier, BillingSeries, TypeDocument
from codenerix_invoicing.models_purchases import PAYMENT_DETAILS
from codenerix_invoicing.settings import CDNX_INVOICING_PERMISSIONS

from codenerix_pos.models import POSSlot, POS

from codenerix_products.models import ProductFinal, TypeTax, ProductUnique
# from codenerix_storages.models import Storage
from codenerix_payments.models import PaymentRequest, Currency

from codenerix_invoicing.exceptions import SalesLinesProductFinalIsSample, SalesLinesUniqueProductNotExists, SalesLinesInsufficientStock, SalesLinesNotModifiable, SalesLinesNotDelete


CURRENCY_MAX_DIGITS = getattr(settings, 'CDNX_INVOICING_CURRENCY_MAX_DIGITS', 10)
CURRENCY_DECIMAL_PLACES = getattr(settings, 'CDNX_INVOICING_CURRENCY_DECIMAL_PLACES', 2)

ROLE_BASKET_SHOPPINGCART = 'SC'
ROLE_BASKET_BUDGET = 'BU'
ROLE_BASKET_WISHLIST = 'WL'

ROLE_BASKET = (
    (ROLE_BASKET_SHOPPINGCART, _("Shopping cart")),
    (ROLE_BASKET_BUDGET, _("Budget")),
    (ROLE_BASKET_WISHLIST, _("Wish list")),
)

STATUS_BUDGET_PENDING_PAYMENT = 'PP'
STATUS_BUDGET_PAYMENT_ACCETED = 'PA'
STATUS_BUDGET_DRAFT = 'DR'

STATUS_BUDGET = (
    (STATUS_BUDGET_DRAFT, _("Draft")),
    (STATUS_BUDGET_PENDING_PAYMENT, _("Pending payment")),
    (STATUS_BUDGET_PAYMENT_ACCETED, _("Payment accepted")),
)

STATUS_ORDER_PENDING = 'PE'
STATUS_ORDER_PAYMENT_ACCEPTED = 'PA'
STATUS_ORDER_SENT = 'SE'
STATUS_ORDER_DELIVERED = 'DE'
STATUS_ORDER = (
    (STATUS_ORDER_PENDING, _("Pending")),
    (STATUS_ORDER_PAYMENT_ACCEPTED, _("Payment accepted")),
    (STATUS_ORDER_SENT, _("Sent")),
    (STATUS_ORDER_DELIVERED, _("Delivered")),
)


STATUS_WISHLIST_PUBLIC = 'PU'
STATUS_WISHLIST = (
    (STATUS_WISHLIST_PUBLIC, _('Public')),
    ('PR', _('Private')),
)

TYPE_PRIORITY_MEDIUM = 'L'
TYPE_PRIORITIES = (
    ('XS', _('Muy baja')),
    ('S', _('Baja')),
    (TYPE_PRIORITY_MEDIUM, _('Media')),
    ('XL', _('Alta')),
    ('XXL', _('Urgente')),
)

STATUS_PRINTER_DOCUMENT_TEMPORARY = 'TM'
STATUS_PRINTER_DOCUMENT_DEFINITVE = 'DF'
STATUS_PRINTER_DOCUMENT = (
    (STATUS_PRINTER_DOCUMENT_TEMPORARY, _('Temporary')),
    (STATUS_PRINTER_DOCUMENT_DEFINITVE, _('Definitive')),
)


class ABSTRACT_GenCustomer(models.Model):  # META: Abstract class

    class Meta(object):
        abstract = True


class Customer(GenRole, CodenerixModel):
    class CodenerixMeta:
        abstract = ABSTRACT_GenCustomer
        rol_groups = {
            'Customer': CDNX_INVOICING_PERMISSIONS['customer'],
        }
        rol_permissions = [
            'add_city',
            'add_citygeonameen',
            'add_citygeonamees',
            'add_continent',
            'add_continentgeonameen',
            'add_continentgeonamees',
            'add_corporateimage',
            'add_country',
            'add_countrygeonameen',
            'add_countrygeonamees',
            'add_customer',
            'add_customerdocument',
            'add_person',
            'add_personaddress',
            'add_province',
            'add_provincegeonameen',
            'add_provincegeonamees',
            'add_region',
            'add_regiongeonameen',
            'add_regiongeonamees',
            'add_salesbasket',
            'add_timezone',
            'change_city',
            'change_citygeonameen',
            'change_citygeonamees',
            'change_continent',
            'change_continentgeonameen',
            'change_continentgeonamees',
            'change_corporateimage',
            'change_country',
            'change_countrygeonameen',
            'change_countrygeonamees',
            'change_customer',
            'change_customerdocument',
            'change_person',
            'change_personaddress',
            'change_province',
            'change_provincegeonameen',
            'change_provincegeonamees',
            'change_region',
            'change_regiongeonameen',
            'change_regiongeonamees',
            'change_salesbasket',
            'change_timezone',
            'change_user',
            'delete_city',
            'delete_citygeonameen',
            'delete_citygeonamees',
            'delete_continent',
            'delete_continentgeonameen',
            'delete_continentgeonamees',
            'delete_corporateimage',
            'delete_country',
            'delete_countrygeonameen',
            'delete_countrygeonamees',
            'delete_customer',
            'delete_customerdocument',
            'delete_person',
            'delete_personaddress',
            'delete_province',
            'delete_provincegeonameen',
            'delete_provincegeonamees',
            'delete_region',
            'delete_regiongeonameen',
            'delete_regiongeonamees',
            'delete_salesbasket',
            'delete_timezone ',
            'list_billingseries',
            'list_city',
            'list_continent',
            'list_corporateimage',
            'list_country',
            'list_customer',
            'list_customerdocument',
            'list_legalnote',
            'list_personaddress',
            'list_productdocument',
            'list_province',
            'list_purchaseslineinvoice',
            'list_region',
            'list_salesalbaran',
            'list_salesbasket',
            'list_salesinvoice',
            'list_salesinvoicerectification',
            'list_salesorder',
            'list_salesticket',
            'list_salesticketrectification',
            'list_timezone',
            'list_typedocument',
            'list_typedocumenttexten',
            'list_typedocumenttextes',
            'view_billingseries',
            'view_city',
            'view_continent',
            'view_corporateimage',
            'view_country',
            'view_customer',
            'view_customerdocument',
            'view_legalnote',
            'view_personaddress',
            'view_province',
            'view_region',
            'view_salesbasket',
            'view_timezone',
            'view_typedocument',
            'view_typedocumenttexten',
            'view_typedocumenttextes',
        ]

        force_methods = {
            'foreignkey_customer': ('CDNX_get_fk_info_customer', _('---')),
            'get_email': ('CDNX_get_email', ),
            'info_customer_details': ('CDNX_get_details_info_customer', ),
        }

    currency = models.ForeignKey(Currency, related_name='customers', verbose_name='Currency', on_delete=models.CASCADE)
    # serie de facturacion
    billing_series = models.ForeignKey(BillingSeries, related_name='customers', verbose_name='Billing series', on_delete=models.CASCADE)
    # datos de facturación
    # saldo final
    final_balance = models.CharField(_("Balance"), max_length=250, blank=True, null=True)
    # credito o riesgo maximo autorizado
    credit = models.CharField(_("Credit"), max_length=250, blank=True, null=True)
    # Aplicar recargo de equivalencia
    apply_equivalence_surcharge = models.BooleanField(_("Apply equivalence surcharge"), blank=False, default=False)
    # Tipo de iva
    type_tax = models.ForeignKey(TypeTax, related_name='customers', verbose_name=_("Type tax"), null=True, on_delete=models.CASCADE)
    default_customer = models.BooleanField(_("Default customer"), blank=False, default=False)

    @staticmethod
    def foreignkey_external():
        return get_external_method(Customer, Customer.CodenerixMeta.force_methods['foreignkey_customer'][0])

    def __str__(self):
        if hasattr(self, 'external'):
            return u"{}".format(smart_text(self.external))
        else:
            return "{}".format(self.pk)

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('final_balance', _("Balance")))
        fields.append(('credit', _("Credit")))
        fields.append(('currency', _("Currency")))
        fields.append(('billing_series', _("Billing series")))
        fields.append(('apply_equivalence_surcharge', _("Equivalence Surcharge")))
        fields.append(('type_tax', _("Type tax")))
        fields.append(('default_customer', _("Default customer")))
        fields = get_external_method(Customer, '__fields_customer__', info, fields)
        return fields

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.default_customer:
                Customer.objects.exclude(pk=self.pk).update(default_customer=False)
            else:
                if not Customer.objects.exclude(pk=self.pk).filter(default_customer=True).exists():
                    self.default_customer = True
        return super(Customer, self).save(*args, **kwargs)

    def buy_product(self, product_pk):
        """
        determina si el customer ha comprado un producto
        """
        if self.invoice_sales.filter(lines_sales__product_final__pk=product_pk).exists() \
                or self.ticket_sales.filter(lines_sales__product_final__pk=product_pk).exists():
            return True
        else:
            return False


# customers
class GenCustomer(GenInterface, ABSTRACT_GenCustomer):  # META: Abstract class
    customer = models.OneToOneField(Customer, related_name='external', verbose_name=_("Customer"), null=True, on_delete=models.SET_NULL, blank=True)

    class Meta(GenInterface.Meta, ABSTRACT_GenCustomer.Meta):
        abstract = True

    @classmethod
    def permissions(cls):
        # group = 'Customer'
        # perms = []
        # print(cls.customer.field.related_model)

        return None

        # print({group: {'gperm': None, 'dperm': perms, 'model': None},})


class ABSTRACT_GenAddress(models.Model):  # META: Abstract class
    class Meta(object):
        abstract = True


class Address(CodenerixModel):

    class CodenerixMeta:
        abstract = ABSTRACT_GenAddress
        force_methods = {
            'foreignkey_address_delivery': ('CDNX_get_fk_info_address_delivery', _('---')),
            'foreignkey_address_invoice': ('CDNX_get_fk_info_address_invoice', _('---')),
            'get_summary': ('get_summary', ),
            'get_address': ('get_address', ),
            'get_zipcode': ('get_zipcode', ),
            'get_city': ('get_city', ),
            'get_province': ('get_province', ),
            'get_country': ('get_country', ),
        }

    def __str__(self):
        if hasattr(self, 'external_delivery'):
            return u"{}".format(smart_text(self.external_delivery.get_summary()))
        elif hasattr(self, 'external_invoice'):
            return u"{}".format(smart_text(self.external_invoice.get_summary()))
        else:
            return 'No data!'

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        if hasattr(self, 'external_delivery'):
            fields.append(('external_delivery', _("Address delivery")))
        elif hasattr(self, 'external_invoice'):
            fields.append(('external_invoice', _("Address invoice")))
        else:
            raise Exception(_('Address unkown'))
        return fields

    @staticmethod
    def foreignkey_external_delivery():
        return get_external_method(Address, Address.CodenerixMeta.force_methods['foreignkey_address_delivery'][0])

    @staticmethod
    def foreignkey_external_invoice():
        return get_external_method(Address, Address.CodenerixMeta.force_methods['foreignkey_address_invoice'][0])


class GenAddress(GenInterface, ABSTRACT_GenAddress):  # META: Abstract class
    class Meta(GenInterface.Meta, ABSTRACT_GenAddress.Meta):
        abstract = True

    def save(self, *args, **kwargs):
        if hasattr(self, 'address_delivery') and self.address_delivery is None:
            address_delivery = Address()
            address_delivery.save()
        elif hasattr(self, 'address_delivery'):
            address_delivery = self.address_delivery

        if hasattr(self, 'address_invoice') and self.address_invoice is None:
            address_invoice = Address()
            address_invoice.save()
        elif hasattr(self, 'address_invoice'):
            address_invoice = self.address_invoice

        if hasattr(self, 'address_delivery'):
            self.address_delivery = address_delivery
        if hasattr(self, 'address_invoice'):
            self.address_invoice = address_invoice
        return super(GenAddress, self).save(*args, **kwargs)


# address delivery
class GenAddressDelivery(GenAddress):  # META: Abstract class
    class Meta(object):
        abstract = True
    address_delivery = models.OneToOneField(Address, related_name='external_delivery', verbose_name=_("Address delivery"), null=True, on_delete=models.SET_NULL, blank=True, editable=False)


# address invoice
class GenAddressInvoice(GenAddress):  # META: Abstract class
    class Meta(object):
        abstract = True
    address_invoice = models.OneToOneField(Address, related_name='external_invoice', verbose_name=_("Address invoice"), null=True, on_delete=models.SET_NULL, blank=True, editable=False)


# documentos de clientes
class CustomerDocument(CodenerixModel, GenDocumentFile):
    customer = models.ForeignKey(Customer, related_name='customer_documents', verbose_name=_("Customer"), on_delete=models.CASCADE)
    type_document = models.ForeignKey('TypeDocument', related_name='customer_documents', verbose_name=_("Type document"), null=True, on_delete=models.CASCADE)

    def __str__(self):
        return u"{}".format(smart_text(self.customer))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('customer', _("Customer")))
        fields.append(('type_document', _("Type document")))
        return fields


# #####################################
# ######## VENTAS #####################
# #####################################
# GenVersion
class GenVersion(CodenerixModel):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True
        unique_together = (("code", "parent_pk"))

    # número de versión del documento
    # version = models.IntegerField(_("Version"), blank=False, null=False)
    # indica si la versión esta bloqueada
    lock = models.BooleanField(_("Lock"), blank=False, default=False)
    # pk de la versión original
    parent_pk = models.IntegerField(_("Parent pk"), blank=True, null=True)
    code = models.CharField(_("Code"), max_length=64, blank=False, null=False)
    code_counter = models.IntegerField(_("Code counter"), blank=False, null=False, editable=False)
    date = models.DateTimeField(_("Date"), blank=False, null=False, default=timezone.now)
    observations = models.TextField(_("Observations"), max_length=256, blank=True, null=True)
    """
    si al guardar una linea asociada a un documento bloqueado (lock==True), duplicar el documento en una nueva versión
    """
    # additional information
    subtotal = models.DecimalField(_("Subtotal"), blank=False, null=False, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, default=0, editable=False)
    discounts = models.FloatField(_("Discounts"), blank=False, null=False, default=0, editable=False)
    taxes = models.FloatField(_("Taxes"), blank=False, null=False, default=0, editable=False)
    equivalence_surcharges = models.FloatField(_("Equivalence surcharge"), blank=False, null=False, default=0, editable=False)
    total = models.DecimalField(_("Total"), blank=False, null=False, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, default=0, editable=False)
    # logical deletion
    removed = models.BooleanField(_("Removed"), blank=False, default=False, editable=False)

    def setcode(self):
        model = self._meta.model
        code_key = None
        if model == SalesBasket:
            code_format = {}
            code_format[ROLE_BASKET_BUDGET] = 'CDNX_INVOICING_CODE_FORMAT_BUDGET'
            code_format[ROLE_BASKET_WISHLIST] = 'CDNX_INVOICING_CODE_FORMAT_WISHLIST'
            code_format[ROLE_BASKET_SHOPPINGCART] = 'CDNX_INVOICING_CODE_FORMAT_SHOPPINGCART'
        elif model == SalesOrder:
            code_key = 'CDNX_INVOICING_CODE_FORMAT_ORDER'
            code_format = getattr(settings, code_key, None)
        elif model == SalesAlbaran:
            code_key = 'CDNX_INVOICING_CODE_FORMAT_ALBARAN'
            code_format = getattr(settings, code_key, None)
        elif model == SalesTicketRectification:
            code_key = 'CDNX_INVOICING_CODE_FORMAT_TICKET'
            code_format = getattr(settings, code_key, None)
        elif model == SalesTicketRectification:
            code_key = 'CDNX_INVOICING_CODE_FORMAT_TICKETRECTIFICATION'
            code_format = getattr(settings, code_key, None)
        elif model == SalesInvoice:
            code_key = 'CDNX_INVOICING_CODE_FORMAT_INVOICE'
            code_format = getattr(settings, code_key, None)
        elif model == SalesInvoiceRectification:
            code_key = 'CDNX_INVOICING_CODE_FORMAT_INVOICERECTIFCATION'
            code_format = getattr(settings, code_key, None)
        else:
            code_format = None

        if code_format:
            billing_series = getattr(self, 'billing_series', None)
            if billing_series is None:
                customer = self.get_customer()
                self.billing_series = customer.billing_series

            now = datetime.datetime.now()
            values = {
                'year': now.year,
                'day': now.day,
                'month': now.month,
                'hour': now.hour,
                'minute': now.minute,
                'second': now.second,
                'microsecond': now.microsecond,
                'quarter': now.month // 4 + 1,
                'serial': self.billing_series,
                'number': self.code_counter,
            }
            if isinstance(code_format, dict):
                role = getattr(self, 'role', None)
                if role and role in code_format and hasattr(settings, code_format[role]):
                    code_format = getattr(settings, code_format[role], None)
                    if code_format:
                        code_str = code_format.format(**values)
                    else:
                        raise Exception(_("{} undefined".format(code_format['role'])))
                else:
                    raise Exception(_("Can not determine code, rol undefined"))
            else:
                try:
                    code_str = code_format.format(**values)
                except KeyError as e:
                    raise KeyError("We have detected that you are using the unknow key {} in '{}'. Available keys are: {}".format(e, code_key, ", ".join(values.keys())))
        else:
            code_str = self.code_counter

        # Set new code to this object
        self.code = code_str

    def save(self, *args, **kwargs):
        # Check force save
        if 'force_save' in kwargs:
            force_save = kwargs.pop('force_save')
            if force_save:
                # Brake here and go as usually
                return super(GenVersion, self).save(*args, **kwargs)

        make_code = False
        if self.pk:
            obj = self._meta.model.objects.get(pk=self.pk)

            #####################
            # En esta sección compruebo si solo se bloquea o si es un cambio.
            #####################
            # Var for check if change must duplicate or only its locking the instance.
            need_duplicate = False

            # Itero por todas las claves
            for key in self.__dict__.keys():
                # Si la clave está en obj, no es block y no es un atributo propio de self (empieza por _) comprueba si son iguales.
                if key in obj.__dict__ and key not in ['lock', 'role', 'updated', 'code', 'created'] and not key.startswith("_"):
                    if need_duplicate is False:
                        # Si son iguales, need_duplicate se mantendrá a false. Solo se activa si son distintos.
                        if type(self.__dict__[key]) == datetime.datetime and obj.__dict__[key]:
                            need_duplicate = self.__dict__[key].strftime("%Y-%m-%d %H:%M") != obj.__dict__[key].strftime("%Y-%m-%d %H:%M")
                        else:
                            need_duplicate = self.__dict__[key] != obj.__dict__[key]
                    else:
                        break

            #####################
            # Fin de comprobacion
            #####################

            # Si está bloqueado y además se ha cambiado algo más, además del lock, se duplica
            if obj.lock is True and need_duplicate is True:
                # parent pk
                if self.parent_pk is None:
                    self.parent_pk = self.pk

                # Reset object so it will create a new copy
                self.pk = None
                self.lock = False
                make_code = True
        else:
            # New register
            make_code = True

        # If we should make a new code
        if make_code:
            with transaction.atomic():
                # Find new code_counter
                model = self._meta.model
                last = model.objects.filter(
                    date__gte=timezone.datetime(self.date.year, 1, 1),
                    date__lt=timezone.datetime(self.date.year + 1, 1, 1)
                ).order_by("-code_counter").first()

                # Check if we found a result
                if last:
                    # Add one more
                    self.code_counter = last.code_counter + 1
                else:
                    # This is the first one
                    self.code_counter = 1

                # Create new code
                self.setcode()

                # Save
                result = super(GenVersion, self).save(*args, **kwargs)
        else:
            result = super(GenVersion, self).save(*args, **kwargs)

        # Return result
        return result

    def delete(self):
        if not hasattr(settings, 'CDNX_INVOICING_LOGICAL_DELETION') or settings.CDNX_INVOICING_LOGICAL_DELETION is False:
            return super(GenVersion, self).delete()
        else:
            self.removed = True
            self.save(force_save=True)

    def update_totales(self, force_save=True):
        # calculate totals and save
        totales = self.calculate_price_doc_complete()
        self.subtotal = totales['subtotal']
        self.total = totales['total']
        self.discounts = sum(totales['discounts'].values())
        self.taxes = sum(totales['taxes'].values())
        self.equivalence_surcharges = sum(totales['equivalence_surcharges'].values())
        if force_save:
            self.save()

    def calculate_price_doc_complete(self, queryset=None, details=False):
        # calculate totals with details
        if queryset:
            subtotal = Decimal("0")
            tax = {}
            discount = {}
            equivalence_surcharges = {}
            total = Decimal("0")
            for line in queryset:
                subtotal += line.subtotal

                if hasattr(line, 'tax'):
                    if line.tax not in tax:
                        if not details:
                            tax[line.tax] = Decimal("0")
                        else:
                            tax[line.tax] = {
                                'label': line.tax_label,
                                'amount': Decimal("0")
                            }
                    price_tax = Decimal(line.taxes)
                    if not details:
                        tax[line.tax] += price_tax
                    else:
                        tax[line.tax]['amount'] += price_tax
                else:
                    price_tax = Decimal("0")

                if hasattr(line, 'equivalence_surcharge'):
                    if line.equivalence_surcharge:
                        if line.equivalence_surcharge not in equivalence_surcharges:
                            equivalence_surcharges[line.equivalence_surcharge] = Decimal("0")

                        equivalence_surcharge = line.subtotal * Decimal(self.equivalence_surcharge / 100.0)
                        equivalence_surcharges[line.equivalence_surcharge] = equivalence_surcharge
                    else:
                        equivalence_surcharge = Decimal("0")
                else:
                    equivalence_surcharge = Decimal("0")

                if hasattr(line, 'discount'):
                    if str(line.discount) not in discount:
                        discount[str(line.discount)] = Decimal("0")
                    price_discount = Decimal(line.discounts)
                    discount[str(line.discount)] += price_discount
                else:
                    price_discount = Decimal("0")

                total += line.subtotal - price_discount + price_tax + equivalence_surcharge

            return {'subtotal': subtotal, 'taxes': tax, 'total': total, 'discounts': discount, 'equivalence_surcharges': equivalence_surcharges}
        else:
            return {'subtotal': 0, 'taxes': {}, 'total': 0, 'discounts': {}, 'equivalence_surcharges': {}}

    def print_counter(self, user):
        # Add new register in the print counter and return the number of impressions definitives
        raise Exception("Method 'print_counter()' don't implemented")

    def get_customer(self):
        # returns the client associated with the document
        raise Exception(_("Method 'get_customer()' don't implemented. ({})".format(self._meta.model_name)))


# facturas rectificativas
class GenInvoiceRectification(GenVersion):  # META: Abstract class
    class Meta(GenVersion.Meta):
        abstract = True

    def __str__(self):
        return u"{}".format(smart_text(self.code))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        fields.append(('total', _('Total')))
        return fields

# ############################


# nueva cesta de la compra
class SalesBasket(GenVersion):
    customer = models.ForeignKey(Customer, related_name='basket_sales', verbose_name=_("Customer"), on_delete=models.CASCADE)
    pos = models.ForeignKey(POS, related_name='basket_sales', verbose_name=_("Point of Sales"), blank=True, null=True, on_delete=models.CASCADE)
    pos_slot = models.ForeignKey(POSSlot, related_name='basket_sales', verbose_name=_("POS Slot"), blank=True, null=True, on_delete=models.CASCADE)
    address_delivery = models.ForeignKey(Address, related_name='order_sales_delivery', verbose_name=_("Address delivery"), blank=True, null=True, on_delete=models.CASCADE)
    address_invoice = models.ForeignKey(Address, related_name='order_sales_invoice', verbose_name=_("Address invoice"), blank=True, null=True, on_delete=models.CASCADE)
    haulier = models.ForeignKey(Haulier, related_name='basket_sales', verbose_name=_("Haulier"), blank=True, null=True, on_delete=models.CASCADE)
    billing_series = models.ForeignKey(BillingSeries, related_name='basket_sales', verbose_name='Billing series', blank=False, null=False, on_delete=models.CASCADE)

    role = models.CharField(_("Role basket"), max_length=2, choices=ROLE_BASKET, blank=False, null=False, default=ROLE_BASKET_SHOPPINGCART)
    signed = models.BooleanField(_("Signed"), blank=False, default=False)
    public = models.BooleanField(_("Public"), blank=False, default=False)
    payment = models.ManyToManyField(PaymentRequest, verbose_name=_(u"Payment Request"), blank=True, related_name='basket_sales')
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False)
    expiration_date = models.DateTimeField(_("Expiration date"), blank=True, null=True, editable=False)

    def __str__(self):
        return u"Order-{}".format(smart_text(self.code))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('customer', _('Customer')))
        fields.append(('name', _('Name')))
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        fields.append(('role', _('Role basket')))
        fields.append(('signed', _('Signed')))
        fields.append(('public', _('Public')))
        fields.append(('address_delivery', _('Address delivery')))
        fields.append(('address_invoice', _('Address invoice')))
        fields.append(('haulier', _('Haulier')))
        fields.append(('subtotal', _('Subtotal')))
        fields.append(('discounts', _('Discounts')))
        fields.append(('taxes', _('Taxes')))
        fields.append(('total', _('Total')))
        fields.append(('lock', _('Locked')))
        return fields

    def pass_to_budget(self, lines=None):
        if self.role != ROLE_BASKET_BUDGET and lines and self.lines_sales.count() != len(lines):
            # duplicate object
            lines = [int(x) for x in lines]
            obj = copy.copy(self)
            obj.pk = None
            obj.role = ROLE_BASKET_BUDGET
            obj.save()
            for line in self.lines_sales.filter(pk__in=lines):
                new_line = copy.copy(line)
                new_line.pk = None  # reset
                new_line.basket = obj  # relation to new object
                new_line.save()
            return obj
        else:
            self.role = ROLE_BASKET_BUDGET
            self.save()
            return self

    def pass_to_shoppingcart(self):
        self.role = ROLE_BASKET_SHOPPINGCART
        self.save()
        return self

    def pass_to_order(self, payment_request=None):
        raise Exception("pass_to_order")
        """
        context = {
            'error': None,
            'order': None
        }
        if not hasattr(self, 'order_sales'):
            try:
                with transaction.atomic():
                    if type(payment_request) == int:
                        payment_request = PaymentRequest.objects.get(pk=payment_request)

                    order = SalesOrder()
                    order.customer = self.customer
                    order.budget = self
                    order.payment = payment_request
                    if order.payment and order.payment.is_paid():
                        order.status_order = STATUS_ORDER_PAYMENT_ACCEPTED
                    order.save()

                    if self.pos:
                        pos = self.pos
                    else:
                        pos = POS.objects.filter(default=True).first()

                    if pos is None:
                        raise IntegrityError(_('POS by default not found'))

                    for line in self.line_basket_sales.all():
                        if line.product.product.feature_special and line.product.product.feature_special.unique:
                            news_lines = range(line.quantity)
                            quantity = 1
                        else:
                            news_lines = [0, ]
                            quantity = line.quantity

                        for counter in news_lines:
                            lorder = SalesLineOrder()
                            lorder.order = order
                            lorder.line_budget = line
                            lorder.product = line.product
                            lorder.product_unique = line.product.book_product(pos, quantity)
                            lorder.price_recommended = line.price_recommended
                            lorder.description = line.description
                            lorder.discount = line.discount
                            lorder.price_base = line.price_base
                            lorder.tax = line.tax
                            lorder.equivalence_surcharge = line.equivalence_surcharge
                            lorder.quantity = quantity
                            lorder.save()

                    self.lock = True
                    self.role = ROLE_BASKET_BUDGET
                    self.expiration_date = None
                    self.save()
                context['order'] = self.order_sales
            except IntegrityError as e:
                context['error'] = str(e)
        else:
            context['order'] = self.order_sales

        return context
        """

    def lock_delete(self, request=None):
        # Solo se puede eliminar si:
        # * el pedido no tiene un pago realizado
        # * no se ha generado un albaran, ticket o factura relaciondos a una linea

        if hasattr(self, 'order_sales') and self.order_sales:
            if self.order_sales.payment is not None:
                return _('Cannot delete, it is related to payment')

            if self.lines_sales.filter(albaran__isnull=False).exists():
                return _('Cannot delete, it is related to albaran')
            if self.lines_sales.filter(ticket__isnull=False).exists():
                return _('Cannot delete, it is related to tickets')
            if self.lines_sales.filter(invoice__isnull=False).exists():
                return _('Cannot delete, it is related to invoices')

        return super(SalesBasket, self).lock_delete()

    def calculate_price_doc_complete(self, details=False):
        return super(SalesBasket, self).calculate_price_doc_complete(self.lines_sales.filter(removed=False), details)

    def list_tickets(self):
        raise Exception("list_tickets")
        # retorna todos los tickets en los que hay lineas de la cesta
        # return SalesTicket.objects.filter(line_ticket_sales__line_order__order__budget=self).distinct()

    def print_counter(self, user):
        raise Exception("print_counter")
        """
        obj = PrintCounterDocumentBasket()
        obj.basket = self
        obj.user = user
        obj.date = datetime.datetime.now()
        if self.lock:
            obj.status_document = STATUS_PRINTER_DOCUMENT_DEFINITVE
        else:
            obj.status_document = STATUS_PRINTER_DOCUMENT_TEMPORARY
        obj.save()
        return PrintCounterDocumentBasket.objects.filter(
            status_document=STATUS_PRINTER_DOCUMENT_DEFINITVE,
            basket=self
        ).count()
        """

    def get_customer(self):
        return self.customer

    @staticmethod
    def add_product(kind, product_pk, info_pack, quantity_str, customer, slot):
        raise Exception('add_product')
        """
        context = {'error': None}
        product_final = ProductFinal.objects.filter(pk=product_pk).first()

        if not product_final:
            context['error'] = _('Product invalid')
        else:
            is_pack = product_final.is_pack()
            if is_pack and info_pack is None:
                context['error'] = _('Pack info invalid')
            else:
                try:
                    info_pack = json.loads(info_pack)
                except ValueError:
                    context['error'] = _('Config pack invalid')
                except TypeError:
                    context['error'] = _('Config pack invalid')

                if is_pack and not info_pack:
                    context['error'] = _('There is not info about pack options')
                elif is_pack and len(info_pack) != product_final.productfinals_option.count():
                    context['error'] = _('There is not enought info about pack options')
                else:
                    if not quantity_str:
                        context['error'] = _('Quantity invalid')
                    else:
                        try:
                            quantity = float(quantity_str)
                        except ValueError:
                            quantity = None
                        if not quantity:
                            context['error'] = _('Quantity invalid')
                        elif product_final.product.force_stock:
                            if product_final.stock_real < quantity:
                                context['error'] = _('Insufficient stock')
                            elif product_final.is_pack():
                                for opt_pk in info_pack:
                                    product_final_option = ProductFinal.objects.filter(
                                        pk=info_pack[opt_pk],
                                        productfinals_optionpack__product_final=product_final,
                                        stock_real__lt=quantity
                                    ).exists()
                                    if product_final_option:
                                        context['error'] = _('Insufficient stock in option')
                                        break
        if context['error'] is None and product_final.product.force_stock:
            product_unique = ProductUnique.objects.filter(product_final=product_final).first()
            if not product_unique:
                context['error'] = _('Stock invalid')
        else:
            product_unique = None

        if context['error'] is None:
            try:
                with transaction.atomic():
                    basket = SalesBasket.objects.filter(
                        customer=customer,
                        pos_slot=slot,
                        lock=False,
                        role=kind,
                        removed=False
                    ).first()
                    if not basket:
                        basket = SalesBasket()
                        basket.billing_series = BillingSeries.objects.filter(default=True).first()
                        basket.customer = customer
                        basket.pos_slot = slot
                        basket.name = slot.name
                        basket.role = kind
                        basket.save()

                    line = SalesLineBasket.objects.filter(
                        basket=basket,
                        product=product_final,
                        removed=False
                    ).first()
                    is_new = False
                    if not line:
                        line = SalesLineBasket()
                        line.product = product_final
                        line.basket = basket
                        line.price_recommended = product_final.price
                        if product_final.code:
                            line.description = product_final.code
                        else:
                            line.description = product_final.product.code
                        line.discount = 0
                        line.price_base = product_final.price_base
                        line.tax = product_final.product.tax.tax
                        line.quantity = 0
                        is_new = True

                    line.quantity += quantity
                    line.save()

                    if product_unique:
                        # update stock
                        product_unique.stock_real -= quantity
                        product_unique.save()

                    if product_final.is_pack():
                        for opt_pk in info_pack:
                            opt = ProductFinalOption.objects.filter(
                                pk=opt_pk,
                                product_final=product_final
                            ).first()
                            pro = ProductFinal.objects.filter(
                                pk=info_pack[opt_pk],
                                productfinals_optionpack__product_final=product_final
                            ).first()

                            if opt and pro:
                                if is_new:
                                    rel = SalesLineBasketOption()
                                    rel.line_budget = line
                                    rel.product_option = opt
                                    rel.product_final = pro
                                    rel.quantity = quantity
                                    rel.save()
                                else:
                                    rel = SalesLineBasketOption.objects.filter(
                                        line_budget=line,
                                        product_option=opt,
                                        product_final=pro
                                    ).first()
                                    if rel:
                                        rel.quantity += quantity
                                        rel.save()
                                    else:
                                        rel = SalesLineBasketOption()
                                        rel.line_budget = line
                                        rel.product_option = opt
                                        rel.product_final = pro
                                        rel.quantity = quantity
                                        rel.save()
                                # update stock
                                product_unique = ProductUnique.objects.filter(product_final=pro).first()
                                if not product_unique:
                                    raise IntegrityError(_('Stock invalid'))
                                else:
                                    product_unique.stock_real -= quantity
                                    product_unique.save()
                            else:
                                context['error'] = _('Option pack invalid')
                                raise IntegrityError(_('Option pack invalid'))

                    context['basket'] = basket.pk
                    context['line'] = line.pk
                    context['price'] = float(line.total)
            except IntegrityError as e:
                context['error'] = str(e)

        return context
        """

    def duplicate(self, list_lines):
        new_budget = SalesBasket.objects.get(pk=self.pk)
        new_budget.lock = False
        new_budget.pk = None
        new_budget.save()
        for line in SalesLines.objects.filter(pk__in=list_lines):
            line.pk = None
            line.basket = new_budget
            line.save()
        return new_budget

    def delete(self):
        with transaction.atomic():
            SalesLines.delete_doc(self)
            return super(SalesBasket, self).delete()


# pedidos
class SalesOrder(GenVersion):
    budget = models.OneToOneField(SalesBasket, related_name='order_sales', verbose_name=_("Budget"), null=False, blank=False, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='order_sales', verbose_name=_("Customer"), on_delete=models.CASCADE)
    # storage = models.ForeignKey(Storage, related_name='order_sales', verbose_name=_("Storage"), blank=True, null=True, on_delete=models.CASCADE)
    payment = models.ForeignKey(PaymentRequest, related_name='order_sales', verbose_name=_(u"Payment Request"), blank=True, null=True, on_delete=models.CASCADE)
    number_tracking = models.CharField(_("Number of tracking"), max_length=128, blank=True, null=True)
    status_order = models.CharField(_("Status"), max_length=2, choices=STATUS_ORDER, blank=False, null=False, default='PE')
    payment_detail = models.CharField(_("Payment detail"), max_length=3, choices=PAYMENT_DETAILS, blank=True, null=True)
    source = models.CharField(_("Source of purchase"), max_length=250, blank=True, null=True)
    billing_series = models.ForeignKey(BillingSeries, related_name='order_sales', verbose_name='Billing series', blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return u"{}".format(smart_text(self.code))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('customer', _('Customer')))
        fields.append(('code', _('Code')))
        fields.append(('budget__code', _('Budget')))
        fields.append(('date', _('Date')))
        # fields.append(('storage', _('Storage')))
        fields.append(('status_order', None))
        fields.append(('get_status_order_display', _('Status')))
        fields.append(('get_payment_detail_display', _('Payment detail')))
        fields.append(('source', _('Source of purchase')))
        fields.append(('number_tracking', _('Number of tracking')))
        fields.append(('budget__address_delivery', _('Address delivery')))
        fields.append(('budget__address_invoice', _('Address invoice')))
        fields.append(('total', _('Total')))
        fields.append(('status_order', None))
        return fields

    def calculate_price_doc(self):
        return self.total

    def calculate_price_doc_complete(self, details=False):
        return super(SalesOrder, self).calculate_price_doc_complete(self.lines_sales.filter(removed=False), details)

    def print_counter(self, user):
        obj = PrintCounterDocumentOrder()
        obj.order = self
        obj.user = user
        obj.date = datetime.datetime.now()
        if self.lock:
            obj.status_document = STATUS_PRINTER_DOCUMENT_DEFINITVE
        else:
            obj.status_document = STATUS_PRINTER_DOCUMENT_TEMPORARY
        obj.save()
        return PrintCounterDocumentOrder.objects.filter(
            status_document=STATUS_PRINTER_DOCUMENT_DEFINITVE,
            order=self
        ).count()

    def get_customer(self):
        return self.customer

    def get_invoices(self, only_code=True):
        queryset = SalesLines.objects.filter(
            order=self,
            invoice__isnull=False,
            removed=False
        )
        if only_code:
            result = list(queryset.values('invoice__code', 'invoice__pk').distinct())
        else:
            result = queryset.distinct()
        return result

    def delete(self):
        with transaction.atomic():
            SalesLines.delete_doc(self)
            return super(SalesOrder, self).delete()


# documentos de pedidos
class SalesOrderDocument(CodenerixModel, GenDocumentFile):
    order = models.ForeignKey(SalesOrder, related_name='order_document_sales', verbose_name=_("Sales order"), on_delete=models.CASCADE)
    kind = models.ForeignKey(TypeDocument, related_name='order_document_sales', verbose_name=_('Document type'), blank=False, null=False, on_delete=models.CASCADE)
    notes = models.TextField(_("Notes"), max_length=256, blank=True, null=True)
    removed = models.BooleanField(_("Removed"), blank=False, default=False, editable=False)

    def __str__(self):
        return u'{}'.format(smart_text(self.name_file))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('kind', _('Document type')))
        fields.append(('name_file', _('Name')))
        return fields

    def delete(self):
        with transaction.atomic():
            if not hasattr(settings, 'CDNX_INVOICING_LOGICAL_DELETION') or settings.CDNX_INVOICING_LOGICAL_DELETION is False:
                return super(SalesLines, self).delete()
            else:
                self.removed = True
                self.save(force_save=True)


# albaranes
class SalesAlbaran(GenVersion):
    summary_delivery = models.TextField(_("Address delivery"), max_length=256, blank=True, null=True)
    billing_series = models.ForeignKey(BillingSeries, related_name='albaran_sales', verbose_name='Billing series', blank=False, null=False, on_delete=models.CASCADE)
    send = models.BooleanField(_("Send"), blank=False, default=False)

    def __str__(self):
        return u"{}".format(smart_text(self.code))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        fields.append(('summary_delivery', _('Address delivery')))
        fields.append(('total', _('Total')))
        return fields

    def calculate_price_doc(self):
        return self.total

    def calculate_price_doc_complete(self, details=False):
        return super(SalesAlbaran, self).calculate_price_doc_complete(self.lines_sales.filter(removed=False), details)

    def print_counter(self, user):
        obj = PrintCounterDocumentAlbaran()
        obj.albaran = self
        obj.user = user
        obj.date = datetime.datetime.now()
        if self.lock:
            obj.status_document = STATUS_PRINTER_DOCUMENT_DEFINITVE
        else:
            obj.status_document = STATUS_PRINTER_DOCUMENT_TEMPORARY
        obj.save()
        return PrintCounterDocumentAlbaran.objects.filter(
            status_document=STATUS_PRINTER_DOCUMENT_DEFINITVE,
            albaran=self
        ).count()

    def delete(self):
        with transaction.atomic():
            SalesLines.delete_doc(self)
            return super(SalesAlbaran, self).delete()


# ticket y facturas son lo mismo con un check de "tengo datos del customere"
class SalesTicket(GenVersion):
    customer = models.ForeignKey(Customer, related_name='ticket_sales', verbose_name=_("Customer"), on_delete=models.CASCADE)
    billing_series = models.ForeignKey(BillingSeries, related_name='ticket_sales', verbose_name='Billing series', blank=False, null=False, on_delete=models.CASCADE)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='order_sales', verbose_name=_("User"))

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user = get_current_user()
        return super(SalesTicket, self).save(*args, **kwargs)

    def __str__(self):
        return u"Ticket-{}".format(smart_text(self.code))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('customer', _('Customer')))
        fields.append(('code', _('Code')))
        fields.append(('lines_sales__product_final', _('Products')))
        fields.append(('date', _('Date')))
        fields.append(('total', _('Total')))
        return fields

    def calculate_price_doc(self):
        return self.total

    def calculate_price_doc_complete(self, details=False):
        return super(SalesTicket, self).calculate_price_doc_complete(self.lines_sales.filter(removed=False), details)

    def print_counter(self, user):
        obj = PrintCounterDocumentTicket()
        obj.ticket = self
        obj.user = user
        obj.date = datetime.datetime.now()
        if self.lock:
            obj.status_document = STATUS_PRINTER_DOCUMENT_DEFINITVE
        else:
            obj.status_document = STATUS_PRINTER_DOCUMENT_TEMPORARY
        obj.save()
        return PrintCounterDocumentTicket.objects.filter(
            status_document=STATUS_PRINTER_DOCUMENT_DEFINITVE,
            ticket=self
        ).count()

    def get_customer(self):
        return self.customer

    def delete(self):
        with transaction.atomic():
            SalesLines.delete_doc(self)
            return super(SalesTicket, self).delete()


# puede haber facturas o tickets rectificativos
# factura rectificativa
class SalesTicketRectification(GenInvoiceRectification):
    ticket = models.ForeignKey(SalesTicket, related_name='ticketrectification_sales', verbose_name=_("Ticket"), null=True, on_delete=models.CASCADE)
    billing_series = models.ForeignKey(BillingSeries, related_name='ticketrectification_sales', verbose_name='Billing series', blank=False, null=False, on_delete=models.CASCADE)

    def __fields__(self, info):
        fields = super(SalesTicketRectification, self).__fields__(info)
        fields.insert(0, ('ticket', _("Ticket")))
        fields.insert(0, ('ticket__customer', _("Customer")))
        return fields

    def calculate_price_doc(self):
        return self.total

    def calculate_price_doc_complete(self, details=False):
        return super(SalesTicketRectification, self).calculate_price_doc_complete(self.lines_sales.filter(removed=False), details)

    def print_counter(self, user):
        obj = PrintCounterDocumentTicketRectification()
        obj.ticket_rectification = self
        obj.user = user
        obj.date = datetime.datetime.now()
        if self.lock:
            obj.status_document = STATUS_PRINTER_DOCUMENT_DEFINITVE
        else:
            obj.status_document = STATUS_PRINTER_DOCUMENT_TEMPORARY
        obj.save()
        return PrintCounterDocumentTicketRectification.objects.filter(
            status_document=STATUS_PRINTER_DOCUMENT_DEFINITVE,
            ticket_rectification=self
        ).count()

    def delete(self):
        with transaction.atomic():
            SalesLines.delete_doc(self)
            return super(SalesTicketRectification, self).delete()


# facturas
# una factura puede contener varios ticket o albaranes
class SalesInvoice(GenVersion):
    customer = models.ForeignKey(Customer, related_name='invoice_sales', verbose_name=_("Customer"), on_delete=models.CASCADE)
    summary_invoice = models.TextField(_("Address invoice"), max_length=256, blank=True, null=True)
    billing_series = models.ForeignKey(BillingSeries, related_name='invoice_sales', verbose_name='Billing series', on_delete=models.CASCADE)

    def __str__(self):
        return u"{}".format(smart_text(self.code))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('customer', _('Customer')))
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        fields.append(('billing_series', _('Billing series')))
        fields.append(('summary_invoice', _('Address invoice')))
        fields.append(('total', _('Total')))
        return fields

    def calculate_price_doc(self):
        return self.total

    def calculate_price_doc_complete(self, details=False):
        return super(SalesInvoice, self).calculate_price_doc_complete(self.lines_sales.filter(removed=False), details)

    def get_customer(self):
        return self.customer

    def print_counter(self, user):
        obj = PrintCounterDocumentInvoice()
        obj.invoice = self
        obj.user = user
        obj.date = datetime.datetime.now()
        if self.lock:
            obj.status_document = STATUS_PRINTER_DOCUMENT_DEFINITVE
        else:
            obj.status_document = STATUS_PRINTER_DOCUMENT_TEMPORARY
        obj.save()
        return PrintCounterDocumentInvoice.objects.filter(
            status_document=STATUS_PRINTER_DOCUMENT_DEFINITVE,
            invoice=self
        ).count()

    def delete(self):
        with transaction.atomic():
            SalesLines.delete_doc(self)
            return super(SalesInvoice, self).delete()


# factura rectificativa
class SalesInvoiceRectification(GenInvoiceRectification):
    invoice = models.ForeignKey(SalesInvoice, related_name='invoicerectification_sales', verbose_name=_("Invoice"), null=True, on_delete=models.CASCADE)
    billing_series = models.ForeignKey(BillingSeries, related_name='invoicerectification_sales', verbose_name='Billing series', blank=False, null=False, on_delete=models.CASCADE)

    def __fields__(self, info):
        fields = super(SalesInvoiceRectification, self).__fields__(info)
        fields.insert(0, ('invoice', _("Invoices")))
        fields.insert(0, ('invoice__customer', _("Customer")))
        return fields

    def calculate_price_doc(self):
        return self.total

    def calculate_price_doc_complete(self, details=False):
        return super(SalesInvoiceRectification, self).calculate_price_doc_complete(self.lines_sales.filter(removed=False), details)

    def print_counter(self, user):
        obj = PrintCounterDocumentInvoiceRectification()
        obj.invoice_rectification = self
        obj.user = user
        obj.date = datetime.datetime.now()
        if self.lock:
            obj.status_document = STATUS_PRINTER_DOCUMENT_DEFINITVE
        else:
            obj.status_document = STATUS_PRINTER_DOCUMENT_TEMPORARY
        obj.save()
        return PrintCounterDocumentInvoiceRectification.objects.filter(
            status_document=STATUS_PRINTER_DOCUMENT_DEFINITVE,
            invoice_rectification=self
        ).count()

    def delete(self):
        with transaction.atomic():
            SalesLines.delete_doc(self)
            return super(SalesInvoiceRectification, self).delete()


# #############################################
class SalesLines(CodenerixModel):
    basket = models.ForeignKey(SalesBasket, related_name='lines_sales', verbose_name=_("Basket"), on_delete=models.CASCADE)
    tax_basket_fk = models.ForeignKey(TypeTax, related_name='lines_sales_basket', verbose_name=_("Tax Basket"), on_delete=models.CASCADE)
    order = models.ForeignKey(SalesOrder, related_name='lines_sales', verbose_name=_("Sales order"), on_delete=models.CASCADE, null=True, blank=True)
    tax_order_fk = models.ForeignKey(TypeTax, related_name='lines_sales_order', verbose_name=_("Tax Sales order"), on_delete=models.CASCADE, null=True, blank=True)
    albaran = models.ForeignKey(SalesAlbaran, related_name='lines_sales', verbose_name=_("Albaran"), on_delete=models.CASCADE, null=True, blank=True)
    ticket = models.ForeignKey(SalesTicket, related_name='lines_sales', verbose_name=_("Ticket"), on_delete=models.CASCADE, null=True, blank=True)
    tax_ticket_fk = models.ForeignKey(TypeTax, related_name='lines_sales_ticket', verbose_name=_("Tax Ticket"), on_delete=models.CASCADE, null=True, blank=True)
    ticket_rectification = models.ForeignKey(SalesTicketRectification, related_name='lines_sales', verbose_name=_("Ticket rectification"), on_delete=models.CASCADE, null=True, blank=True)
    invoice = models.ForeignKey(SalesInvoice, related_name='lines_sales', verbose_name=_("Invoice"), on_delete=models.CASCADE, null=True, blank=True)
    tax_invoice_fk = models.ForeignKey(TypeTax, related_name='lines_sales_invoice', verbose_name=_("Tax Invoice"), on_delete=models.CASCADE, null=True, blank=True)
    invoice_rectification = models.ForeignKey(SalesInvoiceRectification, related_name='lines_sales', verbose_name=_("Invoice rectification"), on_delete=models.CASCADE, null=True, blank=True)
    product_final = models.ForeignKey(ProductFinal, related_name='lines_sales', verbose_name=_("Product"), on_delete=models.CASCADE)
    product_unique = models.ForeignKey(ProductUnique, related_name='lines_sales', verbose_name=_("Product Unique"), on_delete=models.CASCADE, null=True, blank=True)
    # invoiced is True if 'invoice' is not null
    # invoiced = models.BooleanField(_("Invoiced"), blank=False, default=False)
    # logical deletion
    removed = models.BooleanField(_("Removed"), blank=False, default=False, editable=False)

    quantity = models.FloatField(_("Quantity"), blank=False, null=False)

    # additional information
    subtotal = models.DecimalField(_("Subtotal"), blank=False, null=False, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, default=0, editable=False)
    discounts = models.DecimalField(_("Discounts"), blank=False, null=False, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, default=0, editable=False)
    taxes = models.DecimalField(_("Taxes"), blank=False, null=False, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, default=0, editable=False)
    equivalence_surcharges = models.DecimalField(_("Equivalence surcharge"), blank=True, null=True, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, default=0)
    total = models.DecimalField(_("Total"), blank=False, null=False, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, default=0, editable=False)

    code = models.CharField(_("Code"), max_length=250, blank=True, null=True, default=None)
    # ####
    # desde el formulario se podrá modificar el precio y la descripcion del producto
    # se guarda el tax usado y la relacion para poder hacer un seguimiento
    # ####
    # info basket
    price_recommended_basket = models.DecimalField(_("Recomended price base"), blank=True, null=True, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES)
    description_basket = models.CharField(_("Description"), max_length=256, blank=True, null=True)
    price_base_basket = models.DecimalField(_("Price base"), blank=False, null=False, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES)
    discount_basket = models.DecimalField(_("Discount (%)"), blank=False, null=False, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, default=0)
    tax_basket = models.FloatField(_("Tax (%)"), blank=True, null=True, default=0)
    equivalence_surcharge_basket = models.FloatField(_("Equivalence surcharge (%)"), blank=True, null=True, default=0)
    tax_label_basket = models.CharField(_("Tax Name"), max_length=250, blank=True, null=True)
    notes_basket = models.CharField(_("Notes"), max_length=256, blank=True, null=True)
    # info order
    price_recommended_order = models.DecimalField(_("Recomended price base"), blank=True, null=True, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES)
    description_order = models.CharField(_("Description"), max_length=256, blank=True, null=True)
    price_base_order = models.DecimalField(_("Price base"), blank=True, null=True, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES)
    discount_order = models.DecimalField(_("Discount (%)"), blank=True, null=True, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, default=0)
    tax_order = models.FloatField(_("Tax (%)"), blank=True, null=True, default=0)
    equivalence_surcharge_order = models.FloatField(_("Equivalence surcharge (%)"), blank=True, null=True, default=0)
    tax_label_order = models.CharField(_("Tax Name"), max_length=250, blank=True, null=True)
    notes_order = models.CharField(_("Notes"), max_length=256, blank=True, null=True)
    # info albaran - basic
    notes_albaran = models.CharField(_("Notes"), max_length=256, blank=True, null=True)
    # info ticket
    price_recommended_ticket = models.DecimalField(_("Recomended price base"), blank=True, null=True, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES)
    description_ticket = models.CharField(_("Description"), max_length=256, blank=True, null=True)
    price_base_ticket = models.DecimalField(_("Price base"), blank=True, null=True, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES)
    discount_ticket = models.DecimalField(_("Discount (%)"), blank=True, null=True, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, default=0)
    tax_ticket = models.FloatField(_("Tax (%)"), blank=True, null=True, default=0)
    equivalence_surcharge_ticket = models.FloatField(_("Equivalence surcharge (%)"), blank=True, null=True, default=0)
    tax_label_ticket = models.CharField(_("Tax Name"), max_length=250, blank=True, null=True)
    notes_ticket = models.CharField(_("Notes"), max_length=256, blank=True, null=True)
    # info ticket rectification - basic
    notes_ticket_rectification = models.CharField(_("Notes"), max_length=256, blank=True, null=True)
    # info invoice
    price_recommended_invoice = models.DecimalField(_("Recomended price base"), blank=True, null=True, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES)
    description_invoice = models.CharField(_("Description"), max_length=256, blank=True, null=True)
    price_base_invoice = models.DecimalField(_("Price base"), blank=True, null=True, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES)
    discount_invoice = models.DecimalField(_("Discount (%)"), blank=True, null=True, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, default=0)
    tax_invoice = models.FloatField(_("Tax (%)"), blank=True, null=True, default=0)
    equivalence_surcharge_invoice = models.FloatField(_("Equivalence surcharge (%)"), blank=True, null=True, default=0)
    tax_label_invoice = models.CharField(_("Tax Name"), max_length=250, blank=True, null=True)
    notes_invoice = models.CharField(_("Notes"), max_length=256, blank=True, null=True)
    # info invoice rectification - basic
    notes_invoice_rectification = models.CharField(_("Notes"), max_length=256, blank=True, null=True)

    def __str__(self):
        return u"{} - {}".format(self.product_final, self.quantity)

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('product_final', _("Product final")))
        fields.append(('product_unique', _("Product unique")))
        fields.append(('quantity', _("Quantity")))
        return fields

    def get_product_unique(self, quantity, pos=None):
        if self.product_final.sample:
            raise SalesLinesProductFinalIsSample(_("This product can not be sold, it is marked as 'sample'"))
        else:
            products_unique = []
            with transaction.atomic():
                qs = ProductUnique.objects.filter(
                    product_final=self.product_final,
                    stock_real__gt=0,
                    stock_locked__lt=F('stock_real')
                )
                if pos:
                    qs = qs.filter(box__box_structure__zone__storage__in=pos.storage_stock.filter(storage_zones__salable=True))
                elif self.basket.pos:
                    qs = qs.filter(box__box_structure__zone__storage__in=self.basket.pos.storage_stock.filter(storage_zones__salable=True))

                if self.product_final.product.force_stock is False:
                    product_unique = qs.first()
                    if product_unique:
                        products_unique = [
                            {
                                'quantity': quantity,
                                'product_unique': product_unique
                            }
                        ]
                    else:
                        raise SalesLinesUniqueProductNotExists(_('Unique product not exists!'))
                else:
                    stock_available = None
                    for unique_product in qs:
                        if quantity <= 0:
                            break
                        stock_available = unique_product.stock_real - unique_product.stock_locked
                        if stock_available > quantity:
                            stock_available = quantity
                            unique_product.duplicate(quantity)
                        unique_product.locked_stock(stock_available)

                        products_unique.append({
                            'product_unique': unique_product,
                            'quantity': stock_available
                        })
                        quantity -= stock_available

                    if quantity > 0:
                        raise SalesLinesInsufficientStock(_("Insufficient stock"))
                    else:
                        return products_unique

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk is None:
                if self.product_final.code:
                    self.code = self.product_final.code
                else:
                    self.code = self.product_final.product.code

                if self.product_unique is None:
                    if getattr(settings, 'CDNX_INVOICING_FORCE_STOCK_IN_BUDGET', True):
                        products_unique = self.get_product_unique(self.quantity)
                        first = True
                        for unique_product in products_unique:
                            if first:
                                first = False
                                self.quantity = unique_product['quantity']
                                self.product_unique = unique_product['product_unique']
                            else:
                                line = copy.copy(self)
                                line.pk = None
                                line.quantity = unique_product['quantity']
                                line.product_unique = unique_product['product_unique']
                                line.save()

            elif self.pk:
                line_old = SalesLines.objects.filter(pk=self.pk).first()
                if line_old:
                    product_final_old = line_old.product_final
                else:
                    product_final_old = None

                if self.product_final != product_final_old:
                    if self.order or self.albaran or self.ticket or self.invoice:
                        raise SalesLinesNotModifiable(_('You can not modify product'))
                    elif self.description_basket == '{}'.format(product_final_old):
                        self.description_basket = ''

                    # solo se puede cambiar el producto si no esta en un pedido, albaran, ticket o factura
                    self.price_recommended_basket = None
                    self.tax_label_basket = None
                    if getattr(settings, 'CDNX_INVOICING_FORCE_STOCK_IN_BUDGET', True):
                        products_unique = self.get_product_unique(self.quantity)
                        first = True
                        for unique_product in products_unique:
                            if first:
                                first = False
                                self.quantity = unique_product['quantity']
                                self.product_unique = unique_product['product_unique']
                            else:
                                line = copy.copy(self)
                                line.pk = None
                                line.quantity = unique_product['quantity']
                                line.product_unique = unique_product['product_unique']
                                line.save()
                    else:
                        self.product_unique = None
                elif self.order and line_old.order is None:
                    # associate line with order
                    # locked product unique!!
                    if self.product_final.product.force_stock:
                        if self.product_unique is None:
                            products_unique = self.get_product_unique(self.quantity)
                            first = True
                            for unique_product in products_unique:
                                if first:
                                    first = False
                                    self.quantity = unique_product['quantity']
                                    self.product_unique = unique_product['product_unique']
                                else:
                                    line = copy.copy(self)
                                    line.pk = None
                                    line.quantity = unique_product['quantity']
                                    line.product_unique = unique_product['product_unique']
                                    line.save()
                        else:
                            available = self.product_unique.stock_real - self.product_unique.stock_locked
                            if available < self.quantity:
                                products_unique = self.get_product_unique(self.quantity)
                                first = True
                                for unique_product in products_unique:
                                    if first:
                                        first = False
                                        self.quantity = unique_product['quantity']
                                        self.product_unique = unique_product['product_unique']
                                    else:
                                        line = copy.copy(self)
                                        line.pk = None
                                        line.quantity = unique_product['quantity']
                                        line.product_unique = unique_product['product_unique']
                                        line.save()

            # calculate value of equivalence_surcharge
            # save tax label
            # save price recommended
            # save tax foreignkey
            if self.basket:
                if self.tax_basket_fk is None:
                    self.tax_basket_fk = self.product_final.product.tax
                if self.tax_label_basket is None:
                    self.tax_label_basket = self.product_final.product.tax.name
                if not self.tax_basket:
                    self.tax_basket = self.product_final.product.tax.tax
                if self.basket.get_customer().apply_equivalence_surcharge:
                    self.equivalence_surcharge_basket = self.basket.get_customer().tax.recargo_equivalencia
                if self.price_recommended_basket is None:
                    self.price_recommended_basket = self.product_final.price_base
                if not self.description_basket:
                    self.description_basket = '{}'.format(self.product_final)
            if self.order:
                if self.tax_order_fk is None:
                    self.tax_order_fk = self.product_final.product.tax
                if self.tax_label_order is None:
                    self.tax_label_order = self.product_final.product.tax.name
                if not self.tax_order:
                    self.tax_order = self.product_final.product.tax.tax
                if self.order.get_customer().apply_equivalence_surcharge:
                    self.equivalence_surcharge_order = self.order.get_customer().tax.recargo_equivalencia
                if self.price_recommended_order is None:
                    self.price_recommended_order = self.product_final.price_base
                if not self.description_order:
                    self.description_order = '{}'.format(self.product_final)
            if self.ticket:
                if self.tax_ticket_fk is None:
                    self.tax_ticket_fk = self.product_final.product.tax
                if self.tax_label_ticket is None:
                    self.tax_label_ticket = self.product_final.product.tax.name
                if not self.tax_ticket:
                    self.tax_ticket = self.product_final.product.tax.tax
                if self.ticket.get_customer().apply_equivalence_surcharge:
                    self.equivalence_surcharge_ticket = self.ticket.get_customer().tax.recargo_equivalencia
                if self.price_recommended_ticket is None:
                    self.price_recommended_ticket = self.product_final.price_base
                if not self.description_ticket:
                    self.description_ticket = '{}'.format(self.product_final)
            if self.invoice:
                if self.tax_invoice_fk is None:
                    self.tax_invoice_fk = self.product_final.product.tax
                if self.tax_label_invoice is None:
                    self.tax_label_invoice = self.product_final.product.tax.name
                if not self.tax_invoice:
                    self.tax_invoice = self.product_final.product.tax.tax
                if self.invoice.get_customer().apply_equivalence_surcharge:
                    self.equivalence_surcharge_invoice = self.invoice.get_customer().tax.recargo_equivalencia
                if self.price_recommended_invoice is None:
                    self.price_recommended_invoice = self.product_final.price_base
                if not self.description_invoice:
                    self.description_invoice = '{}'.format(self.product_final)

            result = super(self._meta.model, self).save(*args, **kwargs)
            # update totals
            if self.order:
                self.order.update_totales()
            if self.albaran:
                self.albaran.update_totales()
            if self.ticket:
                self.ticket.update_totales()
            if self.ticket_rectification:
                self.ticket_rectification.update_totales()
            if self.invoice:
                self.invoice.update_totales()
            if self.invoice_rectification:
                self.invoice_rectification.update_totales()
            return result

    def delete(self):
        with transaction.atomic():
            if not hasattr(settings, 'CDNX_INVOICING_LOGICAL_DELETION') or settings.CDNX_INVOICING_LOGICAL_DELETION is False:
                return super(SalesLines, self).delete()
            else:
                self.removed = True
                self.save()

    def __limitQ__(self, info):
        return {'removed': Q(removed=False)}

    @staticmethod
    def delete_doc(doc):
        if isinstance(doc, SalesBasket):
            qs = doc.lines_sales.filter(Q(order__isnull=False) | Q(albaran__isnull=False) | Q(ticket__isnull=False) | Q(invoice__isnull=False)).exists()
            if qs:
                raise SalesLinesNotDelete(_('No se puede eliminar el presupuesto al estar relacionado con pedido, albaran, ticket o factura'))
            else:
                with transaction.atomic():
                    doc.lines_sales.objects.filter(removed=False).delete()
        elif isinstance(doc, SalesOrder):
            qs = doc.lines_sales.filter(Q(albaran__isnull=False) | Q(ticket__isnull=False) | Q(invoice__isnull=False)).exists()
            if qs:
                raise SalesLinesNotDelete(_('No se puede eliminar el presupuesto al estar relacionado con albaran, ticket o factura'))
            else:
                with transaction.atomic():
                    for line in doc.lines_sales.filter(removed=False):
                        nline = copy.copy(line)
                        nline.pk = None
                        nline.order = None
                        nline.save()
                        line.delete()
        elif isinstance(doc, SalesAlbaran):
            qs = doc.lines_sales.filter(Q(ticket__isnull=False) | Q(invoice__isnull=False)).exists()
            if qs:
                raise SalesLinesNotDelete(_('No se puede eliminar el presupuesto al estar relacionado ticket o factura'))
            else:
                with transaction.atomic():
                    for line in doc.lines_sales.filter(removed=False):
                        nline = copy.copy(line)
                        nline.pk = None
                        nline.albaran = None
                        nline.save()
                        line.delete()
        elif isinstance(doc, SalesTicket):
            qs = doc.lines_sales.filter(Q(ticket_rectification__isnull=False)).exists()
            if qs:
                raise SalesLinesNotDelete(_('No se puede eliminar el presupuesto al estar relacionado con ticket rectificativos'))
            else:
                with transaction.atomic():
                    for line in doc.lines_sales.filter(removed=False):
                        nline = copy.copy(line)
                        nline.pk = None
                        nline.ticket = None
                        nline.save()
                        line.delete()
        elif isinstance(doc, SalesTicketRectification):
            with transaction.atomic():
                for line in doc.lines_sales.filter(removed=False):
                    nline = copy.copy(line)
                    nline.pk = None
                    nline.ticket_rectification = None
                    nline.save()
                    line.delete()
        elif isinstance(doc, SalesInvoice):
            qs = doc.lines_sales.filter(Q(invoice_rectification__isnull=False)).exists()
            if qs:
                raise SalesLinesNotDelete(_('No se puede eliminar el presupuesto al estar relacionado con factura rectificativos'))
            else:
                with transaction.atomic():
                    for line in doc.lines_sales.filter(removed=False):
                        nline = copy.copy(line)
                        nline.pk = None
                        nline.invoice = None
                        nline.save()
                        line.delete()
        elif isinstance(doc, SalesInvoiceRectification):
            with transaction.atomic():
                for line in doc.lines_sales.filter(removed=False):
                    nline = copy.copy(line)
                    nline.pk = None
                    nline.invoice_rectification = None
                    nline.save()
                    line.delete()

    @staticmethod
    def create_document_from_another(pk, list_lines,
                                     MODEL_SOURCE, MODEL_FINAL,
                                     url_reverse,
                                     msg_error_relation, msg_error_not_found, msg_error_line_not_found,
                                     unique):
        """
        pk: pk del documento origen
        list_lines: listado de pk de lineas de origen
        MODEL_SOURCE: modelo del documento origen
        MODEL_FINAL: model del documento final
        url_reverse: url del destino
        msg_error_relation: Mensaje de error indicando que las lineas ya están relacionadas
        msg_error_not_found: Mensaje de error indicando que no se encuentra el objeto origen
        unique: (True/False) Indica si puede haber más de una linea asociada a otras lineas
        """
        context = {}
        obj_src = MODEL_SOURCE.objects.filter(pk=pk).first()
        if list_lines and obj_src:
            # parse to int
            list_lines = [int(x) for x in list_lines]

            obj_final = MODEL_FINAL()
            complete = True
            field_final_tax = None
            if isinstance(obj_final, SalesOrder):
                obj_final.budget = obj_src
                field_final = 'order'
                field_final_tax = 'tax_order_fk'
            elif isinstance(obj_final, SalesAlbaran):
                field_final = 'albaran'
                field_final_tax = 'tax_albaran_fk'
                complete = False
            elif isinstance(obj_final, SalesTicket):
                field_final = 'ticket'
                field_final_tax = 'tax_ticket_fk'
            elif isinstance(obj_final, SalesTicketRectification):
                field_final = 'ticket_rectification'
                complete = False
            elif isinstance(obj_final, SalesInvoice):
                field_final = 'invoice'
                field_final_tax = 'tax_invoice_fk'
            elif isinstance(obj_final, SalesInvoiceRectification):
                field_final = 'invoice_rectification'
                complete = False
            # list of lines objects
            if unique:
                create = not SalesLines.objects.filter(**{
                    "pk__in": list_lines,
                    "{}__isnull".format(field_final): False
                }).exists()
            else:
                create = True

            """
            si debiendo ser filas unicas no las encuentra en el modelo final, se crea el nuevo documento
            """
            if create:
                with transaction.atomic():
                    if hasattr(obj_src, 'customer'):
                        customer = obj_src.customer
                    else:
                        customer = obj_src.lines_sales.filter(removed=False).first().order.customer
                    obj_final.customer = customer
                    obj_final.date = datetime.datetime.now()
                    obj_final.billing_series = obj_src.billing_series

                    field_src_tax = None
                    if isinstance(obj_src, SalesBasket):
                        field_src = 'basket'
                        field_src_tax = 'tax_basket_fk'
                    elif isinstance(obj_src, SalesOrder) or isinstance(obj_src, SalesAlbaran):
                        field_src = 'order'
                        field_src_tax = 'tax_order_fk'
                    elif isinstance(obj_src, SalesTicket) or isinstance(obj_src, SalesTicketRectification):
                        field_src = 'ticket'
                        field_src_tax = 'tax_ticket_fk'
                    elif isinstance(obj_src, SalesInvoice) or isinstance(obj_src, SalesInvoiceRectification):
                        field_src = 'invoice'
                        field_src_tax = 'tax_invoice_fk'

                    obj_final.save()

                    qs = SalesLines.objects.filter(**{'pk__in': list_lines, '{}__isnull'.format(field_final): True})
                    if qs:
                        for line in qs:
                            setattr(line, field_final, obj_final)
                            if complete:
                                setattr(line, 'description_{}'.format(field_final), getattr(line, 'description_{}'.format(field_src)))
                                setattr(line, 'price_base_{}'.format(field_final), getattr(line, 'price_base_{}'.format(field_src)))
                                setattr(line, 'discount_{}'.format(field_final), getattr(line, 'discount_{}'.format(field_src)))
                                setattr(line, 'tax_{}'.format(field_final), getattr(line, 'tax_{}'.format(field_src)))
                                setattr(line, 'equivalence_surcharge_{}'.format(field_final), getattr(line, 'equivalence_surcharge_{}'.format(field_src)))
                                setattr(line, 'tax_label_{}'.format(field_final), getattr(line, 'tax_label_{}'.format(field_src)))
                            if field_src_tax and field_final_tax:
                                setattr(line, '{}'.format(field_final_tax), getattr(line, '{}'.format(field_src_tax)))

                            setattr(line, 'notes_{}'.format(field_final), getattr(line, 'notes_{}'.format(field_src)))

                            line.save()

                            """
                            FALTA LOS PACKS
                                if hasattr(line_src, 'line_basket_option_sales') and line_src.line_basket_option_sales.exists():
                                    for opt_src in line_src.line_basket_option_sales.all():
                                        opt_dst = SalesLineOrderOption()
                                        opt_dst.line_order = line_final
                                        opt_dst.product_option = opt_src.product_option
                                        opt_dst.product_final = opt_src.product_final
                                        opt_dst.quantity = opt_src.quantity
                                        opt_dst.save()
                            """

                        # bloqueamos el documento origen
                        obj_src.lock = True
                        obj_src.save()
                        # context['url'] = reverse('ordersaless_details', kwargs={'pk': order.pk})
                        context['url'] = "{}#/{}".format(reverse(url_reverse), obj_final.pk)
                        context['obj_final'] = obj_final
                    else:
                        context['error'] = msg_error_relation
            else:
                # _("Hay lineas asignadas a pedidos")
                context['error'] = msg_error_relation
        else:
            # _('Budget not found')
            context['error'] = msg_error_not_found

        return context

    @staticmethod  # ok
    def create_order_from_budget_all(order, signed_obligatorily=True):
        lines_budget = order.budget.lines_sales.filter(removed=False)
        lines = [x[0] for x in lines_budget.values_list('pk')]
        result = SalesLines.create_order_from_budget(order.pk, lines, signed_obligatorily)
        order = result['obj_final']

        return lines_budget.count() == order.lines_sales.filter(removed=False).count()

    @staticmethod  # ok
    def create_order_from_budget(pk, list_lines, signed_obligatorily=True):
        MODEL_SOURCE = SalesBasket
        MODEL_FINAL = SalesOrder
        url_reverse = 'CDNX_invoicing_ordersaless_list'
        # type_doc
        msg_error_relation = _("Hay lineas asignadas a pedidos")
        msg_error_not_found = _('Budget not found')
        msg_error_line_not_found = _('Todas las lineas ya se han pasado a pedido')

        budget = MODEL_SOURCE.objects.get(pk=pk)

        if signed_obligatorily and not budget.signed:
            # el presupuesto tiene que estar firmado para poder generar el pedido
            context = {}
            context['error'] = _("Unsigned budget!")
            return context
        else:
            # duplicamos el presupuesto si el numero de lineas es diferente
            # relacionando el pedido a este nuevo presupuesto
            if list_lines and len(list_lines) != SalesLines.objects.filter(removed=False, basket=pk).count():

                    new_budget = budget.duplicate(list_lines)
                    pk = new_budget.pk
                    list_lines = [x[0] for x in SalesLines.objects.filter(removed=False, basket=pk).values_list('pk')]

            return SalesLines.create_document_from_another(pk, list_lines,
                                                           MODEL_SOURCE, MODEL_FINAL, url_reverse,
                                                           msg_error_relation, msg_error_not_found, msg_error_line_not_found,
                                                           True)

    @staticmethod  # ok
    def create_albaran_automatic(pk, list_lines):
        """
        creamos de forma automatica el albaran
        """
        lines = SalesLines.objects.filter(pk__in=list_lines, removed=False).exclude(albaran__isnull=False).values_list('pk')
        lines_to_albaran = [x[0] for x in lines]
        SalesLines.create_albaran_from_order(pk, lines_to_albaran)

    @staticmethod
    def create_albaran_from_order(pk, list_lines):
        MODEL_SOURCE = SalesOrder
        MODEL_FINAL = SalesAlbaran
        url_reverse = 'CDNX_invoicing_albaransaless_list'
        # type_doc
        msg_error_relation = _("Hay lineas asignadas a albaranes")
        msg_error_not_found = _('Sales order not found')
        msg_error_line_not_found = _('Todas las lineas ya se han pasado a albaran')

        context = SalesLines.create_document_from_another(pk, list_lines, MODEL_SOURCE, MODEL_FINAL, url_reverse, msg_error_relation, msg_error_not_found, msg_error_line_not_found, False)

        # If there was not any error
        if 'error' not in context:
            # Get albaran
            albaran = context['obj_final']

            # Reserve stock
            try:
                with transaction.atomic():
                    # For each line
                    for line in albaran.lines_sales.all():
                        if line.product_unique:
                            # It is a unique product
                            pus = [line.product_unique]
                        else:
                            # It is not a unique product, get all of them
                            pus = line.product_final.products_unique.filter(stock_real__gt=F(stock_locked)):

                        # Reserve as many as we can
                        quantity = line.quantity
                        for pu in pus:
                            # Check how many are free and lock as many as we need
                            available = pu.stock_real - pu.stock_locked
                            # Choose how many we are going to lock
                            to_lock = min(available, quantity)
                            # Mark as locked
                            pu.stock_locked += to_lock
                            pu.save()
                            # Count down from quantity
                            quantity -= to_lock
                            # When we are done, break bucle
                            if not quantity:
                                break

                        # If we are not done
                        if quantity:
                            # Fail
                            raise IOError("Not enought products for line '{}'!".format(line))
            except IOError as e:

                # Remove all line's from albaran before failing
                for line in albaran.lines_sales.all():
                    line.delete()

                # Remove albaran before failing
                albaran.delete()

                # Set error
                context = {}
                context['error'] = e

        # Return result
        return context

    @staticmethod
    def create_ticket_from_order(pk, list_lines):
        MODEL_SOURCE = SalesOrder
        MODEL_FINAL = SalesTicket
        url_reverse = 'CDNX_invoicing_ticketsaless_list'
        # type_doc
        msg_error_relation = _("Hay lineas asignadas a ticket")
        msg_error_not_found = _('Sales order not found')
        msg_error_line_not_found = _('Todas las lineas ya se han pasado a ticket')

        with transaction.atomic():
            SalesLines.create_albaran_automatic(pk, list_lines)
            return SalesLines.create_document_from_another(pk, list_lines,
                                                           MODEL_SOURCE, MODEL_FINAL, url_reverse,
                                                           msg_error_relation, msg_error_not_found, msg_error_line_not_found,
                                                           False)

    @staticmethod
    def create_ticket_from_slot(slot_pk):
        context = {
            "error": None,
            "obj_final": None,
        }
        # order line not paid
        line_orders = SalesLines.objects.filter(
            order__budget__pos_slot__pk=slot_pk,
            order__payment__isnull=True,
            order__cash_movements__isnull=True,
            order__budget__removed=False,
            order__removed=False,
            removed=False
        )
        if line_orders:
            # create o update ticket
            tickets = []
            for line in line_orders:
                if line.ticket:
                    tickets.append(line.ticket)

            if len(set(tickets)) > 1:
                context['error'] = _(u'There are orders that are in several different tickets')
            else:
                if tickets:
                    # update line
                    with transaction.atomic():
                        ticket = SalesTicket.objects.get(pk=tickets[0], removed=False)
                        # There are already orders associated with a ticket
                        for line in line_orders:
                            if line.ticket is None:
                                line.ticket = ticket
                                line.tax_ticket = line.tax_order
                                line.discount_ticket = line.discount_order
                                line.description_ticket = line.description_order
                                line.notes_ticket = line.notes_order
                                line.quantity_ticket = line.quantity_order
                                line.price_recommended_ticket = line.price_recommended_order
                                line.price_base_ticket = line.price_base_order
                                line.save()
                            else:
                                # update line
                                if line.quantity_ticket != line.quantity_order:
                                    line.quantity_ticket = line.quantity_order
                                    line.save()
                else:
                    # new ticket
                    with transaction.atomic():
                        ticket = SalesTicket()
                        ticket.billing_series = BillingSeries.objects.filter(default=True).first()
                        ticket.customer = line_orders[0].order.customer
                        ticket.save()

                        for line in line_orders:
                            line.ticket = ticket
                            line.tax_ticket = line.tax_order
                            line.discount_ticket = line.discount_order
                            line.description_ticket = line.description_order
                            line.notes_ticket = line.notes_order
                            line.quantity_ticket = line.quantity_order
                            line.price_recommended_ticket = line.price_recommended_order
                            line.price_base_ticket = line.price_base_order
                            line.save()
                context['obj_final'] = ticket
        else:
            # get ticket
            line_order = SalesLines.objects.filter(
                order__budget__pos_slot__pk=slot_pk,
                order__budget__removed=False,
                order__removed=False,
                removed=False,
            ).last()
            ticket = SalesTicket.objects.filter(
                customer=line_order.order.customer,
                lines_sales=line_order,
                lines_sales__removed=False,
                removed=False
            ).first()
            if ticket:
                context['obj_final'] = ticket
            else:
                context['error'] = _("Ticket don't found")
        return context

    @staticmethod
    def create_invoice_from_order(pk, list_lines):
        MODEL_SOURCE = SalesOrder
        MODEL_FINAL = SalesInvoice
        url_reverse = 'CDNX_invoicing_invoicesaless_list'
        # type_doc
        msg_error_relation = _("Hay lineas asignadas a facturas")
        msg_error_not_found = _('Sales order not found')
        msg_error_line_not_found = _('Todas las lineas ya se han pasado a facturas')

        with transaction.atomic():
            SalesLines.create_albaran_automatic(pk, list_lines)
            return SalesLines.create_document_from_another(pk, list_lines,
                                                           MODEL_SOURCE, MODEL_FINAL, url_reverse,
                                                           msg_error_relation, msg_error_not_found, msg_error_line_not_found,
                                                           False)

    @staticmethod
    def create_ticket_from_albaran(pk, list_lines):
        MODEL_SOURCE = SalesAlbaran
        MODEL_FINAL = SalesTicket
        url_reverse = 'CDNX_invoicing_ticketsaless_list'
        # type_doc
        msg_error_relation = _("Hay lineas asignadas a ticket")
        msg_error_not_found = _('Sales albaran not found')
        msg_error_line_not_found = _('Todas las lineas ya se han pasado a ticket')

        return SalesLines.create_document_from_another(pk, list_lines,
                                                       MODEL_SOURCE, MODEL_FINAL, url_reverse,
                                                       msg_error_relation, msg_error_not_found, msg_error_line_not_found,
                                                       False)
        """
        context = {}
        if list_lines:
            new_list_lines = SalesLines.objects.filter(
                pk__in=[int(x) for x in list_lines]
            ).exclude(
                invoice__isnull=True
            ).values_list('pk')

            if new_list_lines:
                new_pk = SalesLines.objects.values_list('order__pk').filter(pk__in=new_list_lines).first()
                if new_pk:
                    context = SalesLines.create_ticket_from_order(new_pk, new_list_lines)
                    return context
                else:
                    error = _('Pedido no encontrado')
            else:
                error = _('Lineas no relacionadas con pedido')
        else:
            error = _('Lineas no seleccionadas')
        context['error'] = error
        return context
        """

    @staticmethod
    def create_invoice_from_albaran(pk, list_lines):
        MODEL_SOURCE = SalesAlbaran
        MODEL_FINAL = SalesInvoice
        url_reverse = 'CDNX_invoicing_invoicesaless_list'
        # type_doc
        msg_error_relation = _("Hay lineas asignadas a facturas")
        msg_error_not_found = _('Sales albaran not found')
        msg_error_line_not_found = _('Todas las lineas ya se han pasado a facturas')

        return SalesLines.create_document_from_another(pk, list_lines,
                                                       MODEL_SOURCE, MODEL_FINAL, url_reverse,
                                                       msg_error_relation, msg_error_not_found, msg_error_line_not_found,
                                                       False)
        """
        context = {}
        if list_lines:
            new_list_lines = SalesLines.objects.filter(
                pk__in=[int(x) for x in list_lines]
            ).exclude(
                invoice__isnull=False
            )

            if new_list_lines:
                new_pk = new_list_lines.first()
                if new_pk:
                    context = SalesLines.create_invoice_from_order(
                        new_pk.order.pk,
                        [x['pk'] for x in new_list_lines.values('pk')])
                    return context
                else:
                    error = _('Pedido no encontrado')
            else:
                error = _('Lineas no relacionadas con pedido')
        else:
            error = _('Lineas no seleccionadas')
        context['error'] = error
        return context
        """

    @staticmethod
    def create_invoice_from_ticket(pk, list_lines):
        MODEL_SOURCE = SalesTicket
        MODEL_FINAL = SalesInvoice
        url_reverse = 'CDNX_invoicing_invoicesaless_list'
        # type_doc
        msg_error_relation = _("Hay lineas asignadas a facturas")
        msg_error_not_found = _('Sales ticket not found')
        msg_error_line_not_found = _('Todas las lineas ya se han pasado a facturas')

        return SalesLines.create_document_from_another(pk, list_lines,
                                                       MODEL_SOURCE, MODEL_FINAL, url_reverse,
                                                       msg_error_relation, msg_error_not_found, msg_error_line_not_found,
                                                       False)
        """
                                context = {}
                                if list_lines:
                                    new_list_lines = SalesLines.objects.filter(
                                        pk__in=[int(x) for x in list_lines]
                                    ).exclude(
                                        invoice__isnull=True
                                    )
                                    if new_list_lines:
                                        new_pk = new_list_lines.first()
                                        if new_pk:
                                            context = SalesLines.create_invoice_from_order(
                                                new_pk.order.pk,
                                                [x['pk'] for x in new_list_lines.values('pk')])
                                            return context
                                        else:
                                            error = _('Pedido no encontrado')
                                    else:
                                        error = _('Lineas no relacionadas con pedido')
                                else:
                                    error = _('Lineas no seleccionadas')
                                context['error'] = error
                                return context
                        """


# #############################################
# Print counter per document
class PrintCounterDocument(CodenerixModel):  # META: Abstract class
    date = models.DateTimeField(_("Date"), blank=False, null=False, default=timezone.now, editable=False)
    status_document = models.CharField(_("Status document"), max_length=2, choices=STATUS_PRINTER_DOCUMENT, blank=False, null=False, default=STATUS_PRINTER_DOCUMENT_TEMPORARY)

    class Meta(object):
        abstract = True

    def __str__(self):
        return u"{} - {}  ({})".format(smart_text(self.date), smart_text(self.doc), smart_text(self.user))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('user', _("User")))
        fields.append(('date', _("Date")))
        fields.append(('get_status_document_display', _("Status document")))
        return fields


class PrintCounterDocumentBasket(PrintCounterDocument):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='print_counter_document_basket', verbose_name=_("User"), on_delete=models.CASCADE)
    basket = models.ForeignKey(SalesBasket, related_name='print_counter_document_basket', verbose_name=_("Document"), on_delete=models.CASCADE)


class PrintCounterDocumentOrder(PrintCounterDocument):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='print_counter_document_order', verbose_name=_("User"), on_delete=models.CASCADE)
    order = models.ForeignKey(SalesOrder, related_name='print_counter_document_order', verbose_name=_("Document"), on_delete=models.CASCADE)


class PrintCounterDocumentAlbaran(PrintCounterDocument):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='print_counter_document_albaran', verbose_name=_("User"), on_delete=models.CASCADE)
    albaran = models.ForeignKey(SalesAlbaran, related_name='print_counter_document_albaran', verbose_name=_("Document"), on_delete=models.CASCADE)


class PrintCounterDocumentTicket(PrintCounterDocument):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='print_counter_document_ticket', verbose_name=_("User"), on_delete=models.CASCADE)
    ticket = models.ForeignKey(SalesTicket, related_name='print_counter_document_ticket', verbose_name=_("Document"), on_delete=models.CASCADE)


class PrintCounterDocumentTicketRectification(PrintCounterDocument):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='print_counter_document_ticket_rectification', verbose_name=_("User"), on_delete=models.CASCADE)
    ticket_rectification = models.ForeignKey(SalesTicketRectification, related_name='print_counter_document_ticket_rectification', verbose_name=_("Document"), on_delete=models.CASCADE)


class PrintCounterDocumentInvoice(PrintCounterDocument):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='print_counter_document_invoice', verbose_name=_("User"), on_delete=models.CASCADE)
    invoice = models.ForeignKey(SalesInvoice, related_name='print_counter_document_invoice', verbose_name=_("Document"), on_delete=models.CASCADE)


class PrintCounterDocumentInvoiceRectification(PrintCounterDocument):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='print_counter_document_invoice_rectification', verbose_name=_("User"), on_delete=models.CASCADE)
    invoice_rectification = models.ForeignKey(SalesInvoiceRectification, related_name='print_counter_document_invoice_rectification', verbose_name=_("Document"), on_delete=models.CASCADE)


# Reason of modification
class ReasonModification(CodenerixModel):
    code = models.CharField(_("Code"), max_length=15, blank=False, null=False, unique=True)
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False)
    enable = models.BooleanField(_("Enable"), blank=True, default=True)

    def __str__(self):
        return u"{} ({})".format(smart_text(self.name), smart_text(self.code))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('code', _("Code")))
        fields.append(('name', _("Name")))
        fields.append(('enable', _("Enable")))
        return fields


# Relation between reason of modification and documents lines
class ReasonModificationLine(CodenerixModel):  # META: Abstract class
    date = models.DateTimeField(_("Date"), blank=False, null=False, default=timezone.now)
    quantity = models.FloatField(_("Quantity"), blank=False, null=False)

    class Meta(object):
        abstract = True

    def __str__(self):
        return u"{} - {}  ({})".format(smart_text(self.reason), smart_text(self.line), smart_text(self.quantity))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('user', _("User")))
        fields.append(('date', _("Date")))
        fields.append(('reason', _("Reason")))
        fields.append(('line', _("Line")))
        fields.append(('quantity', _("Quantity")))
        return fields

    def save(self, *args, **kwargs):
        if self.user is None:
            self.user = get_current_user()
        if self.date is None:
            self.date = datetime.datetime.now()
        return super(ReasonModificationLine, self).save(*args, **kwargs)


class ReasonModificationLineBasket(ReasonModificationLine):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reason_line_basket', verbose_name=_("User"), on_delete=models.CASCADE)
    reason = models.ForeignKey(ReasonModification, related_name='reason_line_basket', verbose_name=_("Reason"), on_delete=models.CASCADE)
    line = models.ForeignKey(SalesLines, related_name='reason_line_basket', verbose_name=_("Line"), on_delete=models.CASCADE)
    basket = models.ForeignKey(SalesBasket, related_name='reason_line_basket', verbose_name=_("Basket"), on_delete=models.CASCADE)


class ReasonModificationLineOrder(ReasonModificationLine):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reason_line_order', verbose_name=_("User"), on_delete=models.CASCADE)
    reason = models.ForeignKey(ReasonModification, related_name='reason_line_order', verbose_name=_("Reason"), on_delete=models.CASCADE)
    line = models.ForeignKey(SalesLines, related_name='reason_line_order', verbose_name=_("Line"), on_delete=models.CASCADE)
    order = models.ForeignKey(SalesOrder, related_name='reason_line_order', verbose_name=_("Order"), on_delete=models.CASCADE)


class ReasonModificationLineAlbaran(ReasonModificationLine):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reason_line_albaran', verbose_name=_("User"), on_delete=models.CASCADE)
    reason = models.ForeignKey(ReasonModification, related_name='reason_line_albaran', verbose_name=_("Reason"), on_delete=models.CASCADE)
    line = models.ForeignKey(SalesLines, related_name='reason_line_albaran', verbose_name=_("Line"), on_delete=models.CASCADE)
    albaran = models.ForeignKey(SalesAlbaran, related_name='reason_line_albaran', verbose_name=_("Albaran"), on_delete=models.CASCADE)


class ReasonModificationLineTicket(ReasonModificationLine):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reason_line_ticket', verbose_name=_("User"), on_delete=models.CASCADE)
    reason = models.ForeignKey(ReasonModification, related_name='reason_line_ticket', verbose_name=_("Reason"), on_delete=models.CASCADE)
    line = models.ForeignKey(SalesLines, related_name='reason_line_ticket', verbose_name=_("Line"), on_delete=models.CASCADE)
    ticket = models.ForeignKey(SalesTicket, related_name='reason_line_ticket', verbose_name=_("Ticket"), on_delete=models.CASCADE)


class ReasonModificationLineTicketRectification(ReasonModificationLine):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reason_line_ticket_rectification', verbose_name=_("User"), on_delete=models.CASCADE)
    reason = models.ForeignKey(ReasonModification, related_name='reason_line_ticket_rectification', verbose_name=_("Reason"), on_delete=models.CASCADE)
    line = models.ForeignKey(SalesLines, related_name='reason_line_ticket_rectification', verbose_name=_("Line"), on_delete=models.CASCADE)
    ticket_rectification = models.ForeignKey(SalesTicketRectification, related_name='reason_line_ticket_rectification', verbose_name=_("Ticket Rectification"), on_delete=models.CASCADE)


class ReasonModificationLineInvoice(ReasonModificationLine):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reason_line_invoice', verbose_name=_("User"), on_delete=models.CASCADE)
    reason = models.ForeignKey(ReasonModification, related_name='reason_line_invoice', verbose_name=_("Reason"), on_delete=models.CASCADE)
    line = models.ForeignKey(SalesLines, related_name='reason_line_invoice', verbose_name=_("Line"), on_delete=models.CASCADE)
    invoice = models.ForeignKey(SalesInvoice, related_name='reason_line_invoice', verbose_name=_("Invoice"), on_delete=models.CASCADE)


class ReasonModificationLineInvoiceRectification(ReasonModificationLine):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reason_line_invoice_rectification', verbose_name=_("User"), on_delete=models.CASCADE)
    reason = models.ForeignKey(ReasonModification, related_name='reason_line_invoice_rectification', verbose_name=_("Reason"), on_delete=models.CASCADE)
    line = models.ForeignKey(SalesLines, related_name='reason_line_invoice_rectification', verbose_name=_("Line"), on_delete=models.CASCADE)
    invoice_rectification = models.ForeignKey(SalesInvoiceRectification, related_name='reason_line_invoice_rectification', verbose_name=_("Invoice Rectification"), on_delete=models.CASCADE)
