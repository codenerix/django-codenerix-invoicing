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
from codenerix_extensions.helpers import get_external_model

from codenerix_invoicing.models_sales import Customer, CustomerDocument, \
    SalesOrder, SalesLineOrder, SalesAlbaran, SalesLineAlbaran, SalesTicket, SalesLineTicket, \
    SalesTicketRectification, SalesLineTicketRectification, SalesInvoice, SalesLineInvoice, SalesInvoiceRectification, \
    SalesLineInvoiceRectification, SalesReservedProduct, \
    SalesBasket, SalesLineBasket


class CustomerForm(GenModelForm):
    codenerix_external_field = forms.ModelChoiceField(
        label=Customer.foreignkey_external()['label'],
        queryset=get_external_model(Customer).objects.all()
    )

    class Meta:
        model = Customer
        exclude = ['balance']
        autofill = {
            'codenerix_external_field': ['select', 3, Customer.foreignkey_external()['related']],
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['codenerix_external_field', 6],
                ['billing_series', 3],
                ['currency', 3],
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
                ['person', 6],
                ['billing_series', 6],
                ['credit', 6],
                ['currency', 6],
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
        exclude = ['customer']

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['type_document', 6],
                ['doc_path', 6],
                ['name_file', 6],)
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
            'address_delivery': ['select', 3, 'CDNX_invoicing_salesbaskets_foreignkey_budget', 'customer'],
            'address_invoice': ['select', 3, 'CDNX_invoicing_salesbaskets_foreignkey_budget', 'customer'],
        }

    def __groups__(self):
        g = [
            (_('Basket'), 12,
                ['customer', 6],
                ['date', 2],
                ['signed', 2],
                ['public', 2],
                ['address_delivery', 6],
                ['address_invoice', 6],
                ['name', 4],
                ['point_sales', 4],
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
                ['date', 4],
                ['observations', 6],
                ['address_delivery', 6],
                ['address_invoice', 6],
                ['lock', 6],
                ['role', 6],
                ['haulier', 4],
                ['point_sales', 6],),
        ]
        return g


class LineBasketForm(GenModelForm):
    class Meta:
        model = SalesLineBasket
        exclude = ['basket', 'price_recommended', 'tax', ]
        autofill = {
            'product': ['select', 3, 'CDNX_products_productfinals_foreign_sales', ],
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
                ['price', 6],
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
                ['price', 6],
                ['price_recommended', 6],
                ['discount', 6],
                ['tax', 6],
                ['notes', 12]),
        ]
        return g


class OrderFromBudgetForm(GenModelForm):
    class Meta:
        model = SalesOrder
        fields = ['customer', 'budget']
        autofill = {
            'customer': ['select', 3, 'CDNX_invoicing_customers_foreign_from_budget'],
            'budget': ['select', 3, 'CDNX_invoicing_salesbaskets_foreignkey_budget', 'customer'],
        }

    def __groups__(self):
        g = [
            (_('Select budget'), 12,
                ['customer', 6],
                ['budget', 6],)
        ]
        return g


class OrderFromShoppingCartForm(GenModelForm):
    class Meta:
        model = SalesOrder
        fields = ['customer', 'budget']
        autofill = {
            'customer': ['select', 3, 'CDNX_invoicing_customers_foreign_from_budget'],
            'budget': ['select', 3, 'CDNX_invoicing_salesbaskets_foreignkey_shoppingcart', 'customer'],
        }

    def __groups__(self):
        g = [
            (_('Select budget'), 12,
                ['customer', 6],
                ['budget', 6],)
        ]
        return g


class OrderForm(GenModelForm):
    class Meta:
        model = SalesOrder
        exclude = ['lock', 'code', 'parent_pk']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['customer', 4],
                ['date', 4],
                ['storage', 4],
                ['status_order', 4],
                ['payment_detail', 4],
                ['source', 4],
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
                ['storage', 6],
                ['status_order', 6],
                ['payment_detail', 6],
                ['source', 6],
                ['observations', 6],
                ['lock', 6],)
        ]
        return g


class LineOrderForm(GenModelForm):
    class Meta:
        model = SalesLineOrder
        exclude = ['order', 'line_budget', 'tax', 'price_recommended']
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
                ['price', 6],
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
                ['price', 6],
                ['price_recommended', 6],
                ['discount', 6],
                ['tax', 6],
                ['notes', 6],)
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
                ['tax', 6],
                ['observations', 12],),
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['date', 6],
                ['code', 6],
                ['tax', 6],
                ['lock', 6],
                ['observations', 6],)
        ]
        return g


class LineAlbaranForm(GenModelForm):
    albaran_pk = forms.IntegerField(widget=forms.HiddenInput())
    order = forms.ModelChoiceField(label=_('Order'), queryset=SalesOrder.objects.all())

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
                ['line_order__price', 6],
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
                ['customer', 4],
                ['date', 4],
                ['tax', 4],
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
                ['tax', 6],
                ['lock', 6],
                ['observations', 6],)
        ]
        return g


class LineTicketForm(GenModelForm):
    ticket_pk = forms.IntegerField(widget=forms.HiddenInput())
    order = forms.ModelChoiceField(label=_('Order'), queryset=SalesOrder.objects.all())

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
                ['price', 6],
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
                ['price', 6],
                ['price_recommended', 6],
                ['tax', 6],
                ['notes', 6])
        ]
        return g


class TicketRectificationForm(GenModelForm):
    class Meta:
        model = SalesTicketRectification
        exclude = ['lock', 'parent_pk']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['date', 4],
                ['code', 4],
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
                ['observations', 6],)
        ]
        return g


class TicketRectificationUpdateForm(GenModelForm):
    class Meta:
        model = SalesTicketRectification
        exclude = ['lock', 'parent_pk', 'ticket']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['date', 6],
                ['code', 6],
                ['observations', 12],)
        ]
        return g


class LineTicketRectificationForm(GenModelForm):
    ticket_rectification_pk = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = SalesLineTicketRectification
        exclude = ['ticket_rectification']
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
                ['line_ticket__price', 6],
                ['line_ticket__tax', 6],
                ['line_ticket__price_recommended', 6],
                ['line_ticket__discount', 6],
                ['notes', 6])
        ]
        return g


class LineTicketRectificationLinkedForm(GenModelForm):
    class Meta:
        model = SalesLineTicketRectification
        exclude = ['ticket_rectification', 'line_ticket']
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
            (_('Details'), 12,
                ['customer', 4],
                ['date', 4],
                ['tax', 4],
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
                ['tax', 6],
                ['observations', 6],)
        ]
        return g


class LineInvoiceForm(GenModelForm):
    invoice_pk = forms.IntegerField(widget=forms.HiddenInput())
    order = forms.ModelChoiceField(label=_('Order'), queryset=SalesOrder.objects.all())

    class Meta:
        model = SalesLineInvoice
        exclude = ['invoice', 'tax', 'price_recommended']
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
                ['line_order', 6],
                ['description', 6],
                ['order', 6],
                ['quantity', 6],
                ['price', 6],
                ['discount', 6],
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
                ['price', 6],
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
                ['tax', 6],
                ['observations', 6],)
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
                ['observations', 6],)
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
                ['line_invoice__price', 6],
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
