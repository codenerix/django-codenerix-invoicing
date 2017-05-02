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
from codenerix_extensions.helpers import get_external_model
from codenerix.widgets import WysiwygAngularInput, MultiStaticSelect

from codenerix_invoicing.models_purchases import Provider, \
    PurchasesBudget, PurchasesLineBudget, PurchasesOrder, PurchasesLineOrder, PurchasesAlbaran, PurchasesLineAlbaran, \
    PurchasesTicket, PurchasesLineTicket, PurchasesTicketRectification, PurchasesLineTicketRectification, PurchasesInvoice, \
    PurchasesLineInvoice, PurchasesInvoiceRectification, PurchasesLineInvoiceRectification, PurchasesBudgetDocument, \
    PurchasesOrderDocument, PurchasesAlbaranDocument, PurchasesTicketDocument, PurchasesTicketRectificationDocument, \
    PurchasesInvoiceDocument, PurchasesInvoiceRectificationDocument

from codenerix_storages.models import Storage, StorageZone, StorageBatch
from codenerix_products.models import Category


class ProviderForm(GenModelForm):
    codenerix_external_field = forms.ModelChoiceField(
        label=Provider.foreignkey_external()['label'],
        queryset=get_external_model(Provider).objects.all()
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        label=_('Categories'),
        required=False,
        widget=MultiStaticSelect(
            attrs={'manytomany': True}
        )
    )

    class Meta:
        model = Provider
        exclude = []
        autofill = {
            'codenerix_external_field': ['select', 3, Provider.foreignkey_external()['related']],
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['codenerix_external_field', 4],
                ['balance', 4],
                ['billing_series', 4],
                ['type_tax', 4],
                ['shipping_tax', 4],
                ['finance_surcharge', 4],
                ['credit', 4],
                ['payment_methods', 4],
                ['delivery_time', 4],
                ['categories', 8],)
        ]
        return g
    
    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['codenerix_external_field', 6],
                ['balance', 6],
                ['billing_series', 6],
                ['type_tax', 6],
                ['shipping_tax', 6],
                ['finance_surcharge', 6],
                ['credit', 6],
                ['payment_methods', 6],
                ['delivery_time', 6],)
        ]
        return g


class BudgetForm(GenModelForm):
    class Meta:
        model = PurchasesBudget
        exclude = ['lock', 'parent_pk', ]
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['provider', 6],
                ['date', 2],
                ['code', 2],
                ['tax', 2],
                ['observations', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['provider', 6],
                ['date', 6],
                ['code', 6],
                ['tax', 6],
                ['observations', 6],)
        ]
        return g


class LineBudgetForm(GenModelForm):
    class Meta:
        model = PurchasesLineBudget
        exclude = ['budget', ]

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['product', 6],
                ['quantity', 6],
                ['price', 6],
                ['tax', 6],
                ['description', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['budget', 6],
                ['product', 6],
                ['quantity', 6],
                ['price', 6],
                ['description', 6],
                ['tax', 6],)
        ]
        return g


class OrderForm(GenModelForm):
    class Meta:
        model = PurchasesOrder
        exclude = ['lock', 'parent_pk']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['provider', 6],
                ['budget', 6],
                ['code', 4],
                ['tax', 4],
                ['date', 4],
                ['observations', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['code', 6],
                ['provider', 6],
                ['date', 6],
                ['budget', 6],
                ['tax', 6],
                ['observations', 6],)
        ]
        return g


class OrderFromBudgetForm(GenModelForm):
    class Meta:
        model = PurchasesOrder
        exclude = ['lock', 'parent_pk', 'budget', 'tax', 'provider']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['code', 6],
                ['date', 6],
                ['observations', 6],)
        ]
        return g


