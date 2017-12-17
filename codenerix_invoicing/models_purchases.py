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

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text

from codenerix.models import GenInterface, CodenerixModel
from codenerix.models_people import GenRole

from codenerix_extensions.helpers import get_external_method
from codenerix_extensions.files.models import GenDocumentFile
from codenerix_products.models import ProductFinal, TypeTax, Category

from codenerix_invoicing.settings import CDNX_INVOICING_PERMISSIONS

KIND_CARD_VISA = 'VIS'
KIND_CARD_MASTER = 'MAS'
KIND_CARD_AMERICAN = 'AME'
KIND_CARD_OTHER = 'OTH'

KIND_CARD = (
    (KIND_CARD_VISA, _('Visa')),
    (KIND_CARD_MASTER, _('MasterCard')),
    (KIND_CARD_AMERICAN, _('American Express')),
    (KIND_CARD_OTHER, _('Other')),
)

PAYMENT_DETAILS_AMAZON = 'AMA'
PAYMENT_DETAILS_TRANSFER = 'TRA'
PAYMENT_DETAILS_CARD = 'CAR'
PAYMENT_DETAILS_CASH = 'CAS'
PAYMENT_DETAILS_CREDIT = 'CRE'
PAYMENT_DETAILS_PAYPAL = 'PYP'
PAYMENT_DETAILS_30CREDIT = '30C'
PAYMENT_DETAILS_60CREDIT = '60C'
PAYMENT_DETAILS_90CREDIT = '90C'

PAYMENT_DETAILS = (
    (PAYMENT_DETAILS_AMAZON, _('Amazon')),
    (PAYMENT_DETAILS_TRANSFER, _('Wire transfer')),
    (PAYMENT_DETAILS_CARD, _('Card')),
    (PAYMENT_DETAILS_CASH, _('Cash')),
    (PAYMENT_DETAILS_CREDIT, _('Credit')),
    (PAYMENT_DETAILS_PAYPAL, _('Paypal')),
    (PAYMENT_DETAILS_30CREDIT, _('30 day credit')),
    (PAYMENT_DETAILS_60CREDIT, _('60 day credit')),
    (PAYMENT_DETAILS_90CREDIT, _('90 day credit')),
)

FINANCE_SURCHARGE_STATUS_CHOICE = (
    ('I', _('Taxable base')),
    ('F', _('Total bill')),
)

PURCHASE_ALBARAN_LINE_STATUS_PENDING = 'PR'
PURCHASE_ALBARAN_LINE_STATUS_REVIEWED = 'RV'
PURCHASE_ALBARAN_LINE_STATUS_REJECTED = 'RC'

PURCHASE_ALBARAN_LINE_STATUS = (
    (PURCHASE_ALBARAN_LINE_STATUS_PENDING, _('Pending review')),
    (PURCHASE_ALBARAN_LINE_STATUS_REVIEWED, _('Reviewed')),
    (PURCHASE_ALBARAN_LINE_STATUS_REJECTED, _('Rejected')),
)


# #### CLASES ABSTRACTAS #############################
# lineas de productos
class GenLineProduct(CodenerixModel):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True

    quantity = models.FloatField(_("Quantity"), blank=False, null=False)
    price = models.FloatField(_("Price"), blank=False, null=False)
    tax = models.FloatField(_("Tax"), blank=True, null=True, default=0)
    description = models.TextField(_("description"), blank=True, null=True)

    def __str__(self):
        return u"{} - {}".format(smart_text(self.product), smart_text(self.quantity))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('product', _("Product")))
        fields.append(('quantity', _("Quantity")))
        fields.append(('price', _("Price")))
        fields.append(('tax', _("Tax")))
        fields.append(('description', _("Description")))
        return fields


# documentos relacionados
class GenBillingDocument(CodenerixModel, GenDocumentFile):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True

    code = models.CharField(_("Code"), max_length=256, blank=False, null=False)
    date = models.DateTimeField(_("Date"), blank=False, null=False)

    def __str__(self):
        return u"{} ({})".format(self.code, self.date)

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        fields.append(('name_file', _('Name file')))
        return fields


# Documento tipo de compra
class GenPurchase(CodenerixModel):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True

    code = models.CharField(_("Code"), max_length=64, blank=False, null=False)
    date = models.DateTimeField(_("Date"), blank=False, null=False)
    observations = models.TextField(_("Observations"), max_length=256, blank=True, null=True)

    def __str__(self):
        return u"{}".format(smart_text(self.code))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('provider', _('Provider')))
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        return fields


# ################################################
class ABSTRACT_GenProvider(models.Model):  # META: Abstract class
    class Meta(object):
        abstract = True


