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
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.utils import timezone
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _

from codenerix.models import GenInterface, CodenerixModel
from codenerix.models_people import GenRole
from codenerix_extensions.helpers import get_external_method
from codenerix_extensions.files.models import GenDocumentFile

from codenerix_invoicing.models import POS, Haulier
from codenerix_invoicing.models_purchases import PAYMENT_DETAILS
from codenerix_invoicing.settings import CDNX_INVOICING_PERMISSIONS

from codenerix_products.models import ProductFinal, TypeTax
from codenerix_storages.models import Storage
from codenerix_payments.models import PaymentRequest, PaymentConfirmation

    
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

STATUS_ORDER = (
    ('PE', _("Pending")),
    ('PA', _("Payment accepted")),
    ('SE', _("Sent")),
    ('DE', _("Delivered")),
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
        }


    currency = models.CharField(_("Currency"), max_length=250, blank=True, null=True)
    # serie de facturacion
    billing_series = models.ForeignKey("BillingSeries", related_name='billing_series', verbose_name='Billing series')
    # datos de facturación
    # saldo final
    final_balance = models.CharField(_("Balance"), max_length=250, blank=True, null=True)
    # credito o riesgo maximo autorizado
    credit = models.CharField(_("Credit"), max_length=250, blank=True, null=True)
    # Aplicar recargo de equivalencia
    apply_equivalence_surcharge = models.BooleanField(_("Apply equivalence surcharge"), blank=False, default=False)
    # Tipo de iva
    type_tax = models.ForeignKey(TypeTax, related_name='customers', verbose_name=_("Type tax"), null=True)

    @staticmethod
    def foreignkey_external():
        return get_external_method(Customer, Customer.CodenerixMeta.force_methods['foreignkey_customer'][0])

    def __unicode__(self):
        return u"{}".format(smart_text(self.pk))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('final_balance', _("Balance")))
        fields.append(('credit', _("Credit")))
        fields.append(('currency', _("Currency")))
        fields.append(('billing_series', _("Billing series")))
        fields.append(('apply_equivalence_surcharge', _("Currency")))
        fields.append(('type_tax', _("Type tax")))
        fields = get_external_method(Customer, '__fields_customer__', info, fields)
        return fields

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
        group = 'Customer'
        perms = []
        print(cls.customer.field.related_model)

        return None

        # print({group: {'gperm': None, 'dperm': perms, 'model': None},})


class Address(CodenerixModel):
    def __unicode__(self):
        if hasattr(self, 'external_delivery'):
            return u"{}".format(smart_text(self.external_delivery.get_summary()))
        elif hasattr(self, 'external_invoice'):
            return u"{}".format(smart_text(self.external_invoice.get_summary()))
        else:
            return 'No data!'
            # raise Exception(_('Address unkown'), self.__dict__)

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        if hasattr(self, 'external_delivery'):
            fields.append(('external_delivery', _("Address delivery")))
        elif hasattr(self, 'external_invoice'):
            fields.append(('external_invoice', _("Address invoice")))
        else:
            raise Exception(_('Address unkown'))
        return fields


class ABSTRACT_GenAddress():  # META: Abstract class
    class Meta(object):
        abstract = True


