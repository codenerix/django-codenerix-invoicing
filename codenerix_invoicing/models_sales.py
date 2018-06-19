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
from django.urls import reverse
from django.db import models, transaction, IntegrityError
from django.utils import timezone
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import Q

from codenerix.middleware import get_current_user
from codenerix.models import GenInterface, CodenerixModel
from codenerix.models_people import GenRole
from codenerix_extensions.helpers import get_external_method
from codenerix_extensions.files.models import GenDocumentFile

from codenerix_invoicing.models import Haulier, BillingSeries, TypeDocument
from codenerix_invoicing.models_purchases import PAYMENT_DETAILS
from codenerix_invoicing.settings import CDNX_INVOICING_PERMISSIONS

from codenerix_pos.models import POSSlot

from codenerix_products.models import ProductFinal, TypeTax, ProductFinalOption
from codenerix_storages.models import Storage
from codenerix_payments.models import PaymentRequest


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
STATUS_ORDER_CANCELLED = 'CA'
STATUS_ORDER = (
    (STATUS_ORDER_PENDING, _("Pending")),
    (STATUS_ORDER_PAYMENT_ACCEPTED, _("Payment accepted")),
    (STATUS_ORDER_SENT, _("Sent")),
    (STATUS_ORDER_DELIVERED, _("Delivered")),
    (STATUS_ORDER_CANCELLED, _("Cancelled")),
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
            'add_saleslinebasket',
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
            'change_saleslinebasket',
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
            'delete_saleslinebasket',
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
            'list_saleslinealbaran',
            'list_saleslinebasket',
            'list_saleslineinvoice',
            'list_saleslineinvoicerectification',
            'list_saleslineorder',
            'list_saleslineticket',
            'list_saleslineticketrectification',
            'list_salesorder',
            'list_salesreservedproduct',
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
            'view_saleslinebasket',
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

    currency = models.CharField(_("Currency"), max_length=250, blank=True, null=True)
    # serie de facturacion
    billing_series = models.ForeignKey(BillingSeries, related_name='billing_series', verbose_name='Billing series', on_delete=models.CASCADE)
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
        if self.invoice_sales.filter(line_invoice_sales__line_order__product__pk=product_pk).exists() \
                or self.ticket_sales.filter(line_ticket_sales__line_order__product__pk=product_pk).exists():
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
    subtotal = models.FloatField(_("Subtotal"), blank=False, null=False, default=0, editable=False)
    discounts = models.FloatField(_("Discounts"), blank=False, null=False, default=0, editable=False)
    taxes = models.FloatField(_("Taxes"), blank=False, null=False, default=0, editable=False)
    equivalence_surcharges = models.FloatField(_("Equivalence surcharge"), blank=False, null=False, default=0, editable=False)
    total = models.FloatField(_("Total"), blank=False, null=False, default=0, editable=False)
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
            subtotal = 0
            tax = {}
            discount = {}
            equivalence_surcharges = {}
            total = 0
            for line in queryset:
                subtotal += line.subtotal

                if hasattr(line, 'tax'):
                    if line.tax not in tax:
                        if not details:
                            tax[line.tax] = 0
                        else:
                            tax[line.tax] = {
                                'label': line.tax_label,
                                'amount': 0
                            }
                    price_tax = line.taxes
                    if not details:
                        tax[line.tax] += price_tax
                    else:
                        tax[line.tax]['amount'] += price_tax
                else:
                    price_tax = 0

                if hasattr(line, 'equivalence_surcharge'):
                    if line.equivalence_surcharge:
                        if line.equivalence_surcharge not in equivalence_surcharges:
                            equivalence_surcharges[line.equivalence_surcharge] = 0

                        equivalence_surcharge = line.subtotal * self.equivalence_surcharge / 100.0
                        equivalence_surcharges[line.equivalence_surcharge] = equivalence_surcharge
                    else:
                        equivalence_surcharge = 0
                else:
                    equivalence_surcharge = 0

                if hasattr(line, 'discount'):
                    if line.discount not in discount:
                        discount[line.discount] = 0
                    price_discount = line.discounts
                    discount[line.discount] += price_discount
                else:
                    price_discount = 0

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


class GenLineProductBasic(CodenerixModel):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True
    quantity = models.FloatField(_("Quantity"), blank=False, null=False)
    notes = models.CharField(_("Notes"), max_length=256, blank=True, null=True)
    # additional information
    subtotal = models.FloatField(_("Subtotal"), blank=False, null=False, default=0, editable=False)
    discounts = models.FloatField(_("Discounts"), blank=False, null=False, default=0, editable=False)
    taxes = models.FloatField(_("Taxes"), blank=False, null=False, default=0, editable=False)
    equivalence_surcharges = models.FloatField(_("Equivalence surcharge"), blank=True, null=True, default=0)
    total = models.FloatField(_("Total"), blank=False, null=False, default=0, editable=False)
    # logical deletion
    removed = models.BooleanField(_("Removed"), blank=False, default=False, editable=False)

    def save(self, *args, **kwargs):
        if self.get_customer().apply_equivalence_surcharge:
            self.equivalence_surcharge = self.get_product().tax.recargo_equivalencia
        return super(GenLineProductBasic, self).save(*args, **kwargs)

    def __save__(self, args, kwargs, **conditional):
        if 'standard_save' in kwargs:
            kwargs.pop('standard_save')
        other_line = self._meta.model.objects.filter(**conditional)
        if self.pk:
            other_line = other_line.exclude(pk=self.pk)
        other_line = other_line.first()
        if not self.pk and other_line:
            if hasattr(self, 'product') and not self.product.is_pack():
                other_line.quantity += self.quantity
                other_line.save()
                return other_line.pk
            else:
                kwargs['standard_save'] = True
                return self.save(*args, **kwargs)

        elif self.pk and other_line and not other_line.product.is_pack():
            other_line.quantity += self.quantity
            self.delete()
            other_line.save()
            return other_line.pk
        else:
            kwargs['standard_save'] = True
            return self.save(*args, **kwargs)

    def delete(self):
        if not hasattr(settings, 'CDNX_INVOICING_LOGICAL_DELETION') or settings.CDNX_INVOICING_LOGICAL_DELETION is False:
            return super(GenLineProductBasic, self).delete()
        else:
            self.removed = True
            self.save(force_save=True)

    def __limitQ__(self, info):
        return {'removed': Q(removed=False)}

    def get_customer(self):
        # returns the client associated with the document
        raise Exception(_("Method 'get_customer()' don't implemented. ({})".format(self._meta.model_name)))

    def get_product(self):
        # returns the product associated with the line
        raise Exception(_("Method 'get_product()' don't implemented. ({})".format(self._meta.model_name)))


# lineas de productos
class GenLineProduct(GenLineProductBasic):  # META: Abstract class
    class Meta(GenLineProductBasic.Meta):
        abstract = True

    price_recommended = models.FloatField(_("Recomended price base"), blank=False, null=False)
    # valores aplicados
    """
    desde el formulario se podrá modificar el precio y la descripcion del producto
    se guarda el tax usado y la relacion para poder hacer un seguimiento
    """
    code = models.CharField(_("Code"), max_length=250, blank=True, null=True, default=None)
    description = models.CharField(_("Description"), max_length=256, blank=True, null=True)
    discount = models.FloatField(_("Discount (%)"), blank=False, null=False, default=0)
    price_base = models.FloatField(_("Price base"), blank=False, null=False)
    tax = models.FloatField(_("Tax (%)"), blank=True, null=True, default=0)
    equivalence_surcharge = models.FloatField(_("Equivalence surcharge (%)"), blank=True, null=True, default=0)
    tax_label = models.CharField(_("Tax Name"), max_length=250, blank=True, null=True)

    def __str__(self):
        description = ''
        if hasattr(self, 'description'):
            description = self.description
        elif hasattr(self, 'line_invoice'):
            description = self.line_invoice.description
        elif hasattr(self, 'line_ticket'):
            description = self.line_ticket.description
        return u"{} - {}".format(smart_text(description), smart_text(self.quantity))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('code', _("Code")))
        fields.append(('description', _("Description")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('price_base', _("Price base")))
        fields.append(('discount', _("Discount (%)")))
        fields.append(('discounts', _("Total Discount")))
        fields.append(('tax', _("Tax (%)")))
        fields.append(('equivalence_surcharge', _("Equivalence surcharge (%)")))
        fields.append(('taxes', _("Total Tax")))
        fields.append(('total', _("Total")))
        return fields

    def calculate_total(self):
        # compatibility with old version
        return self.total

    def update_total(self, force_save=True):
        # calculate totals
        self.subtotal = self.price_base * self.quantity
        self.taxes = (self.subtotal * self.tax / 100.0)
        self.equivalence_surcharges = (self.subtotal * self.equivalence_surcharge / 100.0)
        self.discounts = (self.subtotal * self.discount / 100.0)
        self.total = self.subtotal - self.discounts + self.taxes + self.equivalence_surcharges
        if force_save:
            self.save()

    def save(self, *args, **kwargs):
        if self.pk is None:
            if hasattr(self, 'product'):
                if not self.description:
                    self.description = self.product
                self.price_recommended = self.product.price_base
            elif hasattr(self, 'line_order'):
                if not self.description:
                    self.description = self.line_order.product
                self.price_recommended = self.line_order.price_base

        if hasattr(self, 'tax') and hasattr(self, 'type_tax'):
            self.tax = self.type_tax.tax

        if hasattr(self, 'product'):
            self.tax_label = self.product.product.tax.name
            if self.product.code:
                self.code = self.product.code
            else:
                self.code = self.product.product.code

        """
        si al guardar una linea asociada a un documento bloqueado (lock==True), duplicar el documento en una nueva versión
        """
        self.update_total(force_save=False)
        if 'force_save' in kwargs:
            kwargs.pop('force_save')
        return super(GenLineProduct, self).save(*args, **kwargs)

    def __save__(self, args, kwargs, **conditional):
        if hasattr(self, 'product'):
            conditional["product"] = self.product
        if hasattr(self, 'line_order'):
            conditional["line_order"] = self.line_order
        if hasattr(self, 'basket'):
            conditional["basket"] = self.basket

        return super(GenLineProduct, self).__save__(args, kwargs, **conditional)

    @staticmethod
    def create_document_from_another(pk, list_lines,
                                     MODEL_SOURCE, MODEL_FINAL, MODEL_LINE_SOURCE, MODEL_LINE_FINAL,
                                     url_reverse, related_line, related_object,
                                     msg_error_relation, msg_error_not_found, unique):
        """
        pk: pk del documento origen
        list_lines: listado de pk de lineas de origen
        MODEL_SOURCE: modelo del documento origen
        MODEL_FINAL: model del documento final
        MODEL_LINE_SOURCE: modelo de la linea origen
        MODEL_LINE_FINAL: modelo de la linea final
        url_reverse: url del destino
        related_line: campo del modelo linea final en el que irá asignada la linea origen
        related_object: campo del modelo linea final en el que irá asignado el objeto final
        msg_error_relation: Mensaje de error indicando que las lineas ya están relacionadas
        msg_error_not_found: Mensaje de error indicando que no se encuentra el objeto origen
        unique: (True/False) Indica si puede haber más de una linea asociada a otras lineas
        """
        context = {}
        obj_src = MODEL_SOURCE.objects.filter(pk=pk).first()
        if list_lines and obj_src:
            # parse to int
            list_lines = [int(x) for x in list_lines]
            # list of lines objects
            if unique:
                create = not MODEL_LINE_FINAL.objects.filter(**{"{}__pk__in".format(related_line): list_lines}).exists()
            else:
                create = True

            """
            si debiendo ser filas unicas no las encuentra en el modelo final, se crea el nuevo documento
            """
            if create:
                with transaction.atomic():
                    obj_final = MODEL_FINAL()
                    obj_final.customer = obj_src.customer
                    obj_final.date = datetime.datetime.now()
                    obj_final.billing_series = obj_src.billing_series

                    if isinstance(obj_final, SalesOrder):
                        obj_final.budget = obj_src

                    obj_final.save()

                    for lb_pk in list_lines:
                        line_src = MODEL_LINE_SOURCE.objects.filter(pk=lb_pk).first()
                        if line_src:
                            line_final = MODEL_LINE_FINAL(**{"{}_id".format(related_object): obj_final.pk, related_line: line_src})
                            # line_final.order = obj_final
                            # line_final.line_budget = line_src
                            src_list_fields = [f.name for f in line_src._meta.get_fields()]
                            dst_list_fields = [f.name for f in line_final._meta.get_fields()]
                            if 'product' in src_list_fields and 'product' in dst_list_fields:
                                line_final.product = line_src.product
                            if 'description' in src_list_fields and 'description' in dst_list_fields:
                                line_final.description = line_src.description
                            if 'code' in src_list_fields and 'code' in dst_list_fields:
                                line_final.code = line_src.code
                            # if hasattr(line_src, 'line_order') and hasattr(line_final, 'line_order'):
                            if 'line_order' in src_list_fields and 'line_order' in dst_list_fields:
                                line_final.line_order = line_src.line_order
                            line_final.quantity = line_src.quantity
                            line_final.price_base = line_src.price_base
                            # if hasattr(line_src, 'price_recommended') and hasattr(line_final, 'price_recommended'):
                            if 'price_recommended' in src_list_fields and 'price_recommended' in dst_list_fields:
                                line_final.price_recommended = line_src.price_recommended
                            line_final.tax = line_src.tax
                            # line_final.type_tax = line_src.type_tax
                            line_final.discount = line_src.discount
                            if 'removed' in src_list_fields and 'removed' in dst_list_fields:
                                line_final.removed = line_src.removed
                            line_final.save()

                            if hasattr(line_src, 'line_basket_option_sales') and line_src.line_basket_option_sales.exists():
                                for opt_src in line_src.line_basket_option_sales.all():
                                    opt_dst = SalesLineOrderOption()
                                    opt_dst.line_order = line_final
                                    opt_dst.product_option = opt_src.product_option
                                    opt_dst.product_final = opt_src.product_final
                                    opt_dst.quantity = opt_src.quantity
                                    opt_dst.save()

                    # bloqueamos el documento origen
                    obj_src.lock = True
                    obj_src.save()

                    # context['url'] = reverse('ordersaless_details', kwargs={'pk': order.pk})
                    context['url'] = "{}#/{}".format(reverse(url_reverse), obj_final.pk)
                    context['obj_final'] = obj_final
            else:
                # _("Hay lineas asignadas a pedidos")
                context['error'] = msg_error_relation
        else:
            # _('Budget not found')
            context['error'] = msg_error_not_found

        return context

    @staticmethod
    def create_order_from_budget_all(order):
        lines_budget = order.budget.line_basket_sales.all()
        for lb in lines_budget:
            lo = SalesLineOrder()
            lo.order = order
            lo.line_budget = lb
            lo.product = lb.product
            lo.quantity = lb.quantity
            lo.notes = lb.notes
            lo.price_recommended = lb.price_recommended
            lo.description = lb.description
            lo.discount = lb.discount
            lo.price_base = lb.price_base
            lo.tax = lb.tax
            lo.save()

        order.budget.role = ROLE_BASKET_BUDGET
        order.budget.save()

        return lines_budget.count() == order.line_order_sales.all().count()

    @staticmethod
    def create_order_from_budget(pk, list_lines):
        MODEL_SOURCE = SalesBasket
        MODEL_FINAL = SalesOrder
        MODEL_LINE_SOURCE = SalesLineBasket
        MODEL_LINE_FINAL = SalesLineOrder
        url_reverse = 'CDNX_invoicing_ordersaless_list'
        # type_doc
        related_line = 'line_budget'
        related_object = 'order'
        msg_error_relation = _("Hay lineas asignadas a pedidos")
        msg_error_not_found = _('Budget not found')

        # duplicamos el presupuesto si el numero de lineas es diferente
        # relacionando el pedido a este nuevo presupuesto
        if list_lines and len(list_lines) != MODEL_LINE_SOURCE.objects.filter(basket=pk).count():
            budget = MODEL_SOURCE.objects.get(pk=pk)
            # el presupuesto tiene que estar firmado para poder generar el pedido
            if not budget.signed:
                context = {}
                context['error'] = _("Unsigned budget")
                return context
            else:
                new_budget = budget.duplicate(MODEL_LINE_SOURCE, list_lines)
                pk = new_budget.pk
                list_lines = [x[0] for x in MODEL_LINE_SOURCE.objects.filter(basket=pk).values_list('pk')]

        return GenLineProduct.create_document_from_another(pk, list_lines,
                                                           MODEL_SOURCE, MODEL_FINAL, MODEL_LINE_SOURCE, MODEL_LINE_FINAL,
                                                           url_reverse, related_line, related_object,
                                                           msg_error_relation, msg_error_not_found, True)

    @staticmethod
    def create_albaran_automatic(pk, list_lines):
        """
        creamos de forma automatica el albaran
        """
        line_bd = SalesLineAlbaran.objects.filter(line_order__pk__in=list_lines).values_list('line_order__pk')
        if line_bd.count() == 0 or len(list_lines) != len(line_bd[0]):
            # solo aquellas lineas de pedidos que no estan ya albarandas
            if line_bd.count() != 0:
                for x in line_bd[0]:
                    list_lines.pop(list_lines.index(x))

            GenLineProduct.create_albaran_from_order(pk, list_lines)

    @staticmethod
    def create_albaran_from_order(pk, list_lines):
        MODEL_SOURCE = SalesOrder
        MODEL_FINAL = SalesAlbaran
        MODEL_LINE_SOURCE = SalesLineOrder
        MODEL_LINE_FINAL = SalesLineAlbaran
        url_reverse = 'CDNX_invoicing_albaransaless_list'
        # type_doc
        related_line = 'line_order'
        related_object = 'albaran'
        msg_error_relation = _("Hay lineas asignadas a albaranes")
        msg_error_not_found = _('Sales order not found')

        return GenLineProduct.create_document_from_another(pk, list_lines,
                                                           MODEL_SOURCE, MODEL_FINAL, MODEL_LINE_SOURCE, MODEL_LINE_FINAL,
                                                           url_reverse, related_line, related_object,
                                                           msg_error_relation, msg_error_not_found, False)

    @staticmethod
    def create_ticket_from_order(pk, list_lines):
        MODEL_SOURCE = SalesOrder
        MODEL_FINAL = SalesTicket
        MODEL_LINE_SOURCE = SalesLineOrder
        MODEL_LINE_FINAL = SalesLineTicket
        url_reverse = 'CDNX_invoicing_ticketsaless_list'
        # type_doc
        related_line = 'line_order'
        related_object = 'ticket'
        msg_error_relation = _("Hay lineas asignadas a ticket")
        msg_error_not_found = _('Sales order not found')

        with transaction.atomic():
            GenLineProduct.create_albaran_automatic(pk, list_lines)
            return GenLineProduct.create_document_from_another(pk, list_lines,
                                                               MODEL_SOURCE, MODEL_FINAL, MODEL_LINE_SOURCE, MODEL_LINE_FINAL,
                                                               url_reverse, related_line, related_object,
                                                               msg_error_relation, msg_error_not_found, False)

    @staticmethod
    def create_invoice_from_order(pk, list_lines):
        MODEL_SOURCE = SalesOrder
        MODEL_FINAL = SalesInvoice
        MODEL_LINE_SOURCE = SalesLineOrder
        MODEL_LINE_FINAL = SalesLineInvoice
        url_reverse = 'CDNX_invoicing_invoicesaless_list'
        # type_doc
        related_line = 'line_order'
        related_object = 'invoice'
        msg_error_relation = _("Hay lineas asignadas a facturas")
        msg_error_not_found = _('Sales order not found')

        with transaction.atomic():
            GenLineProduct.create_albaran_automatic(pk, list_lines)
            return GenLineProduct.create_document_from_another(pk, list_lines,
                                                               MODEL_SOURCE, MODEL_FINAL, MODEL_LINE_SOURCE, MODEL_LINE_FINAL,
                                                               url_reverse, related_line, related_object,
                                                               msg_error_relation, msg_error_not_found, False)

    @staticmethod
    def create_ticket_from_albaran(pk, list_lines):
        """
        la pk y list_lines son de albaranes, necesitamos la info de las lineas de pedidos
        """
        context = {}
        if list_lines:
            new_list_lines = [x[0] for x in SalesLineAlbaran.objects.values_list('line_order__pk').filter(
                pk__in=[int(x) for x in list_lines]
            ).exclude(invoiced=True)]
            if new_list_lines:
                lo = SalesLineOrder.objects.values_list('order__pk').filter(pk__in=new_list_lines)[:1]
                if lo and lo[0] and lo[0][0]:
                    new_pk = lo[0][0]
                    context = GenLineProduct.create_ticket_from_order(new_pk, new_list_lines)
                    if 'error' not in context or not context['error']:
                        SalesLineAlbaran.objects.filter(
                            pk__in=[int(x) for x in list_lines]
                        ).exclude(invoiced=True).update(invoiced=True)
                    return context
                else:
                    error = _('Pedido no encontrado')
            else:
                error = _('Lineas no relacionadas con pedido')
        else:
            error = _('Lineas no seleccionadas')
        context['error'] = error
        return context

    @staticmethod
    def create_invoice_from_albaran(pk, list_lines):
        """
        la pk y list_lines son de albaranes, necesitamos la info de las lineas de pedidos
        """
        context = {}
        if list_lines:
            new_list_lines = [x[0] for x in SalesLineAlbaran.objects.values_list('line_order__pk').filter(
                pk__in=[int(x) for x in list_lines]
            ).exclude(invoiced=True)]
            if new_list_lines:
                lo = SalesLineOrder.objects.values_list('order__pk').filter(pk__in=new_list_lines)[:1]
                if lo and lo[0] and lo[0][0]:
                    new_pk = lo[0][0]
                    context = GenLineProduct.create_invoice_from_order(new_pk, new_list_lines)
                    if 'error' not in context or not context['error']:
                        SalesLineAlbaran.objects.filter(
                            pk__in=[int(x) for x in list_lines]
                        ).exclude(invoiced=True).update(invoiced=True)
                    return context
                else:
                    error = _('Pedido no encontrado')
            else:
                error = _('Lineas no relacionadas con pedido')
        else:
            error = _('Lineas no seleccionadas')
        context['error'] = error
        return context

    @staticmethod
    def create_invoice_from_ticket(pk, list_lines):
        """
        la pk y list_lines son de ticket, necesitamos la info de las lineas de pedidos
        """
        context = {}
        if list_lines:
            new_list_lines = [x[0] for x in SalesLineTicket.objects.values_list('line_order__pk').filter(pk__in=[int(x) for x in list_lines])]
            if new_list_lines:
                lo = SalesLineOrder.objects.values_list('order__pk').filter(pk__in=new_list_lines)[:1]
                if lo and lo[0] and lo[0][0]:
                    new_pk = lo[0][0]
                    return GenLineProduct.create_invoice_from_order(new_pk, new_list_lines)
                else:
                    error = _('Pedido no encontrado')
            else:
                error = _('Lineas no relacionadas con pedido')
        else:
            error = _('Lineas no seleccionadas')
        context['error'] = error
        return context


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


# reserva de productos
class SalesReservedProduct(CodenerixModel):
    customer = models.ForeignKey(Customer, related_name='reservedproduct_sales', verbose_name=_("Customer"), on_delete=models.CASCADE)
    product = models.ForeignKey(ProductFinal, related_name='reservedproduct_sales', verbose_name=_("Product"), on_delete=models.CASCADE)
    quantity = models.FloatField(_("Quantity"), blank=False, null=False)

    def __str__(self):
        return u"{}".format(smart_text(self.customer))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('customer', _("Customer")))
        fields.append(('product', _("Product")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('created', _("Created")))
        return fields


# nueva cesta de la compra
class SalesBasket(GenVersion):
    customer = models.ForeignKey(Customer, related_name='basket_sales', verbose_name=_("Customer"), on_delete=models.CASCADE)
    pos_slot = models.ForeignKey(POSSlot, related_name='basket_sales', verbose_name=_("Point of Sales"), null=True, on_delete=models.CASCADE)
    role = models.CharField(_("Role basket"), max_length=2, choices=ROLE_BASKET, blank=False, null=False, default=ROLE_BASKET_SHOPPINGCART)
    signed = models.BooleanField(_("Signed"), blank=False, default=False)
    public = models.BooleanField(_("Public"), blank=False, default=False)
    payment = models.ManyToManyField(PaymentRequest, verbose_name=_(u"Payment Request"), blank=True, related_name='basket_sales')
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False)
    address_delivery = models.ForeignKey(Address, related_name='order_sales_delivery', verbose_name=_("Address delivery"), blank=True, null=True, on_delete=models.CASCADE)
    address_invoice = models.ForeignKey(Address, related_name='order_sales_invoice', verbose_name=_("Address invoice"), blank=True, null=True, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(_("Expiration date"), blank=True, null=True, editable=False)
    haulier = models.ForeignKey(Haulier, related_name='basket_sales', verbose_name=_("Haulier"), blank=True, null=True, on_delete=models.CASCADE)
    billing_series = models.ForeignKey(BillingSeries, related_name='basket_sales', verbose_name='Billing series', blank=False, null=False, on_delete=models.CASCADE)

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
        if self.role != ROLE_BASKET_BUDGET and lines and self.line_basket_sales.count() != len(lines):
            # duplicate object
            lines = [int(x) for x in lines]
            obj = copy.copy(self)
            obj.pk = None
            obj.role = ROLE_BASKET_BUDGET
            obj.save()
            for line in self.line_basket_sales.filter(pk__in=lines):
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
        if not hasattr(self, 'order_sales'):
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

                for line in self.line_basket_sales.all():
                    lorder = SalesLineOrder()
                    lorder.order = order
                    lorder.line_budget = line
                    lorder.product = line.product
                    lorder.price_recommended = line.price_recommended
                    lorder.description = line.description
                    lorder.discount = line.discount
                    lorder.price_base = line.price_base
                    lorder.tax = line.tax
                    lorder.equivalence_surcharge = line.equivalence_surcharge
                    lorder.quantity = line.quantity
                    lorder.save()

            self.lock = True
            self.role = ROLE_BASKET_BUDGET
            self.expiration_date = None
            self.save()

    def lock_delete(self, request=None):
        # Solo se puede eliminar si:
        # * el pedido no tiene un pago realizado
        # * no se ha generado un albaran, ticket o factura relaciondos a una linea

        if hasattr(self, 'order_sales') and self.order_sales:
            if self.order_sales.payment is not None:
                return _('Cannot delete, it is related to payment')
            if self.order_sales.line_order_sales.count() != 0:
                lines_order = [x['pk'] for x in self.order_sales.line_order_sales.all().values('pk')]
                if SalesLineAlbaran.objects.filter(line_order__in=lines_order).count() != 0:
                    return _('Cannot delete, it is related to albaran')
                if SalesLineTicket.objects.filter(line_order__in=lines_order).count() != 0:
                    return _('Cannot delete, it is related to tickets')
                if SalesLineInvoice.objects.filter(line_order__in=lines_order).count() != 0:
                    return _('Cannot delete, it is related to invoices')

        return super(SalesBasket, self).lock_delete()

    def calculate_price_doc_complete(self, details=False):
        return super(SalesBasket, self).calculate_price_doc_complete(self.line_basket_sales.filter(removed=False), details)

    def list_tickets(self):
        # retorna todos los tickets en los que hay lineas de la cesta
        return SalesTicket.objects.filter(line_ticket_sales__line_order__order__budget=self).distinct()

    def print_counter(self, user):
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

    def get_customer(self):
        return self.customer


# nueva linea de la cesta de la compra
class SalesLineBasket(GenLineProduct):
    basket = models.ForeignKey(SalesBasket, related_name='line_basket_sales', verbose_name=_("Basket"), on_delete=models.CASCADE)
    product = models.ForeignKey(ProductFinal, related_name='line_basket_sales', verbose_name=_("Product"), on_delete=models.CASCADE)

    def __fields__(self, info):
        fields = super(SalesLineBasket, self).__fields__(info)
        fields.append(('line_basket_option_sales', _('Options')))
        return fields

    def lock_delete(self, request=None):
        # Solo se puede eliminar si no se ha generado un albaran, ticket o factura apartir de ella
        if hasattr(self.basket, 'order_sales') and hasattr(self, 'line_order_sales'):
            if self.line_order_sales.line_albaran_sales.count() != 0:
                return _("Cannot delete line, it is related to albaran")
            elif self.line_order_sales.line_ticket_sales.count() != 0:
                return _("Cannot delete line, it is related to tickets")
            elif self.line_order_sales.line_invoice_sales.count() != 0:
                return _("Cannot delete line, it is related to invoices")

        return super(SalesLineBasket, self).lock_delete(request)

    def save(self, *args, **kwargs):
        force = kwargs.get('force_save', False)
        if self.basket.lock and force is False:
            raise IntegrityError(_('You can not modify, locked document'))
        else:
            if kwargs.get('standard_save', False):
                kwargs.pop('standard_save')
                result = super(self._meta.model, self).save(*args, **kwargs)
                self.basket.update_totales()
                return result
            else:
                return self.__save__(args, kwargs)

    def remove_options(self):
        self.line_basket_option_sales.all().delete()

    def set_options(self, options):
        """
        options = [{
            'product_option': instance of ProductFinalOption,
            'product_final': instance of ProductFinal,
            'quantity': Float
        }, ]
        """
        with transaction.atomic():
            for option in options:
                opt = self.line_basket_option_sales.filter(
                    product_option=option['product_option']
                ).first()
                if opt:  # edit
                    change = False
                    if opt.quantity != option['quantity']:
                        opt.quantity = option['quantity']
                        change = True
                    if opt.product_final != option['product_final']:
                        opt.product_final = option['product_final']
                        change = True
                    if change:
                        opt.save()
                else:  # new
                    opt = SalesLineBasketOption()
                    # raise Exception(self.pk, self.__dict__, self)
                    # raise Exception(self.pk)
                    opt.line_budget = SalesLineBasket.objects.get(pk=self.pk)
                    opt.product_option = option['product_option']
                    opt.product_final = option['product_final']
                    opt.quantity = option['quantity']
                    opt.save()

    def get_customer(self):
        return self.basket.customer

    def get_product(self):
        return self.product


class SalesLineBasketOption(CodenerixModel):
    line_budget = models.ForeignKey(SalesLineBasket, related_name='line_basket_option_sales', verbose_name=_("Line budget"), on_delete=models.CASCADE)
    product_option = models.ForeignKey(ProductFinalOption, related_name='line_basket_option_sales', verbose_name=_("Option"), on_delete=models.CASCADE)
    product_final = models.ForeignKey(ProductFinal, related_name='line_basket_option_sales', verbose_name=_("Product"), on_delete=models.CASCADE)
    quantity = models.FloatField(_("Quantity"), blank=False, null=False)

    def __str__(self):
        return u"{} - {}".format(self.product_option, self.product_final)

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('line_budget', _('Line budget')))
        fields.append(('product_option', _('Product option')))
        fields.append(('product_final', _('Product final')))
        fields.append(('quantity', _('Quantity')))
        return fields