# Proveedores
class Provider(GenRole, CodenerixModel):
    class CodenerixMeta:
        abstract = ABSTRACT_GenProvider
        rol_groups = {
            'Provider': CDNX_INVOICING_PERMISSIONS['provider'],
        }
        rol_permissions = ['list_purchaseslineinvoice', 'list_productdocument', ]
        force_methods = {
            'foreignkey_provider': ('CDNX_get_fk_info_provider', _('---')),
        }

    # person = models.OneToOneField(Person, related_name='providers', verbose_name=_("Person"))
    # saldo
    balance = models.CharField(_("Balance"), max_length=250, blank=True, null=True)
    # credito o riesgo maximo autorizado
    credit = models.CharField(_("Credit"), max_length=250, blank=True, null=True)
    billing_series = models.ForeignKey("BillingSeries", on_delete=models.CASCADE, related_name='providers', verbose_name='Billing series', blank=True, null=True)
    type_tax = models.ForeignKey(TypeTax, on_delete=models.CASCADE, related_name='providers', verbose_name=_("Type tax"), null=True)
    shipping_tax = models.FloatField(_("Impuesto de gastos de envio"), blank=True, null=True)
    finance_surcharge = models.CharField(_("Finance surcharge"), max_length=1, choices=FINANCE_SURCHARGE_STATUS_CHOICE, blank=True, null=True)
    payment_methods = models.CharField(_("Payment methods"), max_length=3, choices=PAYMENT_DETAILS, blank=True, null=True)
    delivery_time = models.SmallIntegerField(_("Delivery time (days)"), blank=False, null=False, default=1)
    categories = models.ManyToManyField(Category, blank=True, related_name='providercategories', symmetrical=False)

    @staticmethod
    def foreignkey_external():
        return get_external_method(Provider, Provider.CodenerixMeta.force_methods['foreignkey_provider'][0])

    def __str__(self):
        if hasattr(self, 'external'):
            return u"{}".format(smart_text(self.external))
        else:
            return "{}".format(self.pk)

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('balance', _("Balance")))
        fields.append(('credit', _("Credit")))
        fields.append(('billing_series', _("Billing series")))
        fields.append(('type_tax', _("Type tax")))
        fields.append(('shipping_tax', _("Impuesto de gastos de envio")))
        fields.append(('finance_surcharge', _("Finance surcharge")))
        fields.append(('payment_methods', _("Payment methods")))
        fields.append(('delivery_time', _("Delivery time")))
        fields.append(('categories', _("Categories")))
        fields = get_external_method(Provider, '__fields_provider__', info, fields)
        return fields


# customers
class GenProvider(GenInterface, ABSTRACT_GenProvider):  # META: Abstract class
    provider = models.OneToOneField(Provider, related_name='external', verbose_name=_("Provider"), null=True, on_delete=models.SET_NULL, blank=True)

    class Meta(GenInterface.Meta, ABSTRACT_GenProvider.Meta):
        abstract = True


# presupuestos
class PurchasesBudget(GenPurchase):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='budget_purchases', verbose_name=_("Provider"))


# lineas de presupuestos
class PurchasesLineBudget(GenLineProduct):
    budget = models.ForeignKey(PurchasesBudget, on_delete=models.CASCADE, related_name='line_budget_purchases', verbose_name=_("Budget"))
    product = models.ForeignKey(ProductFinal, on_delete=models.CASCADE, related_name='line_budget_purchases', verbose_name=_("Product"), null=True)

    def __fields__(self, info):
        fields = super(PurchasesLineBudget, self).__fields__(info)
        fields.insert(0, ('budget', _("Budget")))
        return fields


# documentos asociados a los presupuestos
class PurchasesBudgetDocument(GenBillingDocument):
    budget = models.ForeignKey(PurchasesBudget, on_delete=models.CASCADE, related_name='budgetdocument_purchases', verbose_name=_("Budget"))

    def __fields__(self, info):
        fields = super(PurchasesBudgetDocument, self).__fields__(info)
        fields.append(('budget', _('Budget')))
        return fields


# pedidos
class PurchasesOrder(GenPurchase):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='order_purchases', verbose_name=_("Provider"))
    budget = models.ForeignKey(PurchasesBudget, on_delete=models.CASCADE, related_name='order_purchases', verbose_name=_("Budget"), null=True, blank=True)

    def __fields__(self, info):
        fields = []
        fields.append(('provider', _('Provider')))
        fields.append(('budget', _('Budget')))
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        fields.append(('tax', _('Tax')))
        return fields