class GenAddress(GenInterface, ABSTRACT_GenAddress):  # META: Abstract class
    class Meta(GenInterface.Meta, ABSTRACT_GenAddress.Meta):
        abstract = True

    class CodenerixMeta:
        force_methods = {
            'foreignkey_address': ('CDNX_get_fk_info_address', _('---')),
            'get_summary': ('get_summary', ),
        }

    def save(self, *args, **kwards):
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
        return super(GenAddress, self).save(*args, **kwards)


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
    customer = models.ForeignKey(Customer, related_name='customer_documents', verbose_name=_("Customer"))
    type_document = models.ForeignKey('TypeDocument', related_name='customer_documents', verbose_name=_("Type document"), null=True)

    def __unicode__(self):
        return u"{}".format(smart_text(self.customer))

    def __str__(self):
        return self.__unicode__()

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
    date = models.DateTimeField(_("Date"), blank=False, null=False, default=timezone.now)
    observations = models.TextField(_("Observations"), max_length=256, blank=True, null=True)
    """
    si al guardar una linea asociada a un documento bloqueado (lock==True), duplicar el documento en una nueva versión
    """

    @staticmethod
    def getcode(model, real=False):
        if real is False:
            code = 0
        else:
            last = model.objects.order_by('-pk').first()
            if last:
                code = int(last.code) + 1
            else:
                code = 1
        return code

    def save(self, *args, **kwards):
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

                # reset object
                self.pk = None
                self.lock = False
                self.code = GenVersion.getcode(self._meta.model, True)
        else:
            self.code = GenVersion.getcode(self._meta.model, True)

        return super(GenVersion, self).save(*args, **kwards)


class GenLineProductBasic(CodenerixModel):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True
    quantity = models.FloatField(_("Quantity"), blank=False, null=False)
    notes = models.CharField(_("Notes"), max_length=256, blank=True, null=True)

    def __save__(self, args, kwargs, **conditional):
        other_line = self._meta.model.objects.filter(**conditional)
        if self.pk:
            other_line = other_line.exclude(pk=self.pk)
        other_line = other_line.first()
        if not self.pk and other_line:
            other_line.quantity += self.quantity
            other_line.save()
            return None
        elif self.pk and other_line:
            other_line.quantity += self.quantity
            self.delete()
            other_line.save()
            return None
        else:
            kwargs['standard_save'] = True
            return self.save(*args, **kwargs)