# pedidos
class SalesOrder(GenVersion):
    budget = models.OneToOneField(SalesBasket, related_name='order_sales', verbose_name=_("Budget"), null=True, blank=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='order_sales', verbose_name=_("Customer"), on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, related_name='order_sales', verbose_name=_("Storage"), blank=True, null=True, on_delete=models.CASCADE)
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
        fields.append(('date', _('Date')))
        fields.append(('storage', _('Storage')))
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
        return super(SalesOrder, self).calculate_price_doc_complete(self.line_order_sales.filter(removed=False), details)

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
        queryset = SalesLineInvoice.objects.filter(
            removed=False,
            invoice__removed=False,
            line_order__in=self.line_order_sales.filter(removed=False)
        )
        if only_code:
            result = list(queryset.values('invoice__code', 'invoice__pk').distinct())
        else:
            result = queryset.distinct()
        return result


# lineas de pedidos
class SalesLineOrder(GenLineProduct):
    order = models.ForeignKey(SalesOrder, related_name='line_order_sales', verbose_name=_("Sales order"), on_delete=models.CASCADE)
    line_budget = models.OneToOneField(SalesLineBasket, related_name='line_order_sales', verbose_name=_("Line budget"), null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductFinal, related_name='line_order_sales', verbose_name=_("Product"), on_delete=models.CASCADE)

    def __fields__(self, info):
        fields = super(SalesLineOrder, self).__fields__(info)
        # fields.insert(0, ('order', _("Sales order")))
        # fields.append(('line_budget', _("Line budget")))
        return fields

    def save(self, *args, **kwargs):
        force = kwargs.get('force_save', False)
        if self.order.lock and force is False:
            raise IntegrityError(_('You can not modify, locked document'))
        else:
            if kwargs.get('standard_save', False):
                kwargs.pop('standard_save')
                result = super(self._meta.model, self).save(*args, **kwargs)
                self.order.update_totales()
                return result
            else:
                return self.__save__(args, kwargs, order=self.order, line_budget=self.line_budget)

    def get_customer(self):
        return self.order.customer

    def get_product(self):
        return self.product


