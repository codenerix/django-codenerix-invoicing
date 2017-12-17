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

from django import forms
from django.utils.translation import ugettext as _

from codenerix.forms import GenModelForm
from codenerix.widgets import WysiwygAngularInput
from codenerix_extensions.helpers import get_external_model, get_external_method
from codenerix_products.models import TypeTax

from .models_sales import Address
from .models_sales import Customer, CustomerDocument
from .models_sales import SalesBasket, SalesLineBasket
from .models_sales import SalesOrder, SalesLineOrder, SalesOrderDocument
from .models_sales import SalesAlbaran, SalesLineAlbaran
from .models_sales import SalesTicket, SalesLineTicket
from .models_sales import SalesTicketRectification, SalesLineTicketRectification
from .models_sales import SalesInvoice, SalesLineInvoice
from .models_sales import SalesInvoiceRectification, SalesLineInvoiceRectification
from .models_sales import SalesReservedProduct
from .models_sales import ReasonModification, ReasonModificationLineBasket, ReasonModificationLineOrder, ReasonModificationLineAlbaran, ReasonModificationLineTicket, ReasonModificationLineTicketRectification, ReasonModificationLineInvoice, ReasonModificationLineInvoiceRectification


class CustomerForm(GenModelForm):
    codenerix_external_field = forms.ModelChoiceField(
        label=Customer.foreignkey_external()['label'],
        queryset=get_external_model(Customer).objects.all()
    )

    class Meta:
        model = Customer
        exclude = ['balance', 'default_customer', ]
        autofill = {
            'codenerix_external_field': ['select', 3, Customer.foreignkey_external()['related']],
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['codenerix_external_field', 8],
                ['billing_series', 2],
                ['currency', 2],
                ['credit', 3],
                ['final_balance', 3],
                ['type_tax', 3],
                ['apply_equivalence_surcharge', 3],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['codenerix_external_field', 6],
                ['credit', 6],
                ['currency', 6],
                ['billing_series', 6],
                ['final_balance', 6],
                ['apply_equivalence_surcharge', 3],
                ['type_tax', 3],)
        ]
        return g

    @staticmethod
    def __groups_details_profile__():
        g = [
            (_('Details'), 12,
                ['billing_series', 6],
                ['credit', 6],
                ['currency', 6],
                ['final_balance', 6],
                ['apply_equivalence_surcharge', 3],
                ['type_tax', 3],)
        ]
        return g


class CustomerDocumentForm(GenModelForm):
    class Meta:
        model = CustomerDocument
        exclude = ['name_file', 'customer']

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['type_document', 6],
                ['doc_path', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['customer', 6],
                ['type_document', 6],
                ['doc_path', 6],
                ['name_file', 6],)
        ]
        return g


class BasketForm(GenModelForm):
    class Meta:
        model = SalesBasket
        exclude = ['lock', 'code', 'parent_pk', 'payment', 'role']
        widgets = {
            'observations': WysiwygAngularInput()
        }
        autofill = {
            'address_delivery': ['select', 3, Address.foreignkey_external_delivery()['related'], 'customer'],
            'address_invoice': ['select', 3, Address.foreignkey_external_invoice()['related'], 'customer'],
        }

    def __groups__(self):
        g = [
            (_('Basket'), 12,
                ['customer', 6],
                ['date', 2],
                ['signed', 2],
                ['public', 2],
                ['billing_series', 4],
                ['address_delivery', 4],
                ['address_invoice', 4],
                ['name', 4],
                ['pos_slot', 4],
                ['haulier', 4],
                ['observations', 12],),
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Basket'), 12,
                ['customer', 5],
                ['name', 5],
                ['signed', 2],
                ['public', 2],
                ['code', 3],
                ['billing_series', 4],
                ['date', 4],
                ['observations', 6],
                ['address_delivery', 6],
                ['address_invoice', 6],
                ['lock', 6],
                ['role', 6],
                ['haulier', 4],
                ['pos_slot', 6],),
            (
                _('Total'), 12,
                ['subtotal', 6],
                ['discounts', 6],
                ['taxes', 6],
                ['total', 6],
            )
        ]
        return g


