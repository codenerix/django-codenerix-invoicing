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

from django.db.models import Q
from django.utils.translation import ugettext as _

from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail, GenDetailModal

from codenerix_invoicing.models_sales import ReasonModification
from codenerix_invoicing.models_sales import ReasonModificationLineOrder
from codenerix_invoicing.models_sales import ReasonModificationLineBasket, ReasonModificationLineAlbaran, ReasonModificationLineTicket, ReasonModificationLineTicketRectification, ReasonModificationLineInvoice, ReasonModificationLineInvoiceRectification
from codenerix_invoicing.forms_reason import ReasonModificationForm
from codenerix_invoicing.forms_reason import ReasonModificationLineBasketForm, ReasonModificationLineOrderForm, ReasonModificationLineAlbaranForm, ReasonModificationLineTicketForm, ReasonModificationLineTicketRectificationForm, ReasonModificationLineInvoiceForm, ReasonModificationLineInvoiceRectificationForm


# ###########################################
# ReasonModification
class ReasonModificationList(GenList):
    model = ReasonModification
    extra_context = {'menu': ['sales', 'ReasonModification'], 'bread': [_('Sales'), _('ReasonModification')]}


class ReasonModificationCreate(GenCreate):
    model = ReasonModification
    form_class = ReasonModificationForm


class ReasonModificationCreateModal(GenCreateModal, ReasonModificationCreate):
    pass


class ReasonModificationUpdate(GenUpdate):
    model = ReasonModification
    form_class = ReasonModificationForm


class ReasonModificationUpdateModal(GenUpdateModal, ReasonModificationUpdate):
    pass


class ReasonModificationDelete(GenDelete):
    model = ReasonModification


class ReasonModificationSubList(GenList):
    model = ReasonModification
    extra_context = {'menu': ['sales', 'ReasonModification'], 'bread': [_('Sales'), _('ReasonModification')]}


class ReasonModificationDetails(GenDetail):
    model = ReasonModification
    groups = ReasonModificationForm.__groups_details__()


class ReasonModificationDetailModal(GenDetailModal, ReasonModificationDetails):
    pass


# ###########################################
class ReasonModificationLineList(GenList):
    linkadd = False
    show_details = True


class ReasonModificationLineDetail(GenDetailModal, GenDetail):
    linkedit = False
    linkdelete = False


# ###########################################
# ReasonModificationLineBasket
class ReasonModificationLineBasketSubList(ReasonModificationLineList):
    model = ReasonModificationLineBasket

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(basket__pk=pk)
        return limit


class ReasonModificationLineBasketDetailModal(ReasonModificationLineDetail):
    model = ReasonModificationLineBasket
    groups = ReasonModificationLineBasketForm.__groups_details__()


# ###########################################
# ReasonModificationLineOrder
class ReasonModificationLineOrderSubList(ReasonModificationLineList):
    model = ReasonModificationLineOrder

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(order__pk=pk)
        return limit


class ReasonModificationLineOrderDetailModal(ReasonModificationLineDetail):
    model = ReasonModificationLineOrder
    groups = ReasonModificationLineOrderForm.__groups_details__()


# ###########################################
# ReasonModificationLineAlbaran
class ReasonModificationLineAlbaranSubList(ReasonModificationLineList):
    model = ReasonModificationLineAlbaran

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(albaran__pk=pk)
        return limit


class ReasonModificationLineAlbaranDetailModal(ReasonModificationLineDetail):
    model = ReasonModificationLineAlbaran
    groups = ReasonModificationLineAlbaranForm.__groups_details__()


# ###########################################
# ReasonModificationLineTicket
class ReasonModificationLineTicketSubList(ReasonModificationLineList):
    model = ReasonModificationLineTicket

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(ticket__pk=pk)
        return limit


class ReasonModificationLineTicketDetailModal(ReasonModificationLineDetail):
    model = ReasonModificationLineTicket
    groups = ReasonModificationLineTicketForm.__groups_details__()


# ###########################################
# ReasonModificationLineTicketRectification
class ReasonModificationLineTicketRectificationSubList(ReasonModificationLineList):
    model = ReasonModificationLineTicketRectification

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(ticket_rectification__pk=pk)
        return limit


class ReasonModificationLineTicketRectificationDetailModal(ReasonModificationLineDetail):
    model = ReasonModificationLineTicketRectification
    groups = ReasonModificationLineTicketRectificationForm.__groups_details__()


# ###########################################
# ReasonModificationLineInvoice
class ReasonModificationLineInvoiceSubList(ReasonModificationLineList):
    model = ReasonModificationLineInvoice

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(invoice__pk=pk)
        return limit


class ReasonModificationLineInvoiceDetailModal(ReasonModificationLineDetail):
    model = ReasonModificationLineInvoice
    groups = ReasonModificationLineInvoiceForm.__groups_details__()


# ###########################################
# ReasonModificationLineInvoiceRectification
class ReasonModificationLineInvoiceRectificationSubList(ReasonModificationLineList):
    model = ReasonModificationLineInvoiceRectification

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(invoice_rectification__pk=pk)
        return limit


class ReasonModificationLineInvoiceRectificationDetailModal(ReasonModificationLineDetail):
    model = ReasonModificationLineInvoiceRectification
    groups = ReasonModificationLineInvoiceRectificationForm.__groups_details__()