class SalesLineOrderOption(CodenerixModel):
    line_order = models.ForeignKey(SalesLineOrder, related_name='line_order_option_sales', verbose_name=_("Line Order"), on_delete=models.CASCADE)
    product_option = models.ForeignKey(ProductFinalOption, related_name='line_order_option_sales', verbose_name=_("Option"), on_delete=models.CASCADE)
    product_final = models.ForeignKey(ProductFinal, related_name='line_order_option_sales', verbose_name=_("Product"), on_delete=models.CASCADE)
    quantity = models.FloatField(_("Quantity"), blank=False, null=False)

    def __str__(self):
        return u"Order-{}".format(smart_text(self.code))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('line_order', _('Line order')))
        fields.append(('product_option', _('Product option')))
        fields.append(('product_final', _('Product final')))
        fields.append(('quantity', _('Quantity')))
        return fields


# documentos de pedidos
class SalesOrderDocument(CodenerixModel, GenDocumentFile):
    order = models.ForeignKey(SalesOrder, related_name='order_document_sales', verbose_name=_("Sales order"), on_delete=models.CASCADE)
    kind = models.ForeignKey(TypeDocument, related_name='order_document_sales', verbose_name=_('Document type'), blank=False, null=False, on_delete=models.CASCADE)
    notes = models.TextField(_("Notes"), max_length=256, blank=True, null=True)

    def __str__(self):
        return u'{}'.format(smart_text(self.name_file))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('kind', _('Document type')))
        fields.append(('name_file', _('Name')))
        return fields


