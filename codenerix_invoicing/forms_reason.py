# -*- coding: utf-8 -*-
#
# django-codenerix-invoicing
#
# Copyright 2018 Centrologic Computational Logistic Center S.L.
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
from codenerix_invoicing.models_sales import ReasonModification
from codenerix_invoicing.models_sales import ReasonModificationLineOrder
from codenerix_invoicing.models_sales import ReasonModificationLineBasket, ReasonModificationLineAlbaran, ReasonModificationLineTicket, ReasonModificationLineTicketRectification, ReasonModificationLineInvoice, ReasonModificationLineInvoiceRectification


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