class LineOrderForm(GenModelForm):
    class Meta:
        model = PurchasesLineOrder
        exclude = ['order', ]

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['line_budget', 6],
                ['product', 6],
                ['quantity', 4],
                ['price', 4],
                ['tax', 4],
                ['description', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['order', 6],
                ['line_budget', 6],
                ['product', 6],
                ['quantity', 6],
                ['price', 6],
                ['description', 6],
                ['tax', 6],)
        ]
        return g


class AlbaranForm(GenModelForm):
    class Meta:
        model = PurchasesAlbaran
        exclude = ['lock', 'parent_pk']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['code', 4],
                ['provider', 4],
                ['date', 2],
                ['tax', 2],
                ['observations', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['date', 6],
                ['provider', 6],
                ['code', 6],
                ['tax', 6],
                ['observations', 6],)
        ]
        return g


class LineAlbaranForm(GenModelForm):
    storage = forms.ModelChoiceField(label=_('Storage'), queryset=Storage.objects.all())
    zone = forms.ModelChoiceField(label=_('Zone'), queryset=StorageZone.objects.all())
    batch = forms.ModelChoiceField(label=_('Batch'), queryset=StorageBatch.objects.all())

    class Meta:
        model = PurchasesLineAlbaran
        exclude = ['albaran', ]

    def __groups__(self):
        g = [
            (_('Storage'), 12,
                ['storage', 4],
                ['zone', 4],
                ['batch', 4],
            ),
            (_('Details'), 12,
                ['product', 12],
                ['line_order', 4],
                ['status', 4],
                ['invoiced', 4],
                ['price', 4],
                ['quantity', 4],
                ['tax', 4],
                ['description', 6],
                ['feature_special_value', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['albaran', 6],
                ['line_order', 6],
                ['product', 6],
                ['price', 6],
                ['quantity', 6],
                ['description', 6],
                ['feature_special_value', 6],
                ['invoiced', 6],
                ['tax', 6],
                ['status'],)
        ]
        return g


class TicketForm(GenModelForm):
    class Meta:
        model = PurchasesTicket
        exclude = ['lock', 'parent_pk']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['code', 4],
                ['provider', 4],
                ['date', 2],
                ['tax', 2],
                ['observations', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['provider', 6],
                ['date', 6],
                ['code', 6],
                ['tax', 6],
                ['observations', 6],)
        ]
        return g


class LineTicketForm(GenModelForm):
    class Meta:
        model = PurchasesLineTicket
        exclude = ['ticket']

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['line_albaran', 6],
                ['product', 6],
                ['quantity', 4],
                ['price', 4],
                ['tax', 4],
                ['description', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['ticket', 6],
                ['line_albaran', 6],
                ['product', 6],
                ['quantity', 6],
                ['price', 6],
                ['description', 6],
                ['tax', 6],)
        ]
        return g


class TicketRectificationForm(GenModelForm):
    class Meta:
        model = PurchasesTicketRectification
        exclude = []
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['date', 4],
                ['code', 4],
                ['tax', 4],
                ['observations', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['date', 6],
                ['code', 6],
                ['tax', 6],
                ['observations', 6],)
        ]
        return g


class LineTicketRectificationForm(GenModelForm):
    class Meta:
        model = PurchasesLineTicketRectification
        exclude = ['ticket_rectification', ]

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['line_ticket', 6],
                ['product', 6],
                ['quantity', 4],
                ['price', 4],
                ['tax', 4],
                ['description', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['ticket_rectification', 6],
                ['line_ticket', 6],
                ['product', 6],
                ['quantity', 6],
                ['price', 6],
                ['description', 6],
                ['tax', 6],)
        ]
        return g


class InvoiceForm(GenModelForm):
    class Meta:
        model = PurchasesInvoice
        exclude = ['lock', 'parent_pk']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['code', 4],
                ['provider', 4],
                ['date', 2],
                ['tax', 2],
                ['observations', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['provider', 6],
                ['date', 6],
                ['code', 6],
                ['tax', 6],
                ['observations', 6],)
        ]
        return g