# lineas de pedidos
class PurchasesLineOrder(GenLineProduct):
    order = models.ForeignKey(PurchasesOrder, on_delete=models.CASCADE, related_name='line_order_purchases', verbose_name=_("Purchase order"))
    line_budget = models.ForeignKey(PurchasesLineBudget, on_delete=models.CASCADE, related_name='line_order_purchases', verbose_name=_("Line budget"), null=True, blank=True)
    product = models.ForeignKey(ProductFinal, on_delete=models.CASCADE, related_name='line_order_purchases', verbose_name=_("Product"), null=True, blank=True)

    def __fields__(self, info):
        fields = super(PurchasesLineOrder, self).__fields__(info)
        fields.insert(0, ('order', _("Purchases order")))
        fields.append(('line_budget', _("Line budget")))
        return fields


# documentos asociados a los pedidos
class PurchasesOrderDocument(GenBillingDocument):
    order = models.ForeignKey(PurchasesOrder, on_delete=models.CASCADE, related_name='orderdocument_purchases', verbose_name=_("Purchases order"))

    def __fields__(self, info):
        fields = super(PurchasesOrderDocument, self).__fields__(info)
        fields.append(('Order', _('Purchases order')))
        return fields


# albaranes
class PurchasesAlbaran(GenPurchase):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='albaran_purchases', verbose_name=_("Provider"))


# lineas de albaranes
class PurchasesLineAlbaran(GenLineProduct):
    albaran = models.ForeignKey(PurchasesAlbaran, on_delete=models.CASCADE, related_name='line_albaran_purchases', verbose_name=_("Albaran"))
    line_order = models.ForeignKey(PurchasesLineOrder, on_delete=models.CASCADE, related_name='line_albaran_purchases', verbose_name=_("Line orders"), blank=True, null=True)
    product = models.ForeignKey(ProductFinal, on_delete=models.CASCADE, related_name='line_albaran_purchases', verbose_name=_("Product"))
    status = models.CharField(_("Status"), max_length=2, choices=PURCHASE_ALBARAN_LINE_STATUS, blank=True, null=True, default='PR')
    # facturado
    invoiced = models.BooleanField(_("Invoiced"), blank=False, default=False)
    feature_special_value = models.TextField(_("Feature special values"), blank=True, null=True)

    def __fields__(self, info):
        fields = super(PurchasesLineAlbaran, self).__fields__(info)
        fields.insert(0, ('albaran', _("Albaran")))
        fields.append(('line_order', _("Line orders")))
        fields.append(('invoiced', _("Invoiced")))
        fields.append(('feature_special_value', _("Feature special values")))
        fields.append(('get_status_display', _("Status")))
        return fields


# documentos asociados a los albaranes
class PurchasesAlbaranDocument(GenBillingDocument):
    albaran = models.ForeignKey(PurchasesAlbaran, on_delete=models.CASCADE, related_name='albarandocument_purchases', verbose_name=_("Albaran"))

    def __fields__(self, info):
        fields = super(PurchasesAlbaranDocument, self).__fields__(info)
        fields.append(('albaran', _('Albaran')))
        return fields


# ticket y facturas son lo mismo con un check de "tengo datos del customere"
class PurchasesTicket(GenPurchase):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='ticket_purchases', verbose_name=_("Provider"))


class PurchasesLineTicket(GenLineProduct):
    ticket = models.ForeignKey(PurchasesTicket, on_delete=models.CASCADE, related_name='line_ticket_purchases', verbose_name=_("Ticket"))
    line_albaran = models.ForeignKey(PurchasesLineAlbaran, on_delete=models.CASCADE, related_name='line_ticket_purchases', verbose_name=_("Line albaran"), null=True)
    product = models.ForeignKey(ProductFinal, on_delete=models.CASCADE, related_name='line_ticket_purchases', verbose_name=_("Product"), null=True)

    def __fields__(self, info):
        fields = super(PurchasesLineTicket, self).__fields__(info)
        fields.insert(0, ('ticket', _("Ticket")))
        fields.append(('line_albaran', _("Line albaran")))
        return fields


# documentos asociados a los tickets
class PurchasesTicketDocument(GenBillingDocument):
    ticket = models.ForeignKey(PurchasesTicket, on_delete=models.CASCADE, related_name='ticketdocument_purchases', verbose_name=_("Ticket"))

    def __fields__(self, info):
        fields = super(PurchasesTicketDocument, self).__fields__(info)
        fields.append(('ticket', _('Ticket')))
        return fields