# lineas de productos
class GenLineProduct(GenLineProductBasic):  # META: Abstract class
    class Meta(GenLineProductBasic.Meta):
        abstract = True

    price_recommended = models.FloatField(_("Recomended price"), blank=False, null=False)
    # valores aplicados
    """
    desde el formulario se podrá modificar el precio y la descripcion del producto
    se guarda el tax usado y la relacion para poder hacer un seguimiento
    """
    description = models.CharField(_("Description"), max_length=256, blank=True, null=True)
    discount = models.FloatField(_("Discount"), blank=False, null=False, default=0)
    price = models.FloatField(_("Price"), blank=False, null=False)
    tax = models.FloatField(_("Tax"), blank=True, null=True, default=0)

    def __unicode__(self):
        description = ''
        if hasattr(self, 'description'):
            description = self.description
        elif hasattr(self, 'line_invoice'):
            description = self.line_invoice.description
        elif hasattr(self, 'line_ticket'):
            description = self.line_ticket.description
        return u"{} - {}".format(smart_text(description), smart_text(self.quantity))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('description', _("Description")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('price', _("Price")))
        fields.append(('discount', _("Discount")))
        fields.append(('tax', _("Tax")))
        return fields

    def calculate_total(self):
        price_base = self.price * self.quantity
        return price_base - (price_base * self.discount / 100.0) + (price_base * self.tax / 100.0)

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
                            # if hasattr(line_src, 'line_order') and hasattr(line_final, 'line_order'):
                            if 'line_order' in src_list_fields and 'line_order' in dst_list_fields:
                                line_final.line_order = line_src.line_order
                            line_final.quantity = line_src.quantity
                            line_final.price = line_src.price
                            # if hasattr(line_src, 'price_recommended') and hasattr(line_final, 'price_recommended'):
                            if 'price_recommended' in src_list_fields and 'price_recommended' in dst_list_fields:
                                line_final.price_recommended = line_src.price_recommended
                            line_final.tax = line_src.tax
                            # line_final.type_tax = line_src.type_tax
                            line_final.discount = line_src.discount
                            line_final.save()

                    # bloqueamos el documento origen
                    obj_src.lock = True
                    obj_src.save()

                    # context['url'] = reverse('ordersaless_details', kwargs={'pk': order.pk})
                    context['url'] = "{}#/{}".format(reverse(url_reverse), obj_final.pk)
            else:
                # _("Hay lineas asignadas a pedidos")
                context['error'] = msg_error_relation
        else:
            # _('Budget not found')
            context['error'] = msg_error_not_found

        return context

    def save(self, *args, **kwards):
        if self.pk is None:
            if hasattr(self, 'product'):
                if not self.description:
                    self.description = self.product
                self.price_recommended = self.product.price
            elif hasattr(self, 'line_order'):
                if not self.description:
                    self.description = self.line_order.product
                self.price_recommended = self.line_order.price

        if hasattr(self, 'tax') and hasattr(self, 'type_tax'):
            self.tax = self.type_tax.tax
        """
        si al guardar una linea asociada a un documento bloqueado (lock==True), duplicar el documento en una nueva versión
        """
        return super(GenLineProduct, self).save(*args, **kwards)

    def __save__(self, args, kwargs, **conditional):
        if hasattr(self, 'product'):
            conditional["product"] = self.product
        if hasattr(self, 'line_order'):
            conditional["line_order"] = self.line_order
        if hasattr(self, 'basket'):
            conditional["basket"] = self.basket

        return super(GenLineProduct, self).__save__(args, kwargs, **conditional)

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
            lo.price = lb.price
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
        msg_error_not_found = _('Order not found')

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
        msg_error_not_found = _('Order not found')

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
        msg_error_not_found = _('Order not found')

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

    def __unicode__(self):
        return u"Rct-{}".format(smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        return fields


# reserva de productos
class SalesReservedProduct(CodenerixModel):
    customer = models.ForeignKey(Customer, related_name='reservedproduct_sales', verbose_name=_("Customer"))
    product = models.ForeignKey(ProductFinal, related_name='reservedproduct_sales', verbose_name=_("Product"))
    quantity = models.FloatField(_("Quantity"), blank=False, null=False)

    def __unicode__(self):
        return u"{}".format(smart_text(self.customer))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('customer', _("Customer")))
        fields.append(('product', _("Product")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('created', _("Created")))
        return fields


# nueva cesta de la compra
class SalesBasket(GenVersion):
    customer = models.ForeignKey(Customer, related_name='basket_sales', verbose_name=_("Customer"))
    point_sales = models.ForeignKey(POS, related_name='basket_sales', verbose_name=_("Point of Sales"), null=True)
    role = models.CharField(_("Role basket"), max_length=2, choices=ROLE_BASKET, blank=False, null=False, default=ROLE_BASKET_SHOPPINGCART)
    signed = models.BooleanField(_("Signed"), blank=False, default=False)
    public = models.BooleanField(_("Public"), blank=False, default=False)
    payment = models.ManyToManyField(PaymentRequest, verbose_name=_(u"Payment Request"), blank=True, related_name='basket_sales')
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False)
    address_delivery = models.ForeignKey(Address, related_name='order_sales_delivery', verbose_name=_("Address delivery"), blank=True, null=True)
    address_invoice = models.ForeignKey(Address, related_name='order_sales_invoice', verbose_name=_("Address invoice"), blank=True, null=True)
    expiration_date = models.DateTimeField(_("Expiration date"), blank=True, null=True, editable=False)
    haulier = models.ForeignKey(Haulier, related_name='basket_sales', verbose_name=_("Haulier"), blank=True, null=True)
    
    def __unicode__(self):
        return u"Order-{}".format(smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

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
                order.save()

                for line in self.line_basket_sales.all():
                    lorder = SalesLineOrder()
                    lorder.order = order
                    lorder.line_budget = line
                    lorder.product = line.product
                    lorder.price_recommended = line.price_recommended
                    lorder.description = line.description
                    lorder.discount = line.discount
                    lorder.price = line.price
                    lorder.tax = line.tax
                    lorder.quantity = line.quantity
                    lorder.save()
                
            self.lock = True
            self.role = ROLE_BASKET_BUDGET
            self.expiration_date = None
            self.save()


# nueva linea de la cesta de la compra
class SalesLineBasket(GenLineProduct):
    basket = models.ForeignKey(SalesBasket, related_name='line_basket_sales', verbose_name=_("Basket"))
    product = models.ForeignKey(ProductFinal, related_name='line_basket_sales', verbose_name=_("Product"))

    def __fields__(self, info):
        fields = super(SalesLineBasket, self).__fields__(info)
        fields.insert(0, ('basket', _("Basket")))
        return fields

    def save(self, *args, **kwargs):
        if 'standard_save' in kwargs:
            kwargs.pop('standard_save')
            return super(self._meta.model, self).save(*args, **kwargs)
        else:
            return self.__save__(args, kwargs)


# pedidos
class SalesOrder(GenVersion):
    budget = models.OneToOneField(SalesBasket, related_name='order_sales', verbose_name=_("Budget"), null=True, blank=True)
    customer = models.ForeignKey(Customer, related_name='order_sales', verbose_name=_("Customer"))
    storage = models.ForeignKey(Storage, related_name='order_sales', verbose_name=_("Storage"), blank=True, null=True)
    payment = models.ForeignKey(PaymentRequest, related_name='order_sales', verbose_name=_(u"Payment Request"), blank=True, null=True)
    number_tracking = models.CharField(_("Number of tracking"), max_length=128, blank=True, null=True)
    status_order = models.CharField(_("Status"), max_length=2, choices=STATUS_ORDER, blank=False, null=False, default='PE')
    payment_detail = models.CharField(_("Payment detail"), max_length=3, choices=PAYMENT_DETAILS, blank=True, null=True)
    source = models.CharField(_("Source of purchase"), max_length=250, blank=True, null=True)

    def __unicode__(self):
        return u"Order-{}".format(smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('customer', _('Customer')))
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        fields.append(('storage', _('Storage')))
        fields.append(('status_order', _('Status')))
        fields.append(('payment_detail', _('Payment detail')))
        fields.append(('source', _('Source of purchase')))
        fields.append(('number_tracking', _('Number of tracking')))
        fields.append(('budget__address_delivery', _('Address delivery')))
        fields.append(('budget__address_invoice', _('Address invoice')))
        return fields

    def calculate_price_doc(self):
        total = 0
        for line in self.line_order_sales.all():
            total += line.calculate_total()
        return total


# lineas de pedidos
class SalesLineOrder(GenLineProduct):
    order = models.ForeignKey(SalesOrder, related_name='line_order_sales', verbose_name=_("Order"))
    line_budget = models.ForeignKey(SalesLineBasket, related_name='line_order_sales', verbose_name=_("Line budget"), null=True)
    product = models.ForeignKey(ProductFinal, related_name='line_order_sales', verbose_name=_("Product"))

    def __fields__(self, info):
        fields = super(SalesLineOrder, self).__fields__(info)
        fields.insert(0, ('order', _("Order")))
        fields.append(('line_budget', _("Line budget")))
        return fields

    def save(self, *args, **kwargs):
        if 'standard_save' in kwargs:
            kwargs.pop('standard_save')
            return super(self._meta.model, self).save(*args, **kwargs)
        else:
            return self.__save__(args, kwargs, order=self.order, line_budget=self.line_budget)


# albaranes
class SalesAlbaran(GenVersion):
    tax = models.FloatField(_("Tax"), blank=False, null=False, default=0)
    summary_delivery = models.TextField(_("Address delivery"), max_length=256, blank=True, null=True)

    def __unicode__(self):
        return u"Albaran-{}".format(smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        fields.append(('tax', _('Tax')))
        fields.append(('summary_delivery', _('Address delivery')))
        return fields

    def calculate_price_doc(self):
        total = 0
        for line in self.line_albaran_sales.all():
            total += line.calculate_total()
        return total


# lineas de albaranes
class SalesLineAlbaran(GenLineProductBasic):
    albaran = models.ForeignKey(SalesAlbaran, related_name='line_albaran_sales', verbose_name=_("Albaran"))
    line_order = models.ForeignKey(SalesLineOrder, related_name='line_albaran_sales', verbose_name=_("Line orders"), null=True)
    invoiced = models.BooleanField(_("Invoiced"), blank=False, default=False)

    def __unicode__(self):
        return u"{} - {}".format(smart_text(self.line_order.product), smart_text(self.quantity))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('line_order__order', _("Order")))
        fields.append(('line_order__product', _("Product")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('invoiced', _("Invoiced")))
        return fields

    def save(self, *args, **kwargs):
        if 'standard_save' in kwargs:
            kwargs.pop('standard_save')
            return super(self._meta.model, self).save(*args, **kwargs)
        else:
            return self.__save__(args, kwargs, albaran=self.albaran, line_order=self.line_order)

    def calculate_total(self):
        price_base = self.line_order.price * self.quantity
        return price_base - (price_base * self.line_order.discount / 100.0) + (price_base * self.line_order.tax / 100.0)


# ticket y facturas son lo mismo con un check de "tengo datos del customere"
class SalesTicket(GenVersion):
    customer = models.ForeignKey(Customer, related_name='ticket_sales', verbose_name=_("Customer"))
    tax = models.FloatField(_("Tax"), blank=False, null=False, default=0)

    def __unicode__(self):
        return u"Ticket-{}".format(smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('customer', _('Customer')))
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        fields.append(('tax', _('Tax')))
        return fields

    def calculate_price_doc(self):
        total = 0
        for line in self.line_ticket_sales.all():
            total += line.calculate_total()
        return total


class SalesLineTicket(GenLineProduct):
    ticket = models.ForeignKey(SalesTicket, related_name='line_ticket_sales', verbose_name=_("Ticket"))
    line_order = models.ForeignKey(SalesLineOrder, related_name='line_ticket_sales', verbose_name=_("Line order"), null=True)

    def __fields__(self, info):
        fields = super(SalesLineTicket, self).__fields__(info)
        fields.insert(0, ('ticket', _("Ticket")))
        fields.append(('line_order', _("Line order")))
        return fields

    def save(self, *args, **kwargs):
        if 'standard_save' in kwargs:
            kwargs.pop('standard_save')
            return super(self._meta.model, self).save(*args, **kwargs)
        else:
            return self.__save__(args, kwargs, ticket=self.ticket, line_order=self.line_order)


# puede haber facturas o tickets rectificativos
# factura rectificativa
class SalesTicketRectification(GenInvoiceRectification):
    ticket = models.ForeignKey(SalesTicket, related_name='ticketrectification_sales', verbose_name=_("Ticket"), null=True)

    def calculate_price_doc(self):
        total = 0
        for line in self.line_ticketrectification_sales.all():
            total += line.calculate_total()
        return total

    def __fields__(self, info):
        fields = super(SalesTicketRectification, self).__fields__(info)
        fields.insert(0, ('ticket', _("Ticket")))
        fields.insert(0, ('ticket__customer', _("Customer")))
        return fields


class SalesLineTicketRectification(GenLineProductBasic):
    ticket_rectification = models.ForeignKey(SalesTicketRectification, related_name='line_ticketrectification_sales', verbose_name=_("Ticket rectification"))
    line_ticket = models.ForeignKey(SalesLineTicket, related_name='line_ticketrectification_sales', verbose_name=_("Line ticket"))

    def __fields__(self, info):
        fields = []
        fields.append(('ticket_rectification', _("Ticket rectification")))
        fields.append(('line_ticket', _("Line ticket")))
        fields.append(('quantity', _("Quantity")))
        return fields

    def save(self, *args, **kwargs):
        if 'standard_save' in kwargs:
            kwargs.pop('standard_save')
            return super(self._meta.model, self).save(*args, **kwargs)
        else:
            return self.__save__(args, kwargs, ticket_rectification=self.ticket_rectification, line_ticket=self.line_ticket)

    def calculate_total(self):
        price_base = self.line_ticket.price * self.quantity
        return price_base - (price_base * self.line_ticket.discount / 100.0) + (price_base * self.line_ticket.tax / 100.0)


# facturas
# una factura puede contener varios ticket o albaranes
class SalesInvoice(GenVersion):
    customer = models.ForeignKey(Customer, related_name='invoice_sales', verbose_name=_("Customer"))
    tax = models.FloatField(_("Tax"), blank=False, null=False, default=0)
    summary_invoice = models.TextField(_("Address invoice"), max_length=256, blank=True, null=True)

    def __unicode__(self):
        return u"Invoice-{}".format(smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('customer', _('Customer')))
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        fields.append(('tax', _('Tax')))
        fields.append(('summary_invoice', _('Address invoice')))
        return fields

    def calculate_price_doc(self):
        total = 0
        for line in self.line_invoice_sales.all():
            total += line.calculate_total()
        return total


class SalesLineInvoice(GenLineProduct):
    invoice = models.ForeignKey(SalesInvoice, related_name='line_invoice_sales', verbose_name=_("Invoice"))
    line_order = models.ForeignKey(SalesLineOrder, related_name='line_invoice_sales', verbose_name=_("Line order"), null=True)

    def __fields__(self, info):
        fields = super(SalesLineInvoice, self).__fields__(info)
        fields.insert(0, ('invoice', _("Ticket invoices")))
        fields.append(('line_order', _("Line order")))
        return fields

    def save(self, *args, **kwargs):
        if 'standard_save' in kwargs:
            kwargs.pop('standard_save')
            return super(self._meta.model, self).save(*args, **kwargs)
        else:
            return self.__save__(args, kwargs, invoice=self.invoice, line_order=self.line_order)


# factura rectificativa
class SalesInvoiceRectification(GenInvoiceRectification):
    invoice = models.ForeignKey(SalesInvoice, related_name='invoicerectification_sales', verbose_name=_("Invoice"), null=True)

    def calculate_price_doc(self):
        total = 0
        for line in self.line_invoicerectification_sales.all():
            total += line.calculate_total()
        return total

    def __fields__(self, info):
        fields = super(SalesInvoiceRectification, self).__fields__(info)
        fields.insert(0, ('invoice', _("Invoices")))
        fields.insert(0, ('invoice__customer', _("Customer")))
        return fields


class SalesLineInvoiceRectification(GenLineProductBasic):
    invoice_rectification = models.ForeignKey(SalesInvoiceRectification, related_name='line_invoicerectification_sales', verbose_name=_("Invoice rectification"))
    line_invoice = models.ForeignKey(SalesLineInvoice, related_name='line_invoicerectification_sales', verbose_name=_("Line invoice"))

    def __fields__(self, info):
        fields = []
        fields.append(('invoice_rectification', _("Invoices rectification")))
        fields.append(('line_invoice', _("Line invoice")))
        fields.append(('quantity', _("Quantity")))
        return fields

    def save(self, *args, **kwargs):
        if 'standard_save' in kwargs:
            kwargs.pop('standard_save')
            return super(self._meta.model, self).save(*args, **kwargs)
        else:
            return self.__save__(args, kwargs, invoice_rectification=self.invoice_rectification, line_invoice=self.line_invoice)

    def calculate_total(self):
        price_base = self.line_invoice.price * self.quantity
        return price_base - (price_base * self.line_invoice.discount / 100.0) + (price_base * self.line_invoice.tax / 100.0)