class LineInvoiceForm(GenModelForm):
    class Meta:
        model = PurchasesLineInvoice
        exclude = ['invoice', ]

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['line_albaran', 6],
                ['product', 6],
                ['quantity', 4],
                ['price', 4],
                ['tax', 4],
                ['description', 6],
                ['feature_special_value', 6],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['invoice', 6],
                ['line_albaran', 6],
                ['product', 6],
                ['quantity', 6],
                ['price', 6],
                ['description', 6],
                ['feature_special_value', 6],
                ['tax', 6],)
        ]
        return g


class InvoiceRectificationForm(GenModelForm):
    class Meta:
        model = PurchasesInvoiceRectification
        exclude = ['lock', 'parent_pk']
        widgets = {
            'observations': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['code', 4],
                ['date', 4],
                ['tax', 4],
                ['observations', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['date', 6],
                ['code', 6],
                ['tax', 6],
                ['observations', 6],)
        ]
        return g


class LineInvoiceRectificationForm(GenModelForm):
    class Meta:
        model = PurchasesLineInvoiceRectification
        exclude = ['invoice_rectification', ]

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['line_invoice', 6],
                ['product', 6],
                ['quantity', 4],
                ['price', 4],
                ['tax', 4],
                ['description', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['invoice_rectification', 6],
                ['line_invoice', 6],
                ['product', 6],
                ['quantity', 6],
                ['price', 6],
                ['description', 6],
                ['tax', 6],)
        ]
        return g


# #################################
# formularios de documentos relacionados
class BudgetDocumentForm(GenModelForm):
    class Meta:
        model = PurchasesBudgetDocument
        exclude = ['budget', 'name_file', ]

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['code', 6],
                ['date', 6],
                ['doc_path', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['budget', 6],
                ['code', 6],
                ['date', 6],
                ['name_file', 6],)
        ]
        return g


class OrderDocumentForm(GenModelForm):
    class Meta:
        model = PurchasesOrderDocument
        exclude = ['order', 'name_file']

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['code', 6],
                ['date', 6],
                ['doc_path', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['order', 6],
                ['code', 6],
                ['date', 6],
                ['name_file', 6],)
        ]
        return g


class AlbaranDocumentForm(GenModelForm):
    class Meta:
        model = PurchasesAlbaranDocument
        exclude = ['albaran', 'name_file']

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['code', 6],
                ['date', 6],
                ['doc_path', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['albaran', 6],
                ['code', 6],
                ['date', 6],
                ['name_file', 6],)
        ]
        return g


class TicketDocumentForm(GenModelForm):
    class Meta:
        model = PurchasesTicketDocument
        exclude = ['ticket', 'name_file']

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['code', 6],
                ['date', 6],
                ['doc_path', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['ticket', 6],
                ['code', 6],
                ['date', 6],
                ['name_file', 6],)
        ]
        return g


class TicketRectificationDocumentForm(GenModelForm):
    class Meta:
        model = PurchasesTicketRectificationDocument
        exclude = ['ticket_rectification', 'name_file']

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['code', 6],
                ['date', 6],
                ['doc_path', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['ticket_rectification', 6],
                ['code', 6],
                ['date', 6],
                ['name_file', 6],)
        ]
        return g


class InvoiceDocumentForm(GenModelForm):
    class Meta:
        model = PurchasesInvoiceDocument
        exclude = ['invoice', 'name_file']

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['code', 6],
                ['date', 6],
                ['doc_path', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['invoice', 6],
                ['code', 6],
                ['date', 6],
                ['name_file', 6],)
        ]
        return g


class InvoiceRectificationDocumentForm(GenModelForm):
    class Meta:
        model = PurchasesInvoiceRectificationDocument
        exclude = ['invoice_rectification', 'name_file']

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['code', 6],
                ['date', 6],
                ['doc_path', 12],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['invoice_rectification', 6],
                ['code', 6],
                ['date', 6],
                ['name_file', 6],)
        ]
        return g
