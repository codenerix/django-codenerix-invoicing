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

from django.conf.urls import url
from codenerix_invoicing.views_purchases import ProviderList, BudgetList, LineBudgetList, \
    OrderList, LineOrderList, AlbaranList, LineAlbaranList, \
    TicketList, LineTicketList, TicketRectificationList, \
    LineTicketRectificationList, InvoiceList, LineInvoiceList, \
    InvoiceRectificationList, LineInvoiceRectificationList, \
    ProviderCreate, \
    BudgetCreate, OrderCreate, AlbaranCreate, TicketCreate, \
    TicketRectificationCreate, InvoiceCreate, \
    InvoiceRectificationCreate, \
    ProviderCreateModal, \
    BudgetCreateModal, LineBudgetCreateModal, OrderCreateModal, \
    LineOrderCreateModal, AlbaranCreateModal, LineAlbaranCreateModal, \
    TicketCreateModal, LineTicketCreateModal, TicketRectificationCreateModal, \
    LineTicketRectificationCreateModal, InvoiceCreateModal, LineInvoiceCreateModal, InvoiceRectificationCreateModal, LineInvoiceRectificationCreateModal, \
    ProviderUpdate, ProviderDetails, \
    BudgetUpdate, OrderUpdate, AlbaranUpdate, \
    TicketUpdate, TicketRectificationUpdate, \
    InvoiceUpdate, \
    InvoiceRectificationUpdate, ProviderUpdateModal, \
    BudgetUpdateModal, LineBudgetUpdateModal, OrderUpdateModal, \
    LineOrderUpdateModal, AlbaranUpdateModal, LineAlbaranUpdateModal, \
    TicketUpdateModal, LineTicketUpdateModal, TicketRectificationUpdateModal,\
    LineTicketRectificationUpdateModal, InvoiceUpdateModal, LineInvoiceUpdateModal, \
    InvoiceRectificationUpdateModal, LineInvoiceRectificationUpdateModal, \
    ProviderDelete, \
    BudgetDelete, LineBudgetDelete, OrderDelete, LineOrderDelete, \
    AlbaranDelete, LineAlbaranDelete, TicketDelete, LineTicketDelete, \
    TicketRectificationDelete, LineTicketRectificationDelete, InvoiceDelete, \
    LineInvoiceDelete, InvoiceRectificationDelete, LineInvoiceRectificationDelete, \
    BudgetDocumentList, OrderDocumentList, AlbaranDocumentList, \
    TicketDocumentList, TicketRectificationDocumentList, InvoiceDocumentList, \
    InvoiceRectificationDocumentList, BudgetDocumentCreateModal, OrderDocumentCreateModal, AlbaranDocumentCreateModal, \
    TicketDocumentCreateModal, TicketRectificationDocumentCreateModal, InvoiceDocumentCreateModal, InvoiceRectificationDocumentCreateModal, \
    BudgetDocumentUpdateModal, OrderDocumentUpdateModal, AlbaranDocumentUpdateModal, \
    TicketDocumentUpdateModal, TicketRectificationDocumentUpdateModal, InvoiceDocumentUpdateModal, InvoiceRectificationDocumentUpdateModal, \
    BudgetDocumentDelete, OrderDocumentDelete, AlbaranDocumentDelete, \
    TicketDocumentDelete, TicketRectificationDocumentDelete, InvoiceDocumentDelete, InvoiceRectificationDocumentDelete, \
    BudgetDocumentSubList, OrderDocumentSubList, AlbaranDocumentSubList, \
    TicketDocumentSubList, TicketRectificationDocumentSubList, InvoiceDocumentSubList, InvoiceRectificationDocumentSubList, \
    BudgetDocumentDetails, OrderDocumentDetails, AlbaranDocumentDetails, \
    TicketDocumentDetails, TicketRectificationDocumentDetails, InvoiceDocumentDetails, \
    InvoiceRectificationDocumentDetails, \
    BudgetDocumentDetailsModal, OrderDocumentDetailsModal, AlbaranDocumentDetailsModal, \
    TicketDocumentDetailsModal, TicketRectificationDocumentDetailsModal, InvoiceDocumentDetailsModal, InvoiceRectificationDocumentDetailsModal, \
    BudgetDetails, LineBudgetSubList, LineBudgetDetailsModal, \
    OrderDetails, LineOrderSubList, LineOrderDetailsModal, \
    AlbaranDetails, LineAlbaranSubList, LineAlbaranDetailsModal, \
    InvoiceDetails, LineInvoiceSubList, LineInvoiceDetailsModal, \
    InvoiceRectificationDetails, LineInvoiceRectificationSubList, LineInvoiceRectificationDetailsModal, \
    TicketDetails, LineTicketSubList, LineTicketDetailsModal, \
    TicketRectificationDetails, LineTicketRectificationSubList, LineTicketRectificationDetailsModal, \
    BudgetDoOrder, OrderCreateFromBudget, \
    LineBudgetSubListForm, OrderDetailsModal, \
    BudgetPrint, OrderPrint, AlbaranPrint, TicketPrint, TicketRectificationPrint, InvoicePrint, InvoiceRectificationPrint