class LineBasketForm(GenModelForm):
    price = forms.FloatField(label=_('Price with tax'), widget=forms.NumberInput(attrs={"disabled": 'disabled'}))
    tax = forms.FloatField(label=_('Tax hidden'), widget=forms.NumberInput(attrs={"disabled": 'disabled'}))
    type_tax = forms.ModelChoiceField(label=_('Tax'), queryset=TypeTax.objects.all())

    class Meta:
        model = SalesLineBasket
        exclude = ['basket', 'price_recommended', 'equivalence_surcharges', 'equivalence_surcharge', 'tax_label', 'code']
        autofill = {
            'product': ['select', 3, 'CDNX_products_productfinals_foreign_sales', ],
            'type_tax': ['select', 3, 'CDNX_products_typetaxs_foreing', ],
        }
        widgets = {
            'notes': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['product', 6],
                ['description', 6],
                ['quantity', 6],
                ['price_base', 6, {'extra': ['ng-controller=codenerixSalesLineBasketCtrl', 'ng-change=update_price()']}],
                ['price', 6],
                ['type_tax', 6, {'extra': ['ng-controller=codenerixSalesLineBasketCtrl', 'ng-blur=update_price()']}],
                ['tax', 6],
                ['discount', 6],
                ['notes', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['budget', 6],
                ['product', 6],
                ['description', 6],
                ['quantity', 6],
                ['price_base', 6],
                ['price_recommended', 6],
                ['discount', 6],
                ['tax', 6],
                ['notes', 12]),
        ]
        return g


class LineBasketFormPack(GenModelForm):
    packs = forms.CharField()  # widget=forms.HiddenInput())

    class Meta:
        model = SalesLineBasket
        exclude = ['basket', 'price_recommended', 'tax', ]
        autofill = {
            'product': ['select', 3, 'CDNX_products_productfinals_foreign_sales_pack', ],
        }
        widgets = {
            'notes': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['product', 6],
                ['description', 6],
                ['quantity', 6],
                ['price_base', 6],
                ['discount', 6],
                ['notes', 6],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['budget', 6],
                ['product', 6],
                ['description', 6],
                ['quantity', 6],
                ['price_base', 6],
                ['price_recommended', 6],
                ['discount', 6],
                ['tax', 6],
                ['notes', 12]),
        ]
        return g


class OrderFromBudgetForm(GenModelForm):
    class Meta:
        model = SalesOrder
        fields = ['customer', 'budget', 'billing_series']
        autofill = {
            'customer': ['select', 3, 'CDNX_invoicing_customers_foreign_from_budget'],
            'budget': ['select', 3, 'CDNX_invoicing_salesbaskets_foreignkey_budget', 'customer'],
        }

    def __groups__(self):
        g = [
            (_('Select budget'), 12,
                ['customer', 4],
                ['billing_series', 4],
                ['budget', 4],)
        ]
        return g


class OrderFromShoppingCartForm(GenModelForm):
    class Meta:
        model = SalesOrder
        fields = ['customer', 'budget', 'billing_series']
        autofill = {
            'customer': ['select', 3, 'CDNX_invoicing_customers_foreign_from_shoppingcart'],
            'budget': ['select', 3, 'CDNX_invoicing_salesbaskets_foreignkey_shoppingcart', 'customer'],
        }

    def __groups__(self):
        g = [
            (_('Select budget'), 12,
                ['customer', 4],
                ['billing_series', 4],
                ['budget', 4],)
        ]
        return g