# puede haber facturas o tickets rectificativos
# factura rectificativa
class PurchasesTicketRectification(GenPurchase):
    def __fields__(self, info):
        fields = []
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        fields.append(('tax', _('Tax')))
        return fields


class PurchasesLineTicketRectification(GenLineProduct):
    ticket_rectification = models.ForeignKey(PurchasesTicketRectification, on_delete=models.CASCADE, related_name='line_ticketrectification_purchases', verbose_name=_("Ticket rectification"))
    line_ticket = models.ForeignKey(PurchasesLineTicket, on_delete=models.CASCADE, related_name='line_ticketrectification_purchases', verbose_name=_("Line ticket"))
    product = models.ForeignKey(ProductFinal, on_delete=models.CASCADE, related_name='line_ticketrectification_purchases', verbose_name=_("Product"))

    def __fields__(self, info):
        fields = super(PurchasesLineTicketRectification, self).__fields__(info)
        fields.insert(0, ('ticket_rectification', _("Ticket rectification")))
        fields.append(('line_ticket', _("Line ticket")))
        return fields


# documentos asociados a los tickets rectificativos
class PurchasesTicketRectificationDocument(GenBillingDocument):
    ticket_rectification = models.ForeignKey(PurchasesTicketRectification, on_delete=models.CASCADE, related_name='ticketrectificationdocument_purchases', verbose_name=_("Ticket rectification"))

    def __fields__(self, info):
        fields = super(PurchasesTicketRectificationDocument, self).__fields__(info)
        fields.append(('ticket_rectification', _('Ticket rectification')))
        return fields


# facturas
# una factura puede contener varios ticket o albaranes
class PurchasesInvoice(GenPurchase):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='invoice_purchases', verbose_name=_("Provider"))


class PurchasesLineInvoice(GenLineProduct):
    invoice = models.ForeignKey(PurchasesInvoice, on_delete=models.CASCADE, related_name='line_invoice_purchases', verbose_name=_("Invoice"))
    line_albaran = models.ForeignKey(PurchasesLineAlbaran, on_delete=models.CASCADE, related_name='line_invoice_purchases', verbose_name=_("Line albaran"), blank=True, null=True)
    product = models.ForeignKey(ProductFinal, on_delete=models.CASCADE, related_name='line_invoice_purchases', verbose_name=_("Product"))
    feature_special_value = models.TextField(_("Feature special values"), blank=True, null=True)

    def __fields__(self, info):
        fields = super(PurchasesLineInvoice, self).__fields__(info)
        fields.insert(0, ('invoice', _("Invoices")))
        fields.append(('line_albaran', _("Line albaran")))
        fields.append(('feature_special_value', _("Feature special values")))
        return fields


# documentos asociados a las facturas
class PurchasesInvoiceDocument(GenBillingDocument):
    invoice = models.ForeignKey(PurchasesInvoice, on_delete=models.CASCADE, related_name='invoicedocument_purchases', verbose_name=_("Invoice"))

    def __fields__(self, info):
        fields = super(PurchasesInvoiceDocument, self).__fields__(info)
        fields.append(('invoice', _('Invoice')))
        return fields


# factura rectificativa
class PurchasesInvoiceRectification(GenPurchase):
    def __fields__(self, info):
        fields = []
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        fields.append(('tax', _('Tax')))
        return fields


class PurchasesLineInvoiceRectification(GenLineProduct):
    invoice_rectification = models.ForeignKey(PurchasesInvoiceRectification, on_delete=models.CASCADE, related_name='line_invoicerectification_purchases', verbose_name=_("Invoice rectification"))
    line_invoice = models.ForeignKey(PurchasesLineInvoice, on_delete=models.CASCADE, related_name='line_invoicerectification_purchases', verbose_name=_("Line invoice"))
    product = models.ForeignKey(ProductFinal, on_delete=models.CASCADE, related_name='line_invoicerectification_purchases', verbose_name=_("Product"))

    def __fields__(self, info):
        fields = super(PurchasesLineInvoiceRectification, self).__fields__(info)
        fields.insert(0, ('invoice_rectification', _("Invoices rectification")))
        fields.append(('line_invoice', _("Line invoice")))
        return fields


# documentos asociados a las facturas rectificativas
class PurchasesInvoiceRectificationDocument(GenBillingDocument):
    invoice_rectification = models.ForeignKey(PurchasesInvoiceRectification, on_delete=models.CASCADE, related_name='invoicerectificationdocument_purchases', verbose_name=_("Invoice rectification"))

    def __fields__(self, info):
        fields = super(PurchasesInvoiceRectificationDocument, self).__fields__(info)
        fields.append(('invoice_rectification', _('Invoice rectification')))
        return fields