urlpatterns = [
    url(r'^providers$', ProviderList.as_view(), name='CDNX_invoicing_providers_list'),
    url(r'^providers/add$', ProviderCreate.as_view(), name='CDNX_invoicing_providers_add'),
    url(r'^providers/addmodal$', ProviderCreateModal.as_view(), name='CDNX_invoicing_providers_addmodal'),
    url(r'^providers/(?P<pk>\w+)$', ProviderDetails.as_view(), name='CDNX_invoicing_providers_details'),
    url(r'^providers/(?P<pk>\w+)/edit$', ProviderUpdate.as_view(), name='CDNX_invoicing_providers_edit'),
    url(r'^providers/(?P<pk>\w+)/editmodal$', ProviderUpdateModal.as_view(), name='CDNX_invoicing_providers_editmodal'),
    url(r'^providers/(?P<pk>\w+)/delete$', ProviderDelete.as_view(), name='CDNX_invoicing_providers_delete'),

    url(r'^budgets$', BudgetList.as_view(), name='CDNX_invoicing_budgetpurchasess_list'),
    url(r'^budgets/add$', BudgetCreate.as_view(), name='CDNX_invoicing_budgetpurchasess_add'),
    url(r'^budgets/addmodal$', BudgetCreateModal.as_view(), name='CDNX_invoicing_budgetpurchasess_addmodal'),
    url(r'^budgets/(?P<pk>\w+)$', BudgetDetails.as_view(), name='CDNX_invoicing_budgetpurchasess_details'),
    url(r'^budgets/(?P<pk>\w+)/edit$', BudgetUpdate.as_view(), name='CDNX_invoicing_budgetpurchasess_edit'),
    url(r'^budgets/(?P<pk>\w+)/editmodal$', BudgetUpdateModal.as_view(), name='CDNX_invoicing_budgetpurchasess_editmodal'),
    url(r'^budgets/(?P<pk>\w+)/delete$', BudgetDelete.as_view(), name='CDNX_invoicing_budgetpurchasess_delete'),
    url(r'^budgets/(?P<pk>\w+)/order$', BudgetDoOrder.as_view(), name='CDNX_invoicing_budgetsaless_order'),
    url(r'^budgets/(?P<cpk>\w+)/doorder/(?P<pk>\w+)$', OrderCreateFromBudget.as_view(), name='CDNX_invoicing_budgetsaless3_order'),
    url(r'^budgets/(?P<pk>\w+)/print$', BudgetPrint.as_view(), name='CDNX_invoicing_budgetpurchasess_print'),

    url(r'^purchasesbudgets/addmodal$', BudgetCreateModal.as_view(), name='CDNX_invoicing_budgetpurchasess_addmodal_l'),

    url(r'^linebudgets$', LineBudgetList.as_view(), name='CDNX_invoicing_linebudgetpurchasess_list'),
    url(r'^linebudgets/(?P<pk>\w+)/delete$', LineBudgetDelete.as_view(), name='CDNX_invoicing_linebudgetpurchasess_delete'),
    url(r'^linebudgets/(?P<pk>\w+)/sublist$', LineBudgetSubList.as_view(), name='CDNX_invoicing_linebudgetpurchasess_sublist'),
    url(r'^linebudgets/(?P<pk>\w+)/sublistform$', LineBudgetSubListForm.as_view(), name='CDNX_invoicing_linebudgetpurchasess_sublist_form'),
    url(r'^linebudgets/(?P<pk>\w+)/sublist/add$', LineBudgetCreateModal.as_view(), name='CDNX_invoicing_linebudgetpurchasess_sublist_add'),
    url(r'^linebudgets/(?P<pk>\w+)/sublist/addmodal$', LineBudgetCreateModal.as_view(), name='CDNX_invoicing_linebudgetpurchasess_sublist_addmodal'),
    url(r'^linebudgets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineBudgetDetailsModal.as_view(), name='CDNX_invoicing_linebudgetpurchasess_sublist_details'),
    url(r'^linebudgets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', LineBudgetUpdateModal.as_view(), name='CDNX_invoicing_linebudgetpurchasess_sublist_edit'),
    url(r'^linebudgets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineBudgetUpdateModal.as_view(), name='CDNX_invoicing_linebudgetpurchasess_sublist_editmodal'),
    url(r'^linebudgets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineBudgetDelete.as_view(), name='CDNX_invoicing_linebudgetpurchasess_sublist_delete'),

    url(r'^orders$', OrderList.as_view(), name='CDNX_invoicing_orderpurchasess_list'),
    url(r'^orders/add$', OrderCreate.as_view(), name='CDNX_invoicing_orderpurchasess_add'),
    url(r'^orders/addmodal$', OrderCreateModal.as_view(), name='CDNX_invoicing_orderpurchasess_addmodal'),
    url(r'^orders/(?P<pk>\w+)$', OrderDetails.as_view(), name='CDNX_invoicing_orderpurchasess_details'),
    url(r'^orders#/(?P<pk>\w+)$', OrderDetails.as_view(), name='CDNX_invoicing_orderpurchasess_details_js'),
    url(r'^orders/(?P<pk>\w+)/modal$', OrderDetailsModal.as_view(), name='CDNX_invoicing_orderpurchasess_detailsmodal'),
    url(r'^orders/(?P<pk>\w+)/edit$', OrderUpdate.as_view(), name='CDNX_invoicing_orderpurchasess_edit'),
    url(r'^orders/(?P<pk>\w+)/editmodal$', OrderUpdateModal.as_view(), name='CDNX_invoicing_orderpurchasess_editmodal'),
    url(r'^orders/(?P<pk>\w+)/delete$', OrderDelete.as_view(), name='CDNX_invoicing_orderpurchasess_delete'),
    url(r'^orders/(?P<pk>\w+)/print$', OrderPrint.as_view(), name='CDNX_invoicing_orderpurchasess_print'),

    url(r'^lineorders$', LineOrderList.as_view(), name='CDNX_invoicing_lineorderpurchasess_list'),
    url(r'^lineorders/(?P<pk>\w+)/delete$', LineOrderDelete.as_view(), name='CDNX_invoicing_lineorderpurchasess_delete'),
    url(r'^lineorders/(?P<pk>\w+)/sublist$', LineOrderSubList.as_view(), name='CDNX_invoicing_lineorderpurchasess_sublist'),
    url(r'^lineorders/(?P<pk>\w+)/sublist/add$', LineOrderCreateModal.as_view(), name='CDNX_invoicing_lineorderpurchasess_sublist_add'),
    url(r'^lineorders/(?P<pk>\w+)/sublist/addmodal$', LineOrderCreateModal.as_view(), name='CDNX_invoicing_lineorderpurchasess_sublist_addmodal'),
    url(r'^lineorders/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineOrderDetailsModal.as_view(), name='CDNX_invoicing_lineorderpurchasess_sublist_details'),
    url(r'^lineorders/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', LineOrderUpdateModal.as_view(), name='CDNX_invoicing_lineorderpurchasess_sublist_edit'),
    url(r'^lineorders/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineOrderUpdateModal.as_view(), name='CDNX_invoicing_lineorderpurchasess_sublist_editmodal'),
    url(r'^lineorders/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineOrderDelete.as_view(), name='CDNX_invoicing_lineorderpurchasess_sublist_delete'),

    url(r'^albarans$', AlbaranList.as_view(), name='CDNX_invoicing_albaranpurchasess_list'),
    url(r'^albarans/add$', AlbaranCreate.as_view(), name='CDNX_invoicing_albaranpurchasess_add'),
    url(r'^albarans/addmodal$', AlbaranCreateModal.as_view(), name='CDNX_invoicing_albaranpurchasess_addmodal'),
    url(r'^albarans/(?P<pk>\w+)$', AlbaranDetails.as_view(), name='CDNX_invoicing_albaranpurchasess_details'),
    url(r'^albarans/(?P<pk>\w+)/edit$', AlbaranUpdate.as_view(), name='CDNX_invoicing_albaranpurchasess_edit'),
    url(r'^albarans/(?P<pk>\w+)/editmodal$', AlbaranUpdateModal.as_view(), name='CDNX_invoicing_albaranpurchasess_editmodal'),
    url(r'^albarans/(?P<pk>\w+)/delete$', AlbaranDelete.as_view(), name='CDNX_invoicing_albaranpurchasess_delete'),
    url(r'^albarans/(?P<pk>\w+)/print$', AlbaranPrint.as_view(), name='CDNX_invoicing_albaranpurchasess_print'),

    url(r'^linealbarans$', LineAlbaranList.as_view(), name='CDNX_invoicing_linealbaranpurchasess_list'),
    url(r'^linealbarans/(?P<pk>\w+)/delete$', LineAlbaranDelete.as_view(), name='CDNX_invoicing_linealbaranpurchasess_delete'),
    url(r'^linealbarans/(?P<pk>\w+)/sublist$', LineAlbaranSubList.as_view(), name='CDNX_invoicing_linealbaranpurchasess_sublist'),
    url(r'^linealbarans/(?P<pk>\w+)/sublist/add$', LineAlbaranCreateModal.as_view(), name='CDNX_invoicing_linealbaranpurchasess_sublist_add'),
    url(r'^linealbarans/(?P<pk>\w+)/sublist/addmodal$', LineAlbaranCreateModal.as_view(), name='CDNX_invoicing_linealbaranpurchasess_sublist_addmodal'),
    url(r'^linealbarans/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineAlbaranDetailsModal.as_view(), name='CDNX_invoicing_linealbaranpurchasess_sublist_details'),
    url(r'^linealbarans/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', LineAlbaranUpdateModal.as_view(), name='CDNX_invoicing_linealbaranpurchasess_sublist_edit'),
    url(r'^linealbarans/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineAlbaranUpdateModal.as_view(), name='CDNX_invoicing_linealbaranpurchasess_sublist_editmodal'),
    url(r'^linealbarans/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineAlbaranDelete.as_view(), name='CDNX_invoicing_linealbaranpurchasess_sublist_delete'),

    url(r'^tickets$', TicketList.as_view(), name='CDNX_invoicing_ticketpurchasess_list'),
    url(r'^tickets/add$', TicketCreate.as_view(), name='CDNX_invoicing_ticketpurchasess_add'),
    url(r'^tickets/addmodal$', TicketCreateModal.as_view(), name='CDNX_invoicing_ticketpurchasess_addmodal'),
    url(r'^tickets/(?P<pk>\w+)$', TicketDetails.as_view(), name='CDNX_invoicing_ticketpurchasess_details'),
    url(r'^tickets/(?P<pk>\w+)/edit$', TicketUpdate.as_view(), name='CDNX_invoicing_ticketpurchasess_edit'),
    url(r'^tickets/(?P<pk>\w+)/editmodal$', TicketUpdateModal.as_view(), name='CDNX_invoicing_ticketpurchasess_editmodal'),
    url(r'^tickets/(?P<pk>\w+)/delete$', TicketDelete.as_view(), name='CDNX_invoicing_ticketpurchasess_delete'),
    url(r'^tickets/(?P<pk>\w+)/print$', TicketPrint.as_view(), name='CDNX_invoicing_ticketpurchasess_print'),

    url(r'^linetickets$', LineTicketList.as_view(), name='CDNX_invoicing_lineticketpurchasess_list'),
    url(r'^linetickets/(?P<pk>\w+)/delete$', LineTicketDelete.as_view(), name='CDNX_invoicing_lineticketpurchasess_delete'),
    url(r'^linetickets/(?P<pk>\w+)/sublist$', LineTicketSubList.as_view(), name='CDNX_invoicing_lineticketpurchasess_sublist'),
    url(r'^linetickets/(?P<pk>\w+)/sublist/add$', LineTicketCreateModal.as_view(), name='CDNX_invoicing_lineticketpurchasess_sublist_add'),
    url(r'^linetickets/(?P<pk>\w+)/sublist/addmodal$', LineTicketCreateModal.as_view(), name='CDNX_invoicing_lineticketpurchasess_sublist_addmodal'),
    url(r'^linetickets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineTicketDetailsModal.as_view(), name='CDNX_invoicing_lineticketpurchasess_sublist_details'),
    url(r'^linetickets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', LineTicketUpdateModal.as_view(), name='CDNX_invoicing_lineticketpurchasess_sublist_edit'),
    url(r'^linetickets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineTicketUpdateModal.as_view(), name='CDNX_invoicing_lineticketpurchasess_sublist_editmodal'),
    url(r'^linetickets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineTicketDelete.as_view(), name='CDNX_invoicing_lineticketpurchasess_sublist_delete'),

    url(r'^ticketrectifications$', TicketRectificationList.as_view(), name='CDNX_invoicing_ticketrectificationpurchasess_list'),
    url(r'^ticketrectifications/add$', TicketRectificationCreate.as_view(), name='CDNX_invoicing_ticketrectificationpurchasess_add'),
    url(r'^ticketrectifications/addmodal$', TicketRectificationCreateModal.as_view(), name='CDNX_invoicing_ticketrectificationpurchasess_addmodal'),
    url(r'^ticketrectifications/(?P<pk>\w+)$', TicketRectificationDetails.as_view(), name='CDNX_invoicing_ticketrectificationpurchasess_details'),
    url(r'^ticketrectifications/(?P<pk>\w+)/edit$', TicketRectificationUpdate.as_view(), name='CDNX_invoicing_ticketrectificationpurchasess_edit'),
    url(r'^ticketrectifications/(?P<pk>\w+)/editmodal$', TicketRectificationUpdateModal.as_view(), name='CDNX_invoicing_ticketrectificationpurchasess_editmodal'),
    url(r'^ticketrectifications/(?P<pk>\w+)/delete$', TicketRectificationDelete.as_view(), name='CDNX_invoicing_ticketrectificationpurchasess_delete'),
    url(r'^ticketrectifications/(?P<pk>\w+)/print$', TicketRectificationPrint.as_view(), name='CDNX_invoicing_ticketrectificationpurchasess_print'),

    url(r'^lineticketrectifications$', LineTicketRectificationList.as_view(), name='CDNX_invoicing_lineticketrectificationpurchasess_list'),
    url(r'^lineticketrectifications/(?P<pk>\w+)/delete$', LineTicketRectificationDelete.as_view(), name='CDNX_invoicing_lineticketrectificationpurchasess_delete'),
    url(r'^lineticketrectifications/(?P<pk>\w+)/sublist$', LineTicketRectificationSubList.as_view(), name='CDNX_invoicing_lineticketrectificationpurchasess_sublist'),
    url(r'^lineticketrectifications/(?P<pk>\w+)/sublist/add$', LineTicketRectificationCreateModal.as_view(), name='CDNX_invoicing_lineticketrectificationpurchasess_sublist_add'),
    url(r'^lineticketrectifications/(?P<pk>\w+)/sublist/addmodal$', LineTicketRectificationCreateModal.as_view(), name='CDNX_invoicing_lineticketrectificationpurchasess_sublist_addmodal'),
    url(r'^lineticketrectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineTicketRectificationDetailsModal.as_view(), name='CDNX_invoicing_lineticketrectificationpurchasess_sublist_details'),
    url(r'^lineticketrectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', LineTicketRectificationUpdateModal.as_view(), name='CDNX_invoicing_lineticketrectificationpurchasess_sublist_edit'),
    url(r'^lineticketrectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineTicketRectificationUpdateModal.as_view(), name='CDNX_invoicing_lineticketrectificationpurchasess_sublist_editmodal'),
    url(r'^lineticketrectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineTicketRectificationDelete.as_view(), name='CDNX_invoicing_lineticketrectificationpurchasess_sublist_delete'),

    url(r'^invoices$', InvoiceList.as_view(), name='CDNX_invoicing_invoicepurchasess_list'),
    url(r'^invoices/add$', InvoiceCreate.as_view(), name='CDNX_invoicing_invoicepurchasess_add'),
    url(r'^invoices/addmodal$', InvoiceCreateModal.as_view(), name='CDNX_invoicing_invoicepurchasess_addmodal'),
    url(r'^invoices/(?P<pk>\w+)$', InvoiceDetails.as_view(), name='CDNX_invoicing_invoicepurchasess_details'),
    url(r'^invoices/(?P<pk>\w+)/edit$', InvoiceUpdate.as_view(), name='CDNX_invoicing_invoicepurchasess_edit'),
    url(r'^invoices/(?P<pk>\w+)/editmodal$', InvoiceUpdateModal.as_view(), name='CDNX_invoicing_invoicepurchasess_editmodal'),
    url(r'^invoices/(?P<pk>\w+)/delete$', InvoiceDelete.as_view(), name='CDNX_invoicing_invoicepurchasess_delete'),
    url(r'^invoices/(?P<pk>\w+)/print$', InvoicePrint.as_view(), name='CDNX_invoicing_invoicepurchasess_print'),

    url(r'^lineinvoices$', LineInvoiceList.as_view(), name='CDNX_invoicing_lineinvoicepurchasess_list'),
    url(r'^lineinvoices/(?P<pk>\w+)/delete$', LineInvoiceDelete.as_view(), name='CDNX_invoicing_lineinvoicepurchasess_delete'),
    url(r'^lineinvoices/(?P<pk>\w+)/sublist$', LineInvoiceSubList.as_view(), name='CDNX_invoicing_lineinvoicepurchasess_sublist'),
    url(r'^lineinvoices/(?P<pk>\w+)/sublist/add$', LineInvoiceCreateModal.as_view(), name='CDNX_invoicing_lineinvoicepurchasess_sublist_add'),
    url(r'^lineinvoices/(?P<pk>\w+)/sublist/addmodal$', LineInvoiceCreateModal.as_view(), name='CDNX_invoicing_lineinvoicepurchasess_sublist_addmodal'),
    url(r'^lineinvoices/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineInvoiceDetailsModal.as_view(), name='CDNX_invoicing_lineinvoicepurchasess_sublist_details'),
    url(r'^lineinvoices/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', LineInvoiceUpdateModal.as_view(), name='CDNX_invoicing_lineinvoicepurchasess_sublist_edit'),
    url(r'^lineinvoices/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineInvoiceUpdateModal.as_view(), name='CDNX_invoicing_lineinvoicepurchasess_sublist_editmodal'),
    url(r'^lineinvoices/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineInvoiceDelete.as_view(), name='CDNX_invoicing_lineinvoicepurchasess_sublist_delete'),

    url(r'^invoicerectifications$', InvoiceRectificationList.as_view(), name='CDNX_invoicing_invoicerectificationpurchasess_list'),
    url(r'^invoicerectifications/add$', InvoiceRectificationCreate.as_view(), name='CDNX_invoicing_invoicerectificationpurchasess_add'),
    url(r'^invoicerectifications/addmodal$', InvoiceRectificationCreateModal.as_view(), name='CDNX_invoicing_invoicerectificationpurchasess_addmodal'),
    url(r'^invoicerectifications/(?P<pk>\w+)$', InvoiceRectificationDetails.as_view(), name='CDNX_invoicing_invoicerectificationpurchasess_details'),
    url(r'^invoicerectifications/(?P<pk>\w+)/edit$', InvoiceRectificationUpdate.as_view(), name='CDNX_invoicing_invoicerectificationpurchasess_edit'),
    url(r'^invoicerectifications/(?P<pk>\w+)/editmodal$', InvoiceRectificationUpdateModal.as_view(), name='CDNX_invoicing_invoicerectificationpurchasess_editmodal'),
    url(r'^invoicerectifications/(?P<pk>\w+)/delete$', InvoiceRectificationDelete.as_view(), name='CDNX_invoicing_invoicerectificationpurchasess_delete'),
    url(r'^invoicerectifications/(?P<pk>\w+)/print$', InvoiceRectificationPrint.as_view(), name='CDNX_invoicing_invoicerectificationpurchasess_print'),

    url(r'^lineinvoicerectifications$', LineInvoiceRectificationList.as_view(), name='CDNX_invoicing_lineinvoicerectificationpurchasess_list'),
    url(r'^lineinvoicerectifications/(?P<pk>\w+)/editmodal$', LineInvoiceRectificationUpdateModal.as_view(), name='CDNX_invoicing_lineinvoicerectificationpurchasess_editmodal'),
    url(r'^lineinvoicerectifications/(?P<pk>\w+)/delete$', LineInvoiceRectificationDelete.as_view(), name='CDNX_invoicing_lineinvoicerectificationpurchasess_delete'),
    url(r'^lineinvoicerectifications/(?P<pk>\w+)/sublist$', LineInvoiceRectificationSubList.as_view(), name='CDNX_invoicing_lineinvoicerectificationpurchasess_sublist'),
    url(r'^lineinvoicerectifications/(?P<pk>\w+)/sublist/add$', LineInvoiceRectificationCreateModal.as_view(), name='CDNX_invoicing_lineinvoicerectificationpurchasess_sublist_add'),
    url(r'^lineinvoicerectifications/(?P<pk>\w+)/sublist/addmodal$', LineInvoiceRectificationCreateModal.as_view(), name='CDNX_invoicing_lineinvoicerectificationpurchasess_sublist_addmodal'),
    url(r'^lineinvoicerectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineInvoiceRectificationDetailsModal.as_view(), name='CDNX_invoicing_lineinvoicerectificationpurchasess_sublist_details'),
    url(r'^lineinvoicerectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', LineInvoiceRectificationUpdateModal.as_view(), name='CDNX_invoicing_lineinvoicerectificationpurchasess_sublist_edit'),
    url(r'^lineinvoicerectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineInvoiceRectificationUpdateModal.as_view(), name='CDNX_invoicing_lineinvoicerectificationpurchasess_sublist_editmodal'),
    url(r'^lineinvoicerectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineInvoiceRectificationDelete.as_view(), name='CDNX_invoicing_lineinvoicerectificationpurchasess_sublist_delete'),

    url(r'^budgetdocuments$', BudgetDocumentList.as_view(), name='CDNX_invoicing_budgetpurchasesdocuments_list'),
    url(r'^budgetdocuments/(?P<pk>\w+)$', BudgetDocumentDetails.as_view(), name='CDNX_invoicing_budgetpurchasesdocuments_details'),
    url(r'^budgetdocuments/(?P<pk>\w+)/delete$', BudgetDocumentDelete.as_view(), name='CDNX_invoicing_budgetpurchasesdocuments_delete'),
    url(r'^budgetdocuments/(?P<pk>\w+)/sublist$', BudgetDocumentSubList.as_view(), name='CDNX_invoicing_budgetpurchasesdocuments_sublist'),
    url(r'^budgetdocuments/(?P<pk>\w+)/sublist/add$', BudgetDocumentCreateModal.as_view(), name='CDNX_invoicing_budgetpurchasesdocuments_sublist_add'),
    url(r'^budgetdocuments/(?P<pk>\w+)/sublist/addmodal$', BudgetDocumentCreateModal.as_view(), name='CDNX_invoicing_budgetpurchasesdocuments_sublist_addmodal'),
    url(r'^budgetdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', BudgetDocumentDetailsModal.as_view(), name='CDNX_invoicing_budgetpurchasesdocuments_sublist_details'),
    url(r'^budgetdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', BudgetDocumentUpdateModal.as_view(), name='CDNX_invoicing_budgetpurchasesdocuments_sublist_edit'),
    url(r'^budgetdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edimodalt$', BudgetDocumentUpdateModal.as_view(), name='CDNX_invoicing_budgetpurchasesdocuments_sublist_editmodal'),
    url(r'^budgetdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', BudgetDocumentDelete.as_view(), name='CDNX_invoicing_budgetpurchasesdocuments_sublist_delete'),

    url(r'^orderdocuments$', OrderDocumentList.as_view(), name='CDNX_invoicing_orderpurchasesdocuments_list'),
    url(r'^orderdocuments/(?P<pk>\w+)$', OrderDocumentDetails.as_view(), name='CDNX_invoicing_orderpurchasesdocuments_details'),
    url(r'^orderdocuments/(?P<pk>\w+)/delete$', OrderDocumentDelete.as_view(), name='CDNX_invoicing_orderpurchasesdocuments_delete'),
    url(r'^orderdocuments/(?P<pk>\w+)/sublist$', OrderDocumentSubList.as_view(), name='CDNX_invoicing_orderpurchasesdocuments_sublist'),
    url(r'^orderdocuments/(?P<pk>\w+)/sublist/add$', OrderDocumentCreateModal.as_view(), name='CDNX_invoicing_orderpurchasesdocuments_sublist_add'),
    url(r'^orderdocuments/(?P<pk>\w+)/sublist/addmodal$', OrderDocumentCreateModal.as_view(), name='CDNX_invoicing_orderpurchasesdocuments_sublist_addmodal'),
    url(r'^orderdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', OrderDocumentDetailsModal.as_view(), name='CDNX_invoicing_orderpurchasesdocuments_sublist_details'),
    url(r'^orderdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', OrderDocumentUpdateModal.as_view(), name='CDNX_invoicing_orderpurchasesdocuments_sublist_edit'),
    url(r'^orderdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', OrderDocumentUpdateModal.as_view(), name='CDNX_invoicing_orderpurchasesdocuments_sublist_editmodal'),
    url(r'^orderdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', OrderDocumentDelete.as_view(), name='CDNX_invoicing_orderpurchasesdocuments_sublist_delete'),

    url(r'^albarandocuments$', AlbaranDocumentList.as_view(), name='CDNX_invoicing_albaranpurchasesdocuments_list'),
    url(r'^albarandocuments/(?P<pk>\w+)$', AlbaranDocumentDetails.as_view(), name='CDNX_invoicing_albaranpurchasesdocuments_details'),
    url(r'^albarandocuments/(?P<pk>\w+)/delete$', AlbaranDocumentDelete.as_view(), name='CDNX_invoicing_albaranpurchasesdocuments_delete'),
    url(r'^albarandocuments/(?P<pk>\w+)/sublist$', AlbaranDocumentSubList.as_view(), name='CDNX_invoicing_albaranpurchasesdocuments_sublist'),
    url(r'^albarandocuments/(?P<pk>\w+)/sublist/add$', AlbaranDocumentCreateModal.as_view(), name='CDNX_invoicing_albaranpurchasesdocuments_sublist_add'),
    url(r'^albarandocuments/(?P<pk>\w+)/sublist/addmodal$', AlbaranDocumentCreateModal.as_view(), name='CDNX_invoicing_albaranpurchasesdocuments_sublist_addmodal'),
    url(r'^albarandocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', AlbaranDocumentDetailsModal.as_view(), name='CDNX_invoicing_albaranpurchasesdocuments_sublist_details'),
    url(r'^albarandocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', AlbaranDocumentUpdateModal.as_view(), name='CDNX_invoicing_albaranpurchasesdocuments_sublist_edit'),
    url(r'^albarandocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', AlbaranDocumentUpdateModal.as_view(), name='CDNX_invoicing_albaranpurchasesdocuments_sublist_editmodal'),
    url(r'^albarandocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', AlbaranDocumentDelete.as_view(), name='CDNX_invoicing_albaranpurchasesdocuments_sublist_delete'),

    url(r'^ticketdocuments$', TicketDocumentList.as_view(), name='CDNX_invoicing_ticketpurchasesdocuments_list'),
    url(r'^ticketdocuments/(?P<pk>\w+)$', TicketDocumentDetails.as_view(), name='CDNX_invoicing_ticketpurchasesdocuments_details'),
    url(r'^ticketdocuments/(?P<pk>\w+)/delete$', TicketDocumentDelete.as_view(), name='CDNX_invoicing_ticketpurchasesdocuments_delete'),
    url(r'^ticketdocuments/(?P<pk>\w+)/sublist$', TicketDocumentSubList.as_view(), name='CDNX_invoicing_ticketpurchasesdocuments_sublist'),
    url(r'^ticketdocuments/(?P<pk>\w+)/sublist/add$', TicketDocumentCreateModal.as_view(), name='CDNX_invoicing_ticketpurchasesdocuments_sublist_add'),
    url(r'^ticketdocuments/(?P<pk>\w+)/sublist/addmodal$', TicketDocumentCreateModal.as_view(), name='CDNX_invoicing_ticketpurchasesdocuments_sublist_addmodal'),
    url(r'^ticketdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', TicketDocumentDetailsModal.as_view(), name='CDNX_invoicing_ticketpurchasesdocuments_sublist_details'),
    url(r'^ticketdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', TicketDocumentUpdateModal.as_view(), name='CDNX_invoicing_ticketpurchasesdocuments_sublist_edit'),
    url(r'^ticketdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', TicketDocumentUpdateModal.as_view(), name='CDNX_invoicing_ticketpurchasesdocuments_sublist_editmodal'),
    url(r'^ticketdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', TicketDocumentDelete.as_view(), name='CDNX_invoicing_ticketpurchasesdocuments_sublist_delete'),

    url(r'^ticketrectificationdocuments$', TicketRectificationDocumentList.as_view(), name='CDNX_invoicing_ticketrectificationpurchasesdocuments_list'),
    url(r'^ticketrectificationdocuments/(?P<pk>\w+)$', TicketRectificationDocumentDetails.as_view(), name='CDNX_invoicing_ticketrectificationpurchasesdocuments_details'),
    url(r'^ticketrectificationdocuments/(?P<pk>\w+)/delete$', TicketRectificationDocumentDelete.as_view(), name='CDNX_invoicing_ticketrectificationpurchasesdocuments_delete'),
    url(r'^ticketrectificationdocuments/(?P<pk>\w+)/sublist$', TicketRectificationDocumentSubList.as_view(), name='CDNX_invoicing_ticketrectificationpurchasesdocuments_sublist'),
    url(r'^ticketrectificationdocuments/(?P<pk>\w+)/sublist/add$', TicketRectificationDocumentCreateModal.as_view(), name='CDNX_invoicing_ticketrectificationpurchasesdocuments_sublist_add'),
    url(r'^ticketrectificationdocuments/(?P<pk>\w+)/sublist/addmodal$', TicketRectificationDocumentCreateModal.as_view(), name='CDNX_invoicing_ticketrectificationpurchasesdocuments_sublist_addmodal'),
    url(r'^ticketrectificationdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', TicketRectificationDocumentDetailsModal.as_view(), name='CDNX_invoicing_ticketrectificationpurchasesdocuments_sublist_details'),
    url(r'^ticketrectificationdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', TicketRectificationDocumentUpdateModal.as_view(), name='CDNX_invoicing_ticketrectificationpurchasesdocuments_sublist_edit'),
    url(r'^ticketrectificationdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', TicketRectificationDocumentUpdateModal.as_view(), name='CDNX_invoicing_ticketrectificationpurchasesdocuments_sublist_editmodal'),
    url(r'^ticketrectificationdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', TicketRectificationDocumentDelete.as_view(), name='CDNX_invoicing_ticketrectificationpurchasesdocuments_sublist_delete'),

    url(r'^invoicedocuments$', InvoiceDocumentList.as_view(), name='CDNX_invoicing_invoicepurchasesdocuments_list'),
    url(r'^invoicedocuments/(?P<pk>\w+)$', InvoiceDocumentDetails.as_view(), name='CDNX_invoicing_invoicepurchasesdocuments_details'),
    url(r'^invoicedocuments/(?P<pk>\w+)/delete$', InvoiceDocumentDelete.as_view(), name='CDNX_invoicing_invoicepurchasesdocuments_delete'),
    url(r'^invoicedocuments/(?P<pk>\w+)/sublist$', InvoiceDocumentSubList.as_view(), name='CDNX_invoicing_invoicepurchasesdocuments_sublist'),
    url(r'^invoicedocuments/(?P<pk>\w+)/sublist/add$', InvoiceDocumentCreateModal.as_view(), name='CDNX_invoicing_invoicepurchasesdocuments_sublist_add'),
    url(r'^invoicedocuments/(?P<pk>\w+)/sublist/addmodal$', InvoiceDocumentCreateModal.as_view(), name='CDNX_invoicing_invoicepurchasesdocuments_sublist_addmodal'),
    url(r'^invoicedocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', InvoiceDocumentDetailsModal.as_view(), name='CDNX_invoicing_invoicepurchasesdocuments_sublist_details'),
    url(r'^invoicedocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', InvoiceDocumentUpdateModal.as_view(), name='CDNX_invoicing_invoicepurchasesdocuments_sublist_edit'),
    url(r'^invoicedocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', InvoiceDocumentUpdateModal.as_view(), name='CDNX_invoicing_invoicepurchasesdocuments_sublist_editmodal'),
    url(r'^invoicedocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', InvoiceDocumentDelete.as_view(), name='CDNX_invoicing_invoicepurchasesdocuments_sublist_delete'),

    url(r'^invoicerectificationdocuments$', InvoiceRectificationDocumentList.as_view(), name='CDNX_invoicing_invoicerectificationpurchasesdocuments_list'),
    url(r'^invoicerectificationdocuments/(?P<pk>\w+)$', InvoiceRectificationDocumentDetails.as_view(), name='CDNX_invoicing_invoicerectificationpurchasesdocuments_details'),
    url(r'^invoicerectificationdocuments/(?P<pk>\w+)/delete$', InvoiceRectificationDocumentDelete.as_view(), name='CDNX_invoicing_invoicerectificationpurchasesdocuments_delete'),
    url(r'^invoicerectificationdocuments/(?P<pk>\w+)/sublist$', InvoiceRectificationDocumentSubList.as_view(), name='CDNX_invoicing_invoicerectificationpurchasesdocuments_sublist'),
    url(r'^invoicerectificationdocuments/(?P<pk>\w+)/sublist/add$', InvoiceRectificationDocumentCreateModal.as_view(), name='CDNX_invoicing_invoicerectificationpurchasesdocuments_sublist_add'),
    url(r'^invoicerectificationdocuments/(?P<pk>\w+)/sublist/addmodal$', InvoiceRectificationDocumentCreateModal.as_view(), name='CDNX_invoicing_invoicerectificationpurchasesdocuments_sublist_addmodal'),
    url(r'^invoicerectificationdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', InvoiceRectificationDocumentDetailsModal.as_view(), name='CDNX_invoicing_invoicerectificationpurchasesdocuments_sublist_details'),
    url(r'^invoicerectificationdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', InvoiceRectificationDocumentUpdateModal.as_view(), name='CDNX_invoicing_invoicerectificationpurchasesdocuments_sublist_edit'),
    url(r'^invoicerectificationdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', InvoiceRectificationDocumentUpdateModal.as_view(), name='CDNX_invoicing_invoicerectificationpurchasesdocuments_sublist_editmodal'),
    url(r'^invoicerectificationdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', InvoiceRectificationDocumentDelete.as_view(), name='CDNX_invoicing_invoicerectificationpurchasesdocuments_sublist_delete'),

]