class OrderForm(GenModelForm):
    class Meta:
        model = SalesOrder
        exclude = ['lock', 'code', 'parent_pk', 'budget', 'payment']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['customer', 4],
                ['billing_series', 2],
                ['date', 2],
                ['storage', 4],
                ['status_order', 4],
                ['payment_detail', 4],
                ['source', 4],
                ['number_tracking', 6],
                ['observations', 12],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        info_customer = get_external_method(Customer, Customer.CodenerixMeta.force_methods['info_customer_details'][0])

        g = [
            (
                _('Details'), 12,
                ['customer', 6],
                ['budget', 6],
                ['date', 6],
                ['code', 6],
                ['billing_series', 2],
                ['storage', 6],
                ['status_order', 6],
                ['payment_detail', 6],
                ['payment', 6],
                ['source', 6],
                ['number_tracking', 6],
                ['observations', 6],
                ['lock', 6],
            ),
        ]
        if info_customer:
            for info in info_customer:
                g.append(info)
        g.append(
            (
                _('Total'), 12,
                ['subtotal', 6],
                ['discounts', 6],
                ['taxes', 6],
                ['total', 6],
            )
        )
        return g


class LineOrderForm(GenModelForm):
    class Meta:
        model = SalesLineOrder
        exclude = ['order', 'line_budget', 'tax', 'price_recommended', 'equivalence_surcharge', 'equivalence_surcharges']
        autofill = {
            'product': ['select', 3, 'CDNX_products_productfinals_foreign_sales'],
        }
        widgets = {
            'notes': WysiwygAngularInput()
        }

    def clean(self):
        cleaned_data = super(LineOrderForm, self).clean()
        product = cleaned_data.get('product')
        if product.product.force_stock:
            quantity = cleaned_data.get('quantity')
            if product.stock_real < quantity:
                self.add_error("quantity", _("No hay tantos productos en Stock"))

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['product', 6],
                ['description', 6],
                ['quantity', 6],
                ['price_base', 6],
                ['discount', 6],
                ['notes', 12])
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['order', 6],
                ['line_budget', 6],
                ['product', 6],
                ['description', 6],
                ['quantity', 6],
                ['price_base', 6],
                ['price_recommended', 6],
                ['discount', 6],
                ['tax', 6],
                ['notes', 6],)
        ]
        return g


class LineOrderFormEdit(LineOrderForm):
    reason = forms.ModelChoiceField(label=_('Reason of modification'), queryset=ReasonModification.objects.all().order_by('code'))

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['product', 6],
                ['description', 6],
                ['quantity', 6],
                ['price_base', 6],
                ['discount', 6],
                ['reason', 6],
                ['notes', 12])
        ]
        return g


class OrderDocumentForm(GenModelForm):
    class Meta:
        model = SalesOrderDocument
        exclude = ['name_file']
        widgets = {
            'notes': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['order', 6],
                ['kind', 6],
                ['doc_path', 6],
                ['notes', 12],
            ),
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['order', 6],
                ['name_file', 6],
                ['kind', 6],
                ['doc_path', 6],
                ['notes', 6],
            )
        ]
        return g


class OrderDocumentSublistForm(GenModelForm):
    class Meta:
        model = SalesOrderDocument
        exclude = ['name_file', 'order']
        widgets = {
            'notes': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['kind', 6],
                ['doc_path', 6],
                ['notes', 12],
            ),
        ]
        return g


class AlbaranForm(GenModelForm):
    class Meta:
        model = SalesAlbaran
        exclude = ['lock', 'code', 'parent_pk']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['date', 6],
                ['billing_series', 6],
                ['summary_delivery', 6],
                ['observations', 6],),
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['date', 6],
                ['code', 6],
                ['billing_series', 6],
                ['summary_delivery', 6],
                ['lock', 6],
                ['observations', 6],),
            (
                _('Total'), 12,
                ['subtotal', 6],
                ['discounts', 6],
                ['taxes', 6],
                ['total', 6],
            )
        ]
        return g