# albaranes
class SalesAlbaran(GenVersion):
    summary_delivery = models.TextField(_("Address delivery"), max_length=256, blank=True, null=True)
    billing_series = models.ForeignKey(BillingSeries, related_name='albaran_sales', verbose_name='Billing series', blank=False, null=False, on_delete=models.CASCADE)

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
        return super(SalesAlbaran, self).calculate_price_doc_complete(self.line_albaran_sales.filter(removed=False), details)

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


# lineas de albaranes
class SalesLineAlbaran(GenLineProductBasic):
    albaran = models.ForeignKey(SalesAlbaran, related_name='line_albaran_sales', verbose_name=_("Albaran"), on_delete=models.CASCADE)
    line_order = models.ForeignKey(SalesLineOrder, related_name='line_albaran_sales', verbose_name=_("Line orders"), null=True, on_delete=models.CASCADE)
    invoiced = models.BooleanField(_("Invoiced"), blank=False, default=False)

    def __str__(self):
        return u"{} - {}".format(smart_text(self.line_order.product), smart_text(self.quantity))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('line_order__order', _("Sales order")))
        fields.append(('line_order__product', _("Product")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('invoiced', _("Invoiced")))
        return fields

    def update_total(self, force_save=True):
        self.subtotal = self.line_order.price_base * self.quantity
        self.taxes = (self.subtotal * self.line_order.tax / 100.0)
        self.equivalence_surcharges = (self.subtotal * self.line_order.equivalence_surcharge / 100.0)
        self.discounts = (self.subtotal * self.line_order.discount / 100.0)
        self.total = self.subtotal - self.discounts + self.taxes + self.equivalence_surcharges
        if force_save:
            self.save()

    def get_customer(self):
        return self.line_order.get_customer()

    def get_product(self):
        return self.line_order.product

    def save(self, *args, **kwargs):
        force = kwargs.get('force_save', False)
        if self.albaran.lock and force is False:
            raise IntegrityError(_('You can not modify, locked document'))
        else:
            if kwargs.get('standard_save', False):
                kwargs.pop('standard_save')
                self.update_total(force_save=False)
                result = super(self._meta.model, self).save(*args, **kwargs)
                self.albaran.update_totales()
                return result
            else:
                return self.__save__(args, kwargs, albaran=self.albaran, line_order=self.line_order)

    def calculate_total(self):
        return self.total


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
        fields.append(('line_ticket_sales__line_order__product', _('Products')))
        fields.append(('date', _('Date')))
        fields.append(('total', _('Total')))
        return fields

    def calculate_price_doc(self):
        return self.total

    def calculate_price_doc_complete(self, details=False):
        return super(SalesTicket, self).calculate_price_doc_complete(self.line_ticket_sales.filter(removed=False), details)

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


class SalesLineTicket(GenLineProduct):
    ticket = models.ForeignKey(SalesTicket, related_name='line_ticket_sales', verbose_name=_("Ticket"), on_delete=models.CASCADE)
    line_order = models.ForeignKey(SalesLineOrder, related_name='line_ticket_sales', verbose_name=_("Line order"), null=True, on_delete=models.CASCADE)

    def __fields__(self, info):
        fields = super(SalesLineTicket, self).__fields__(info)
        # fields.insert(0, ('ticket', _("Ticket")))
        # fields.append(('line_order', _("Line order")))
        return fields

    def get_customer(self):
        return self.line_order.get_customer()

    def get_product(self):
        return self.line_order.product

    def save(self, *args, **kwargs):
        force = kwargs.get('force_save', False)
        if self.ticket.lock and force is False:
            raise IntegrityError(_('You can not modify, locked document'))
        else:
            if kwargs.get('standard_save', False):
                kwargs.pop('standard_save')
                result = super(self._meta.model, self).save(*args, **kwargs)
                self.ticket.update_totales()
                return result
            else:
                return self.__save__(args, kwargs, ticket=self.ticket, line_order=self.line_order)


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
        return super(SalesTicketRectification, self).calculate_price_doc_complete(self.line_ticketrectification_sales.filter(removed=False), details)

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


class SalesLineTicketRectification(GenLineProductBasic):
    ticket_rectification = models.ForeignKey(SalesTicketRectification, related_name='line_ticketrectification_sales', verbose_name=_("Ticket rectification"), on_delete=models.CASCADE)
    line_ticket = models.ForeignKey(SalesLineTicket, related_name='line_ticketrectification_sales', verbose_name=_("Line ticket"), on_delete=models.CASCADE)

    def __fields__(self, info):
        fields = []
        fields.append(('ticket_rectification', _("Ticket rectification")))
        fields.append(('line_ticket', _("Line ticket")))
        fields.append(('quantity', _("Quantity")))
        return fields

    def update_total(self, force_save=True):
        self.subtotal = self.line_ticket.price_base * self.quantity
        self.taxes = (self.subtotal * self.line_ticket.tax / 100.0)
        self.equivalence_surcharges = (self.subtotal * self.line_ticket.equivalence_surcharge / 100.0)
        self.discounts = (self.subtotal * self.line_ticket.discount / 100.0)
        self.total = self.subtotal - self.discounts + self.taxes + self.equivalence_surcharges
        if force_save:
            self.save()

    def get_customer(self):
        return self.line_ticket.get_customer()

    def get_product(self):
        return self.line_ticket.product

    def save(self, *args, **kwargs):
        force = kwargs.get('force_save', False)
        if self.ticket_rectification.lock and force is False:
            raise IntegrityError(_('You can not modify, locked document'))
        else:
            if kwargs.get('standard_save', False):
                kwargs.pop('standard_save')
                self.update_total(force_save=False)
                result = super(self._meta.model, self).save(*args, **kwargs)
                self.ticket_rectification.update_totales()
                return result
            else:
                return self.__save__(args, kwargs, ticket_rectification=self.ticket_rectification, line_ticket=self.line_ticket)

    def calculate_total(self):
        return self.total


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
        return super(SalesInvoice, self).calculate_price_doc_complete(self.line_invoice_sales.filter(removed=False), details)

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


class SalesLineInvoice(GenLineProduct):
    invoice = models.ForeignKey(SalesInvoice, related_name='line_invoice_sales', verbose_name=_("Invoice"), on_delete=models.CASCADE)
    line_order = models.ForeignKey(SalesLineOrder, related_name='line_invoice_sales', verbose_name=_("Line order"), null=True, on_delete=models.CASCADE)

    def __fields__(self, info):
        fields = super(SalesLineInvoice, self).__fields__(info)
        # fields.insert(0, ('invoice', _("Invoice")))
        # fields.append(('line_order', _("Line order")))
        return fields

    def save(self, *args, **kwargs):
        force = kwargs.get('force_save', False)
        if self.invoice.lock and force is False:
            raise IntegrityError(_('You can not modify, locked document'))
        else:
            if kwargs.get('standard_save', False):
                kwargs.pop('standard_save')
                result = super(self._meta.model, self).save(*args, **kwargs)
                self.invoice.update_totales()
                return result
            else:
                return self.__save__(args, kwargs, invoice=self.invoice, line_order=self.line_order)

    def get_customer(self):
        return self.invoice.customer


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
        return super(SalesInvoiceRectification, self).calculate_price_doc_complete(self.line_invoicerectification_sales.filter(removed=False), details)

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


class SalesLineInvoiceRectification(GenLineProductBasic):
    invoice_rectification = models.ForeignKey(SalesInvoiceRectification, related_name='line_invoicerectification_sales', verbose_name=_("Invoice rectification"), on_delete=models.CASCADE)
    line_invoice = models.ForeignKey(SalesLineInvoice, related_name='line_invoicerectification_sales', verbose_name=_("Line invoice"), on_delete=models.CASCADE)

    def __fields__(self, info):
        fields = []
        fields.append(('invoice_rectification', _("Invoices rectification")))
        fields.append(('line_invoice', _("Line invoice")))
        fields.append(('quantity', _("Quantity")))
        return fields

    def update_total(self, force_save=True):
        self.subtotal = self.line_invoice.price_base * self.quantity
        self.taxes = (self.subtotal * self.line_invoice.tax / 100.0)
        self.equivalence_surcharges = (self.subtotal * self.line_invoice.equivalence_surcharge / 100.0)
        self.discounts = (self.subtotal * self.line_invoice.discount / 100.0)
        self.total = self.subtotal - self.discounts + self.taxes + self.equivalence_surcharges
        if force_save:
            self.save()

    def save(self, *args, **kwargs):
        force = kwargs.get('force_save', False)
        if self.invoice_rectification.lock and force is False:
            raise IntegrityError(_('You can not modify, locked document'))
        else:
            if kwargs.get('standard_save', False):
                kwargs.pop('standard_save')
                result = super(self._meta.model, self).save(*args, **kwargs)
                self.update_total(force_save=False)
                self.invoice_rectification.update_totales()
                return result
            else:
                return self.__save__(args, kwargs, invoice_rectification=self.invoice_rectification, line_invoice=self.line_invoice)

    def calculate_total(self):
        return self.total

    def get_customer(self):
        return self.invoice_rectification.invoice.customer


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
    line = models.ForeignKey(SalesLineBasket, related_name='reason_line_basket', verbose_name=_("Line"), on_delete=models.CASCADE)


class ReasonModificationLineOrder(ReasonModificationLine):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reason_line_order', verbose_name=_("User"), on_delete=models.CASCADE)
    reason = models.ForeignKey(ReasonModification, related_name='reason_line_order', verbose_name=_("Reason"), on_delete=models.CASCADE)
    line = models.ForeignKey(SalesLineOrder, related_name='reason_line_order', verbose_name=_("Line"), on_delete=models.CASCADE)


class ReasonModificationLineAlbaran(ReasonModificationLine):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reason_line_albaran', verbose_name=_("User"), on_delete=models.CASCADE)
    reason = models.ForeignKey(ReasonModification, related_name='reason_line_albaran', verbose_name=_("Reason"), on_delete=models.CASCADE)
    line = models.ForeignKey(SalesLineAlbaran, related_name='reason_line_albaran', verbose_name=_("Line"), on_delete=models.CASCADE)


class ReasonModificationLineTicket(ReasonModificationLine):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reason_line_ticket', verbose_name=_("User"), on_delete=models.CASCADE)
    reason = models.ForeignKey(ReasonModification, related_name='reason_line_ticket', verbose_name=_("Reason"), on_delete=models.CASCADE)
    line = models.ForeignKey(SalesLineTicket, related_name='reason_line_ticket', verbose_name=_("Line"), on_delete=models.CASCADE)


class ReasonModificationLineTicketRectification(ReasonModificationLine):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reason_line_ticket_rectification', verbose_name=_("User"), on_delete=models.CASCADE)
    reason = models.ForeignKey(ReasonModification, related_name='reason_line_ticket_rectification', verbose_name=_("Reason"), on_delete=models.CASCADE)
    line = models.ForeignKey(SalesLineTicketRectification, related_name='reason_line_ticket_rectification', verbose_name=_("Line"), on_delete=models.CASCADE)


class ReasonModificationLineInvoice(ReasonModificationLine):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reason_line_invoice', verbose_name=_("User"), on_delete=models.CASCADE)
    reason = models.ForeignKey(ReasonModification, related_name='reason_line_invoice', verbose_name=_("Reason"), on_delete=models.CASCADE)
    line = models.ForeignKey(SalesLineInvoice, related_name='reason_line_invoice', verbose_name=_("Line"), on_delete=models.CASCADE)


class ReasonModificationLineInvoiceRectification(ReasonModificationLine):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reason_line_invoice_rectification', verbose_name=_("User"), on_delete=models.CASCADE)
    reason = models.ForeignKey(ReasonModification, related_name='reason_line_invoice_rectification', verbose_name=_("Reason"), on_delete=models.CASCADE)
    line = models.ForeignKey(SalesLineInvoiceRectification, related_name='reason_line_invoice_rectification', verbose_name=_("Line"), on_delete=models.CASCADE)


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