class LineAlbaranForm(GenModelForm):
    albaran_pk = forms.IntegerField(widget=forms.HiddenInput())
    order = forms.ModelChoiceField(label=_('Sales order'), queryset=SalesOrder.objects.all())

    class Meta:
        model = SalesLineAlbaran
        exclude = ['albaran', 'invoiced']
        autofill = {
            'order': ['select', 3, 'CDNX_invoicing_ordersaless_foreign', 'albaran_pk'],
            'line_order': ['select', 3, 'CDNX_invoicing_lineordersaless_foreign', 'order'],
        }
        widgets = {
            'notes': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['order', 5],
                ['line_order', 5],
                ['quantity', 2],
                ['notes', 12])
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['albaran', 6],
                ['line_order', 6],
                ['line_order__product', 6],
                ['line_order__description', 6],
                ['invoiced', 6],
                ['quantity', 6],
                ['line_order__price_base', 6],
                ['line_order__price_recommended', 6],
                ['line_order__discount', 6],
                ['line_order__tax', 6],
                ['notes', 6])
        ]
        return g


class TicketForm(GenModelForm):
    class Meta:
        model = SalesTicket
        exclude = ['lock', 'code', 'parent_pk']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['customer', 6],
                ['billing_series', 3],
                ['date', 3],
                ['observations', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['customer', 6],
                ['date', 6],
                ['code', 6],
                ['billing_series', 6],
                ['lock', 6],
                ['observations', 6],),
            (
                _('Total'), 12,
                ['subtotal', 6],
                ['discounts', 6],
                ['taxes', 6],
                ['total', 6],
            )
        ]
        return g


class LineTicketForm(GenModelForm):
    ticket_pk = forms.IntegerField(widget=forms.HiddenInput())
    order = forms.ModelChoiceField(label=_('Sales order'), queryset=SalesOrder.objects.all())

    class Meta:
        model = SalesLineTicket
        exclude = ['ticket', 'tax', 'price_recommended']
        autofill = {
            'order': ['select', 3, 'CDNX_invoicing_ordersaless_foreign', 'ticket_pk'],
            'line_order': ['select', 3, 'CDNX_invoicing_lineordersaless_foreign_custom', 'order'],
        }
        widgets = {
            'notes': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['order', 6],
                ['line_order', 6],
                ['description', 6],
                ['quantity', 6],
                ['price_base', 6],
                ['discount', 6],
                ['notes', 12])
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['ticket', 6],
                ['line_order', 6],
                ['line_order__product', 6],
                ['description', 6],
                ['quantity', 6],
                ['discount', 6],
                ['price_base', 6],
                ['price_recommended', 6],
                ['tax', 6],
                ['notes', 6])
        ]
        return g


class TicketRectificationForm(GenModelForm):
    class Meta:
        model = SalesTicketRectification
        exclude = ['lock', 'parent_pk', 'code']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['date', 4],
                ['billing_series', 4],
                ['ticket', 4],
                ['observations', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['ticket', 6],
                ['date', 6],
                ['code', 6],
                ['tax', 6],
                ['observations', 6],),
            (
                _('Total'), 12,
                ['subtotal', 6],
                ['discounts', 6],
                ['taxes', 6],
                ['total', 6],
            )
        ]
        return g


class TicketRectificationUpdateForm(GenModelForm):
    class Meta:
        model = SalesTicketRectification
        exclude = ['lock', 'parent_pk', 'ticket', 'code']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['date', 6],
                ['billing_series', 6],
                ['observations', 12],)
        ]
        return g


class LineTicketRectificationForm(GenModelForm):
    ticket_rectification_pk = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = SalesLineTicketRectification
        exclude = ['ticket_rectification', 'equivalence_surcharges']
        autofill = {
            'line_ticket': ['select', 3, 'CDNX_invoicing_lineticketsaless_foreign', 'ticket_rectification_pk'],
        }
        widgets = {
            'notes': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['line_ticket', 6],
                ['quantity', 6],
                ['notes', 12])
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['ticket_rectification', 6],
                ['line_ticket', 6],
                ['line_ticket__product', 6],
                ['line_ticket__description', 6],
                ['quantity', 6],
                ['line_ticket__price_base', 6],
                ['line_ticket__tax', 6],
                ['line_ticket__price_recommended', 6],
                ['line_ticket__discount', 6],
                ['notes', 6])
        ]
        return g


class LineTicketRectificationLinkedForm(GenModelForm):
    class Meta:
        model = SalesLineTicketRectification
        exclude = ['ticket_rectification', 'line_ticket', 'equivalence_surcharges']
        widgets = {
            'notes': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['quantity', 3],
                ['notes', 9])
        ]
        return g


class InvoiceForm(GenModelForm):
    class Meta:
        model = SalesInvoice
        exclude = ['lock', 'code', 'parent_pk']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['customer', 4],
                ['date', 4],
                ['billing_series', 4],
                ['summary_invoice', 6],
                ['observations', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['customer', 6],
                ['date', 6],
                ['code', 6],
                ['billing_series', 6],
                ['observations', 6],
                ['summary_invoice']
            ),
            (
                _('Total'), 12,
                ['subtotal', 6],
                ['discounts', 6],
                ['taxes', 6],
                ['total', 6],
            )
        ]
        return g


class LineInvoiceForm(GenModelForm):
    invoice_pk = forms.IntegerField(widget=forms.HiddenInput())
    order = forms.ModelChoiceField(label=_('Sales order'), queryset=SalesOrder.objects.all())

    class Meta:
        model = SalesLineInvoice
        exclude = ['invoice', 'tax', 'price_recommended', 'equivalence_surcharges', 'equivalence_surcharge']
        autofill = {
            'order': ['select', 3, 'CDNX_invoicing_ordersaless_foreign', 'invoice_pk'],
            'line_order': ['select', 3, 'CDNX_invoicing_lineordersaless_foreign_custom', 'order'],
        }
        widgets = {
            'notes': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['order', 6],
                ['line_order', 6],
                ['description', 12],
                ['quantity', 4],
                ['price_base', 4],
                ['discount', 4],
                ['notes', 12])
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['invoice', 6],
                ['line_order', 6],
                ['product', 6],
                ['description', 6],
                ['quantity', 6],
                ['price_base', 6],
                ['price_recommended', 6],
                ['discount', 6],
                ['tax', 6],
                ['notes', 6])
        ]
        return g


class InvoiceRectificationForm(GenModelForm):
    class Meta:
        model = SalesInvoiceRectification
        exclude = ['lock', 'code', 'parent_pk']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['date', 6],
                ['invoice', 6],
                ['billing_series', 6],
                ['observations', 6],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['invoice', 6],
                ['date', 6],
                ['code', 6],
                ['observations', 6],),
            (
                _('Total'), 12,
                ['subtotal', 6],
                ['discounts', 6],
                ['taxes', 6],
                ['total', 6],
            )
        ]
        return g


class InvoiceRectificationUpdateForm(GenModelForm):
    class Meta:
        model = SalesInvoiceRectification
        exclude = ['lock', 'code', 'parent_pk', 'invoice']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['date', 6],
                ['billing_series', 6],
                ['observations', 12],)
        ]
        return g


class LineInvoiceRectificationForm(GenModelForm):
    invoice_rectification_pk = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = SalesLineInvoiceRectification
        exclude = ['invoice_rectification']
        autofill = {
            'line_invoice': ['select', 3, 'CDNX_invoicing_lineinvoicessaless_foreign', 'invoice_rectification_pk'],
        }
        widgets = {
            'notes': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['line_invoice', 6],
                ['quantity', 6],
                ['notes', 12])
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['invoice_rectification', 6],
                ['line_invoice', 6],
                ['line_invoice__description', 6],
                ['quantity', 6],
                ['line_invoice__price_base', 6],
                ['line_invoice__tax', 6],
                ['line_invoice__discount', 6],
                ['notes', 6])
        ]
        return g


class LineInvoiceRectificationLinkedForm(GenModelForm):
    class Meta:
        model = SalesLineInvoiceRectification
        exclude = ['invoice_rectification', 'line_invoice']
        widgets = {
            'notes': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['quantity', 3],
                ['notes', 9])
        ]
        return g


class ReservedProductForm(GenModelForm):
    class Meta:
        model = SalesReservedProduct
        exclude = []

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['customer', 4],
                ['product', 4],
                ['quantity', 4],)
        ]
        return g


class ReasonModificationForm(GenModelForm):
    class Meta:
        model = ReasonModification
        exclude = []

    def __groups__(self):
        return [
            (
                _('Details'), 12,
                ['code', 6],
                ['name', 6],
                ['enable', 6],
            )
        ]

    @staticmethod
    def __groups_details__():
        return [
            (
                _('Details'), 12,
                ['code', 6],
                ['name', 6],
                ['enable', 6],
            )
        ]


class ReasonModificationLineForm(GenModelForm):
    doc = forms.FloatField(label=_('Document'), widget=forms.NumberInput(attrs={"disabled": 'disabled'}))

    class Meta:
        exclude = ['user', ]

    def __groups__(self):
        return [
            (
                _('Details'), 12,
                ['date', 6],
                ['line', 6],
                ['reason', 6],
                ['quantity', 6],
                ['doc', 6]
            )
        ]

    @staticmethod
    def __groups_details__():
        return [
            (
                _('Details'), 12,
                ['date', 6],
                ['line', 6],
                ['reason', 6],
                ['quantity', 6],
            )
        ]


class ReasonModificationLineBasketForm(ReasonModificationLineForm):
    class Meta(ReasonModificationLineForm.Meta):
        model = ReasonModificationLineBasket
        autofill = {
            'line': ['select', 3, 'CDNX_invoicing_linebasketsaless_foreign', 'doc']
        }


class ReasonModificationLineOrderForm(ReasonModificationLineForm):
    class Meta(ReasonModificationLineForm.Meta):
        model = ReasonModificationLineOrder
        autofill = {
            'line': ['select', 3, 'CDNX_invoicing_lineordersaless_foreign', 'doc']
        }


class ReasonModificationLineAlbaranForm(ReasonModificationLineForm):
    class Meta(ReasonModificationLineForm.Meta):
        model = ReasonModificationLineAlbaran
        autofill = {
            'line': ['select', 3, 'CDNX_invoicing_linealbaransaless_foreign', 'doc']
        }


class ReasonModificationLineTicketForm(ReasonModificationLineForm):
    class Meta(ReasonModificationLineForm.Meta):
        model = ReasonModificationLineTicket
        autofill = {
            'line': ['select', 3, 'CDNX_invoicing_lineticketsaless_foreign', 'doc']
        }


class ReasonModificationLineTicketRectificationForm(ReasonModificationLineForm):
    class Meta(ReasonModificationLineForm.Meta):
        model = ReasonModificationLineTicketRectification
        autofill = {
            'line': ['select', 3, 'CDNX_invoicing_lineticketrectificationsaless_sublist_foreign', 'doc']
        }


class ReasonModificationLineInvoiceForm(ReasonModificationLineForm):
    class Meta(ReasonModificationLineForm.Meta):
        model = ReasonModificationLineInvoice
        autofill = {
            'line': ['select', 3, 'CDNX_invoicing_lineinvoicessaless_foreign', 'doc']
        }


class ReasonModificationLineInvoiceRectificationForm(ReasonModificationLineForm):
    class Meta(ReasonModificationLineForm.Meta):
        model = ReasonModificationLineInvoiceRectification
        autofill = {
            'line': ['select', 3, 'CDNX_invoicing_lineinvoicerectificationsaless_sublist_foreign', 'doc']
        }
