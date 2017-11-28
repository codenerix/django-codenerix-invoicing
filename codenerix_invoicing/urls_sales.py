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
from .views_sales import AlbaranCreate, AlbaranCreateModal, AlbaranDelete, AlbaranList, AlbaranUpdate, AlbaranUpdateModal
from .views_sales import CustomerCreate, CustomerCreateModal, CustomerDelete, CustomerList, CustomerUpdate, CustomerUpdateModal, CustomerDetails
from .views_sales import InvoiceRectificationCreate, InvoiceRectificationCreateModal, InvoiceRectificationDelete, InvoiceRectificationList, InvoiceRectificationUpdate, InvoiceRectificationUpdateModal, InvoiceRectificationDetails, InvoiceRectificationPrint
from .views_sales import InvoiceCreate, InvoiceCreateModal, InvoiceDelete, InvoiceList, InvoiceUpdate, InvoiceUpdateModal, InvoicePrint
from .views_sales import LineAlbaranCreate, LineAlbaranCreateModal, LineAlbaranDelete, LineAlbaranList, LineAlbaranUpdate, LineAlbaranUpdateModal
from .views_sales import LineInvoiceRectificationCreate, LineInvoiceRectificationCreateModal, LineInvoiceRectificationDelete, LineInvoiceRectificationList, LineInvoiceRectificationUpdate, LineInvoiceRectificationUpdateModal, LineInvoiceRectificationSubList, LineInvoiceRectificationDetailModal
from .views_sales import LineInvoiceCreate, LineInvoiceCreateModal, LineInvoiceDelete, LineInvoiceList, LineInvoiceUpdate, LineInvoiceUpdateModal
from .views_sales import LineOrderCreateModal, LineOrderDelete, LineOrderDetailsModal, LineOrderList, LineOrderSubList, LineOrderUpdateModal
from .views_sales import LineTicketRectificationCreate, LineTicketRectificationCreateModal, LineTicketRectificationDelete, LineTicketRectificationList, LineTicketRectificationUpdate, LineTicketRectificationUpdateModal, LineTicketRectificationSubList, LineTicketRectificationDetailModal
from .views_sales import LineTicketCreate, LineTicketCreateModal, LineTicketDelete, LineTicketList, LineTicketUpdate, LineTicketUpdateModal
from .views_sales import OrderCreate, OrderCreateModal, OrderDelete, OrderDetails, OrderList, OrderUpdate, OrderUpdateModal, OrderPrint
from .views_sales import TicketRectificationCreate, TicketRectificationCreateModal, TicketRectificationDelete, TicketRectificationList, TicketRectificationUpdate, TicketRectificationUpdateModal, TicketRectificationDetails
from .views_sales import TicketCreate, TicketCreateModal, TicketDelete, TicketList, TicketUpdate, TicketUpdateModal
from .views_sales import AlbaranDetails, LineAlbaranSubList, AlbaranPrint, LineAlbaranDetailsModal
from .views_sales import TicketDetails, LineTicketSubList, TicketPrint, LineTicketDetailsModal
from .views_sales import InvoiceDetails, LineInvoiceSubList, LineInvoiceDetailsModal
from .views_sales import OrderCreateAlbaran, OrderCreateTicket, OrderCreateInvoice, OrderStatus
from .views_sales import AlbaranCreateTicket, AlbaranCreateInvoice
from .views_sales import TicketCreateInvoice
from .views_sales import OrderForeign, LineOrderForeign, LineOrderForeignCustom
from .views_sales import InvoiceCreateRectification, LineInvoiceForeign, TicketCreateRectification, LineTicketForeign, TicketRectificationPrint
from .views_sales import CustomerDocumentSubList, CustomerDocumentCreateModal, CustomerDocumentDetailsModal, CustomerDocumentUpdateModal, CustomerDocumentDelete
from .views_sales import ReservedProductList, ReservedProductCreate, ReservedProductUpdate, ReservedProductDelete
from .views_sales import BasketCreate, BasketCreateModal, BasketUpdate, BasketUpdateModal, BasketDetails, BasketDelete
from .views_sales import BasketListSHOPPINGCART, BasketDetailsSHOPPINGCART, BasketCreateSHOPPINGCART, BasketCreateSHOPPINGCARTModal, BasketUpdateSHOPPINGCART, BasketDeleteSHOPPINGCART
from .views_sales import BasketListBUDGET, BasketDetailsBUDGET, BasketCreateBUDGET, BasketCreateBUDGETModal, BasketUpdateBUDGET, BasketDeleteBUDGET
from .views_sales import BasketListWISHLIST, BasketDetailsWISHLIST, BasketCreateWISHLIST, BasketCreateWISHLISTModal, BasketUpdateWISHLIST, BasketDeleteWISHLIST
from .views_sales import BasketPassToBudget
from .views_sales import BasketPassToOrder
from .views_sales import LineBasketList, LineBasketCreate, LineBasketCreateModal, LineBasketUpdate, LineBasketUpdateModal, LineBasketDelete, LineBasketSubList, LineBasketDetails, LineBasketDetailModal, LineBasketCreateModalPack, LineBasketForeign
from .views_sales import ShoppingCartManagement
from .views_sales import CustomerForeignBudget, CustomerForeignShoppingCart
from .views_sales import BasketForeignShoppingCart, BasketForeignBudget
from .views_sales import OrderCreateModalFromBudget, OrderCreateModalFromShoppingCart

from .views_sales import ReasonModificationList, ReasonModificationCreate, ReasonModificationCreateModal, ReasonModificationUpdate, ReasonModificationUpdateModal, ReasonModificationDelete, ReasonModificationSubList, ReasonModificationDetails, ReasonModificationDetailModal
from .views_sales import ReasonModificationLineBasketList, ReasonModificationLineBasketCreate, ReasonModificationLineBasketCreateModal, ReasonModificationLineBasketUpdate, ReasonModificationLineBasketUpdateModal, ReasonModificationLineBasketDelete, ReasonModificationLineBasketSubList, ReasonModificationLineBasketDetails, ReasonModificationLineBasketDetailModal
from .views_sales import ReasonModificationLineOrderList, ReasonModificationLineOrderCreate, ReasonModificationLineOrderCreateModal, ReasonModificationLineOrderUpdate, ReasonModificationLineOrderUpdateModal, ReasonModificationLineOrderDelete, ReasonModificationLineOrderSubList, ReasonModificationLineOrderDetails, ReasonModificationLineOrderDetailModal
from .views_sales import ReasonModificationLineAlbaranList, ReasonModificationLineAlbaranCreate, ReasonModificationLineAlbaranCreateModal, ReasonModificationLineAlbaranUpdate, ReasonModificationLineAlbaranUpdateModal, ReasonModificationLineAlbaranDelete, ReasonModificationLineAlbaranSubList, ReasonModificationLineAlbaranDetails, ReasonModificationLineAlbaranDetailModal
from .views_sales import ReasonModificationLineTicketList, ReasonModificationLineTicketCreate, ReasonModificationLineTicketCreateModal, ReasonModificationLineTicketUpdate, ReasonModificationLineTicketUpdateModal, ReasonModificationLineTicketDelete, ReasonModificationLineTicketSubList, ReasonModificationLineTicketDetails, ReasonModificationLineTicketDetailModal
from .views_sales import ReasonModificationLineTicketRectificationList, ReasonModificationLineTicketRectificationCreate, ReasonModificationLineTicketRectificationCreateModal, ReasonModificationLineTicketRectificationUpdate, ReasonModificationLineTicketRectificationUpdateModal, ReasonModificationLineTicketRectificationDelete, ReasonModificationLineTicketRectificationSubList, ReasonModificationLineTicketRectificationDetails, ReasonModificationLineTicketRectificationDetailModal
from .views_sales import ReasonModificationLineInvoiceList, ReasonModificationLineInvoiceCreate, ReasonModificationLineInvoiceCreateModal, ReasonModificationLineInvoiceUpdate, ReasonModificationLineInvoiceUpdateModal, ReasonModificationLineInvoiceDelete, ReasonModificationLineInvoiceSubList, ReasonModificationLineInvoiceDetails, ReasonModificationLineInvoiceDetailModal
from .views_sales import ReasonModificationLineInvoiceRectificationList, ReasonModificationLineInvoiceRectificationCreate, ReasonModificationLineInvoiceRectificationCreateModal, ReasonModificationLineInvoiceRectificationUpdate, ReasonModificationLineInvoiceRectificationUpdateModal, ReasonModificationLineInvoiceRectificationDelete, ReasonModificationLineInvoiceRectificationSubList, ReasonModificationLineInvoiceRectificationDetails, ReasonModificationLineInvoiceRectificationDetailModal

from .views_sales import LineAlbaranForeign, LineTicketRectificationForeign, LineInvoiceRectificationForeign
from .views_sales import PrintCounterDocumentBasketSublist, PrintCounterDocumentOrderSublist, PrintCounterDocumentAlbaranSublist, PrintCounterDocumentTicketSublist, PrintCounterDocumentTicketRectificationSublist, PrintCounterDocumentInvoiceSublist, PrintCounterDocumentInvoiceRectificationSublist
from .views_sales import OrderDocumentList, OrderDocumentCreate, OrderDocumentCreateModal, OrderDocumentUpdate, OrderDocumentUpdateModal, OrderDocumentDelete, OrderDocumentSubList, OrderDocumentDetails, OrderDocumentDetailModal

from .views_sales import BasketPrintBUDGET

urlpatterns = [
    url(r'^customers$', CustomerList.as_view(), name='CDNX_invoicing_customers_list'),
    url(r'^customers/add$', CustomerCreate.as_view(), name='CDNX_invoicing_customers_add'),
    url(r'^customers/addmodal$', CustomerCreateModal.as_view(), name='CDNX_invoicing_customers_addmodal'),
    url(r'^customers/(?P<pk>\w+)$', CustomerDetails.as_view(), name='CDNX_invoicing_customers_detail'),
    url(r'^customers/(?P<pk>\w+)/edit$', CustomerUpdate.as_view(), name='CDNX_invoicing_customers_edit'),
    url(r'^customers/(?P<pk>\w+)/editmodal$', CustomerUpdateModal.as_view(), name='CDNX_invoicing_customers_editmodal'),
    url(r'^customers/(?P<pk>\w+)/delete$', CustomerDelete.as_view(), name='CDNX_invoicing_customers_delete'),

    url(r'^customers/foreign/shoppingcarts/(?P<search>[\w\W]+|\*)$', CustomerForeignShoppingCart.as_view(), name='CDNX_invoicing_customers_foreign_from_shoppingcart'),
    url(r'^customers/foreign/(?P<search>[\w\W]+|\*)$', CustomerForeignBudget.as_view(), name='CDNX_invoicing_customers_foreign_from_budget'),

    url(r'^customerdocuments/(?P<pk>\w+)/sublist$', CustomerDocumentSubList.as_view(), name='CDNX_invoicing_customerdocuments_sublist'),
    url(r'^customerdocuments/(?P<pk>\w+)/sublist/add$', CustomerDocumentCreateModal.as_view(), name='CDNX_invoicing_customerdocuments_sublist_add'),
    url(r'^customerdocuments/(?P<pk>\w+)/sublist/addmodal$', CustomerDocumentCreateModal.as_view(), name='CDNX_invoicing_customerdocuments_sublist_addmodal'),
    url(r'^customerdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', CustomerDocumentDetailsModal.as_view(), name='CDNX_invoicing_customerdocuments_sublist_details'),
    url(r'^customerdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', CustomerDocumentUpdateModal.as_view(), name='CDNX_invoicing_customerdocuments_sublist_edit'),
    url(r'^customerdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', CustomerDocumentUpdateModal.as_view(), name='CDNX_invoicing_customerdocuments_sublist_editmodal'),
    url(r'^customerdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', CustomerDocumentDelete.as_view(), name='CDNX_invoicing_customerdocuments_sublist_delete'),

    url(r'^orders$', OrderList.as_view(), name='CDNX_invoicing_ordersaless_list'),
    url(r'^orders/add$', OrderCreate.as_view(), name='CDNX_invoicing_ordersaless_add'),
    url(r'^orders/addmodal$', OrderCreateModal.as_view(), name='CDNX_invoicing_ordersaless_addmodal'),

    url(r'^orders/addfrombudget$', OrderCreateModalFromBudget.as_view(), name='CDNX_invoicing_ordersaless_add_from_budget'),
    url(r'^orders/addfromshoppingcart$', OrderCreateModalFromShoppingCart.as_view(), name='CDNX_invoicing_ordersaless_add_from_shoppingcart'),

    url(r'^orders/(?P<pk>\w+)$', OrderDetails.as_view(), name='CDNX_invoicing_ordersaless_details'),
    url(r'^orders/(?P<pk>\w+)/edit$', OrderUpdate.as_view(), name='CDNX_invoicing_ordersaless_edit'),
    url(r'^orders/(?P<pk>\w+)/editmodal$', OrderUpdateModal.as_view(), name='CDNX_invoicing_ordersaless_editmodal'),
    url(r'^orders/(?P<pk>\w+)/delete$', OrderDelete.as_view(), name='CDNX_invoicing_ordersaless_delete'),
    url(r'^orders/(?P<pk>\w+)/status/(?P<action>\w+)$', OrderStatus.as_view(), name='CDNX_invoicing_ordersaless_status'),
    url(r'^orders/(?P<pk>\w+)/createalbaran$', OrderCreateAlbaran.as_view(), name='CDNX_invoicing_ordersaless_create_albaran'),
    url(r'^orders/(?P<pk>\w+)/createticket$', OrderCreateTicket.as_view(), name='CDNX_invoicing_ordersaless_create_ticket'),
    url(r'^orders/(?P<pk>\w+)/createinvoice$', OrderCreateInvoice.as_view(), name='CDNX_invoicing_ordersaless_create_invoice'),
    url(r'^orders/foreign/(?P<search>[\w\W]+|\*)$', OrderForeign.as_view(), name='CDNX_invoicing_ordersaless_foreign'),
    url(r'^orders/(?P<pk>\w+)/print$', OrderPrint.as_view(), name='CDNX_invoicing_ordersaless_print'),

    url(r'^lineorders$', LineOrderList.as_view(), name='CDNX_invoicing_lineordersaless_list'),
    url(r'^lineorders/(?P<pk>\w+)/delete$', LineOrderDelete.as_view(), name='CDNX_invoicing_lineordersaless_delete'),
    url(r'^lineorders/(?P<pk>\w+)/sublist$', LineOrderSubList.as_view(), name='CDNX_invoicing_lineordersaless_sublist'),
    url(r'^lineorders/(?P<pk>\w+)/sublist/addmodal$', LineOrderCreateModal.as_view(), name='CDNX_invoicing_lineordersaless_sublist_add'),
    url(r'^lineorders/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineOrderDetailsModal.as_view(), name='CDNX_invoicing_lineordersaless_sublist_details'),
    url(r'^lineorders/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineOrderUpdateModal.as_view(), name='CDNX_invoicing_lineordersaless_sublist_details'),
    url(r'^lineorders/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineOrderDelete.as_view(), name='CDNX_invoicing_lineordersaless_sublist_delete'),
    url(r'^lineorders/foreign/(?P<search>[\w\W]+|\*)$', LineOrderForeign.as_view(), name='CDNX_invoicing_lineordersaless_foreign'),
    url(r'^lineorders/foreigncustom/(?P<search>[\w\W]+|\*)$', LineOrderForeignCustom.as_view(), name='CDNX_invoicing_lineordersaless_foreign_custom'),

    url(r'^albarans$', AlbaranList.as_view(), name='CDNX_invoicing_albaransaless_list'),
    url(r'^albarans/add$', AlbaranCreate.as_view(), name='CDNX_invoicing_albaransaless_add'),
    url(r'^albarans/addmodal$', AlbaranCreateModal.as_view(), name='CDNX_invoicing_albaransaless_addmodal'),
    url(r'^albarans/(?P<pk>\w+)$', AlbaranDetails.as_view(), name='CDNX_invoicing_albaransaless_details'),
    url(r'^albarans/(?P<pk>\w+)/edit$', AlbaranUpdate.as_view(), name='CDNX_invoicing_albaransaless_edit'),
    url(r'^albarans/(?P<pk>\w+)/editmodal$', AlbaranUpdateModal.as_view(), name='CDNX_invoicing_albaransaless_editmodal'),
    url(r'^albarans/(?P<pk>\w+)/delete$', AlbaranDelete.as_view(), name='CDNX_invoicing_albaransaless_delete'),
    url(r'^albarans/(?P<pk>\w+)/createticket$', AlbaranCreateTicket.as_view(), name='CDNX_invoicing_albaransaless_create_ticket'),
    url(r'^albarans/(?P<pk>\w+)/createinvoice$', AlbaranCreateInvoice.as_view(), name='CDNX_invoicing_albaransaless_create_invoice'),
    url(r'^albarans/(?P<pk>\w+)/print$', AlbaranPrint.as_view(), name='CDNX_invoicing_albaransaless_print'),

    url(r'^linealbarans$', LineAlbaranList.as_view(), name='CDNX_invoicing_linealbaransaless_list'),
    url(r'^linealbarans/(?P<pk>\w+)/delete$', LineAlbaranDelete.as_view(), name='CDNX_invoicing_linealbaransaless_delete'),
    url(r'^linealbarans/(?P<pk>\w+)/sublist$', LineAlbaranSubList.as_view(), name='CDNX_invoicing_linealbaransaless_sublist'),
    url(r'^linealbarans/(?P<pk>\w+)/sublist/addmodal$', LineAlbaranCreateModal.as_view(), name='CDNX_invoicing_linealbaransaless_sublist_add'),
    url(r'^linealbarans/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineAlbaranDetailsModal.as_view(), name='CDNX_invoicing_linealbaransaless_sublist_details'),
    url(r'^linealbarans/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineAlbaranUpdateModal.as_view(), name='CDNX_invoicing_linealbaransaless_sublist_details'),
    url(r'^linealbarans/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineAlbaranDelete.as_view(), name='CDNX_invoicing_linealbaransaless_sublist_delete'),
    url(r'^linealbarans/foreign/(?P<search>[\w\W]+|\*)$', LineAlbaranForeign.as_view(), name='CDNX_invoicing_linealbaransaless_foreign'),


    url(r'^tickets$', TicketList.as_view(), name='CDNX_invoicing_ticketsaless_list'),
    url(r'^tickets/add$', TicketCreate.as_view(), name='CDNX_invoicing_ticketsaless_add'),
    url(r'^tickets/addmodal$', TicketCreateModal.as_view(), name='CDNX_invoicing_ticketsaless_addmodal'),
    url(r'^tickets/(?P<pk>\w+)$', TicketDetails.as_view(), name='CDNX_invoicing_ticketsales_details'),
    url(r'^tickets/(?P<pk>\w+)/edit$', TicketUpdate.as_view(), name='CDNX_invoicing_ticketsaless_edit'),
    url(r'^tickets/(?P<pk>\w+)/editmodal$', TicketUpdateModal.as_view(), name='CDNX_invoicing_ticketsaless_editmodal'),
    url(r'^tickets/(?P<pk>\w+)/delete$', TicketDelete.as_view(), name='CDNX_invoicing_ticketsaless_delete'),
    url(r'^tickets/(?P<pk>\w+)/createinvoice$', TicketCreateInvoice.as_view(), name='CDNX_invoicing_ticketsaless_create_invoice'),
    url(r'^tickets/(?P<pk>\w+)/createticketrectification$', TicketCreateRectification.as_view(), name='CDNX_invoicing_ticketsaless_create_rectification'),
    url(r'^tickets/(?P<pk>\w+)/print$', TicketPrint.as_view(), name='CDNX_invoicing_ticketsaless_print'),

    url(r'^linetickets$', LineTicketList.as_view(), name='CDNX_invoicing_lineticketsaless_list'),
    url(r'^linetickets/(?P<pk>\w+)/delete$', LineTicketDelete.as_view(), name='CDNX_invoicing_lineticketsaless_delete'),
    url(r'^linetickets/(?P<pk>\w+)/sublist$', LineTicketSubList.as_view(), name='CDNX_invoicing_lineticketsaless_sublist'),
    url(r'^linetickets/(?P<pk>\w+)/sublist/addmodal$', LineTicketCreateModal.as_view(), name='CDNX_invoicing_lineticketsaless_sublist_add'),
    url(r'^linetickets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineTicketDetailsModal.as_view(), name='CDNX_invoicing_lineticketsaless_sublist_details'),
    url(r'^linetickets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineTicketUpdateModal.as_view(), name='CDNX_invoicing_lineticketsaless_sublist_details'),
    url(r'^linetickets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineTicketDelete.as_view(), name='CDNX_invoicing_lineticketsaless_sublist_delete'),
    url(r'^linetickets/foreign/(?P<search>[\w\W]+|\*)$', LineTicketForeign.as_view(), name='CDNX_invoicing_lineticketsaless_foreign'),

    url(r'^ticketrectifications$', TicketRectificationList.as_view(), name='CDNX_invoicing_ticketrectificationsaless_list'),
    url(r'^ticketrectifications/add$', TicketRectificationCreate.as_view(), name='CDNX_invoicing_ticketrectificationsaless_add'),
    url(r'^ticketrectifications/addmodal$', TicketRectificationCreateModal.as_view(), name='CDNX_invoicing_ticketrectificationsaless_addmodal'),
    url(r'^ticketrectifications/(?P<pk>\w+)$', TicketRectificationDetails.as_view(), name='CDNX_invoicing_invoicesales_details'),
    url(r'^ticketrectifications/(?P<pk>\w+)/edit$', TicketRectificationUpdate.as_view(), name='CDNX_invoicing_ticketrectificationsaless_edit'),
    url(r'^ticketrectifications/(?P<pk>\w+)/editmodal$', TicketRectificationUpdateModal.as_view(), name='CDNX_invoicing_ticketrectificationsaless_editmodal'),
    url(r'^ticketrectifications/(?P<pk>\w+)/delete$', TicketRectificationDelete.as_view(), name='CDNX_invoicing_ticketrectificationsaless_delete'),
    url(r'^ticketrectifications/(?P<pk>\w+)/print$', TicketRectificationPrint.as_view(), name='CDNX_invoicing_ticketrectificationsaless_print'),

    url(r'^lineticketrectifications/(?P<pk>\w+)/sublist$', LineTicketRectificationSubList.as_view(), name='CDNX_invoicing_lineticketrectificationsaless_sublist'),
    url(r'^lineticketrectifications/(?P<pk>\w+)/sublist/addmodal$', LineTicketRectificationCreateModal.as_view(), name='CDNX_invoicing_lineticketrectificationsaless_sublist_add'),
    url(r'^lineticketrectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineTicketRectificationDetailModal.as_view(), name='CDNX_invoicing_lineticketrectificationsaless_sublist_details'),
    url(r'^lineticketrectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineTicketRectificationUpdateModal.as_view(), name='CDNX_invoicing_lineticketrectificationsaless_sublist_details'),
    url(r'^lineticketrectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineTicketRectificationDelete.as_view(), name='CDNX_invoicing_lineticketrectificationsaless_sublist_delete'),
    url(r'^lineticketrectifications/foreign/(?P<search>[\w\W]+|\*)$', LineTicketRectificationForeign.as_view(), name='CDNX_invoicing_lineticketrectificationsaless_sublist_foreign'),

    url(r'^invoices$', InvoiceList.as_view(), name='CDNX_invoicing_invoicesaless_list'),
    url(r'^invoices/add$', InvoiceCreate.as_view(), name='CDNX_invoicing_invoicesaless_add'),
    url(r'^invoices/addmodal$', InvoiceCreateModal.as_view(), name='CDNX_invoicing_invoicesaless_addmodal'),
    url(r'^invoices/(?P<pk>\w+)$', InvoiceDetails.as_view(), name='CDNX_invoicing_invoicesales_details'),
    url(r'^invoices/(?P<pk>\w+)/edit$', InvoiceUpdate.as_view(), name='CDNX_invoicing_invoicesaless_edit'),
    url(r'^invoices/(?P<pk>\w+)/editmodal$', InvoiceUpdateModal.as_view(), name='CDNX_invoicing_invoicesaless_editmodal'),
    url(r'^invoices/(?P<pk>\w+)/delete$', InvoiceDelete.as_view(), name='CDNX_invoicing_invoicesaless_delete'),
    url(r'^invoices/(?P<pk>\w+)/createinvoicerectification$', InvoiceCreateRectification.as_view(), name='CDNX_invoicing_invoicesaless_create_rectification'),
    url(r'^invoices/(?P<pk>\w+)/print$', InvoicePrint.as_view(), name='CDNX_invoicing_invoicesaless_print'),

    url(r'^lineinvoices$', LineInvoiceList.as_view(), name='CDNX_invoicing_lineinvoicesaless_list'),
    url(r'^lineinvoices/(?P<pk>\w+)/delete$', LineInvoiceDelete.as_view(), name='CDNX_invoicing_lineinvoicesaless_delete'),
    url(r'^lineinvoices/(?P<pk>\w+)/sublist$', LineInvoiceSubList.as_view(), name='CDNX_invoicing_lineinvoicesaless_sublist'),
    url(r'^lineinvoices/(?P<pk>\w+)/sublist/addmodal$', LineInvoiceCreateModal.as_view(), name='CDNX_invoicing_lineinvoicesaless_sublist_add'),
    url(r'^lineinvoices/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineInvoiceDetailsModal.as_view(), name='CDNX_invoicing_lineinvoicesaless_sublist_details'),
    url(r'^lineinvoices/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineInvoiceUpdateModal.as_view(), name='CDNX_invoicing_lineinvoicesaless_sublist_details'),
    url(r'^lineinvoices/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineInvoiceDelete.as_view(), name='CDNX_invoicing_lineinvoicesaless_sublist_delete'),
    url(r'^lineinvoices/foreign/(?P<search>[\w\W]+|\*)$', LineInvoiceForeign.as_view(), name='CDNX_invoicing_lineinvoicessaless_foreign'),

    url(r'^invoicerectifications$', InvoiceRectificationList.as_view(), name='CDNX_invoicing_invoicerectificationsaless_list'),
    url(r'^invoicerectifications/add$', InvoiceRectificationCreate.as_view(), name='CDNX_invoicing_invoicerectificationsaless_add'),
    url(r'^invoicerectifications/addmodal$', InvoiceRectificationCreateModal.as_view(), name='CDNX_invoicing_invoicerectificationsaless_addmodal'),
    url(r'^invoicerectifications/(?P<pk>\w+)$', InvoiceRectificationDetails.as_view(), name='CDNX_invoicing_invoicerectificationsaless_detail'),
    url(r'^invoicerectifications/(?P<pk>\w+)/edit$', InvoiceRectificationUpdate.as_view(), name='CDNX_invoicing_invoicerectificationsaless_edit'),
    url(r'^invoicerectifications/(?P<pk>\w+)/editmodal$', InvoiceRectificationUpdateModal.as_view(), name='CDNX_invoicing_invoicerectificationsaless_editmodal'),
    url(r'^invoicerectifications/(?P<pk>\w+)/delete$', InvoiceRectificationDelete.as_view(), name='CDNX_invoicing_invoicerectificationsaless_delete'),
    url(r'^invoicerectifications/(?P<pk>\w+)/print$', InvoiceRectificationPrint.as_view(), name='CDNX_invoicing_invoicerectificationsaless_print'),

    url(r'^lineinvoicerectifications/(?P<pk>\w+)/sublist$', LineInvoiceRectificationSubList.as_view(), name='CDNX_invoicing_lineinvoicerectificationsaless_sublist'),
    url(r'^lineinvoicerectifications/(?P<pk>\w+)/sublist/addmodal$', LineInvoiceRectificationCreateModal.as_view(), name='CDNX_invoicing_lineinvoicerectificationsaless_sublist_add'),
    url(r'^lineinvoicerectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineInvoiceRectificationDetailModal.as_view(), name='CDNX_invoicing_lineinvoicerectificationsaless_sublist_details'),
    url(r'^lineinvoicerectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineInvoiceRectificationUpdateModal.as_view(), name='CDNX_invoicing_lineinvoicerectificationsaless_sublist_details'),
    url(r'^lineinvoicerectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineInvoiceRectificationDelete.as_view(), name='CDNX_invoicing_lineinvoicerectificationsaless_sublist_delete'),
    url(r'^lineinvoicerectifications/foreign/(?P<search>[\w\W]+|\*)$', LineInvoiceRectificationForeign.as_view(), name='CDNX_invoicing_lineinvoicerectificationsaless_sublist_foreign'),

    url(r'^reservedproducts$', ReservedProductList.as_view(), name='CDNX_invoicing_reservedproducts_list'),
    url(r'^reservedproducts/add$', ReservedProductCreate.as_view(), name='CDNX_invoicing_reservedproducts_add'),
    url(r'^reservedproducts/(?P<pk>\w+)/edit$', ReservedProductUpdate.as_view(), name='CDNX_invoicing_reservedproducts_edit'),
    url(r'^reservedproducts/(?P<pk>\w+)/delete$', ReservedProductDelete.as_view(), name='CDNX_invoicing_reservedproducts_delete'),

    url(r'^shoppingcarts/management$', ShoppingCartManagement.as_view(), name='CDNX_invoicing_shoppingcarts_management'),

    url(r'^nshoppingcarts$', BasketListSHOPPINGCART.as_view(), name='CDNX_invoicing_salesbaskets_shoppingcart_list'),
    url(r'^nbudgets$', BasketListBUDGET.as_view(), name='CDNX_invoicing_salesbaskets_budget_list'),
    url(r'^nwishlists$', BasketListWISHLIST.as_view(), name='CDNX_invoicing_salesbaskets_wishlist_list'),

    url(r'^nshoppingcarts/add$', BasketCreateSHOPPINGCART.as_view(), name='CDNX_invoicing_salesbaskets_SHOPPINGCART_add'),
    url(r'^nbudgets/add$', BasketCreateBUDGET.as_view(), name='CDNX_invoicing_salesbaskets_BUDGET_add'),
    url(r'^nwishlists/add$', BasketCreateWISHLIST.as_view(), name='CDNX_invoicing_salesbaskets_WISHLIST_add'),

    url(r'^nshoppingcarts/(?P<pk>\w+)$', BasketDetailsSHOPPINGCART.as_view(), name='CDNX_invoicing_salesbaskets_SHOPPINGCART_details'),
    url(r'^nbudgets/(?P<pk>\w+)$', BasketDetailsBUDGET.as_view(), name='CDNX_invoicing_salesbaskets_BUDGET_details'),
    url(r'^nwishlists/(?P<pk>\w+)$', BasketDetailsWISHLIST.as_view(), name='CDNX_invoicing_salesbaskets_WISHLIST_details'),

    url(r'^nshoppingcarts/addmodal$', BasketCreateSHOPPINGCARTModal.as_view(), name='CDNX_invoicing_salesbaskets_SHOPPINGCART_addmodal'),
    url(r'^nbudgets/addmodal$', BasketCreateBUDGETModal.as_view(), name='CDNX_invoicing_salesbaskets_BUDGET_addmodal'),
    url(r'^nwishlists/addmodal$', BasketCreateWISHLISTModal.as_view(), name='CDNX_invoicing_salesbaskets_WISHLIST_addmodal'),

    url(r'^nshoppingcarts/(?P<pk>\w+)/edit$', BasketUpdateSHOPPINGCART.as_view(), name='CDNX_invoicing_salesbaskets_SHOPPINGCART_edit'),
    url(r'^nbudgets/(?P<pk>\w+)/edit$', BasketUpdateBUDGET.as_view(), name='CDNX_invoicing_salesbaskets_BUDGET_edit'),
    url(r'^nwishlists/(?P<pk>\w+)/edit$', BasketUpdateWISHLIST.as_view(), name='CDNX_invoicing_salesbaskets_WISHLIST_edit'),

    url(r'^nshoppingcarts/(?P<pk>\w+)/delete$', BasketDeleteSHOPPINGCART.as_view(), name='CDNX_invoicing_salesbaskets_SHOPPINGCART_delete'),
    url(r'^nbudgets/(?P<pk>\w+)/delete$', BasketDeleteBUDGET.as_view(), name='CDNX_invoicing_salesbaskets_BUDGET_delete'),
    url(r'^nwishlists/(?P<pk>\w+)/delete$', BasketDeleteWISHLIST.as_view(), name='CDNX_invoicing_salesbaskets_WISHLIST_delete'),

    url(r'^nshoppingcarts/(?P<pk>\w+)/createbudget$', BasketPassToBudget.as_view(), name='CDNX_invoicing_salesbaskets_createbudget'),
    url(r'^nbudgets/(?P<pk>\w+)/createorder$', BasketPassToOrder.as_view(), name='CDNX_invoicing_salesbaskets_createorder'),

    url(r'^nshoppingcarts/foreign/(?P<search>[\w\W]+|\*)$', BasketForeignShoppingCart.as_view(), name='CDNX_invoicing_salesbaskets_foreignkey_shoppingcart'),
    url(r'^nbudgets/foreign/(?P<search>[\w\W]+|\*)$', BasketForeignBudget.as_view(), name='CDNX_invoicing_salesbaskets_foreignkey_budget'),

    url(r'^nbudgets/(?P<pk>\w+)/print$', BasketPrintBUDGET.as_view(), name='CDNX_invoicing_budgetsaless_print'),

    url(r'^linebaskets$', LineBasketList.as_view(), name='CDNX_invoicing_saleslinebaskets_list'),
    url(r'^linebaskets/add$', LineBasketCreate.as_view(), name='CDNX_invoicing_saleslinebaskets_add'),
    url(r'^linebaskets/addmodal$', LineBasketCreateModal.as_view(), name='CDNX_invoicing_saleslinebaskets_addmodal'),
    url(r'^linebaskets/(?P<pk>\w+)$', LineBasketDetails.as_view(), name='CDNX_invoicing_saleslinebaskets_details'),
    url(r'^linebaskets/(?P<pk>\w+)/edit$', LineBasketUpdate.as_view(), name='CDNX_invoicing_saleslinebaskets_edit'),
    url(r'^linebaskets/(?P<pk>\w+)/editmodal$', LineBasketUpdateModal.as_view(), name='CDNX_invoicing_saleslinebaskets_editmodal'),
    url(r'^linebaskets/(?P<pk>\w+)/delete$', LineBasketDelete.as_view(), name='CDNX_invoicing_saleslinebaskets_delete'),
    url(r'^linebaskets/(?P<pk>\w+)/sublist$', LineBasketSubList.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist'),
    url(r'^linebaskets/(?P<pk>\w+)/sublist/addmodal$', LineBasketCreateModal.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist_add'),
    url(r'^linebaskets/(?P<pk>\w+)/sublist/addpackmodal$', LineBasketCreateModalPack.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist_addpack'),
    url(r'^linebaskets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineBasketDetailModal.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist_details'),
    url(r'^linebaskets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineBasketUpdateModal.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist_details'),
    url(r'^linebaskets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineBasketDelete.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist_delete'),
    url(r'^linebaskets/foreign/(?P<search>[\w\W]+|\*)$', LineBasketForeign.as_view(), name='CDNX_invoicing_linebasketsaless_foreign'),



    url(r'^reasonmodifications$', ReasonModificationList.as_view(), name='CDNX_invoicing_reasonmodifications_list'),
    url(r'^reasonmodifications/add$', ReasonModificationCreate.as_view(), name='CDNX_invoicing_reasonmodifications_add'),
    url(r'^reasonmodifications/addmodal$', ReasonModificationCreateModal.as_view(), name='CDNX_invoicing_reasonmodifications_addmodal'),
    url(r'^reasonmodifications/(?P<pk>\w+)$', ReasonModificationDetails.as_view(), name='CDNX_invoicing_reasonmodifications_details'),
    url(r'^reasonmodifications/(?P<pk>\w+)/edit$', ReasonModificationUpdate.as_view(), name='CDNX_invoicing_reasonmodifications_edit'),
    url(r'^reasonmodifications/(?P<pk>\w+)/editmodal$', ReasonModificationUpdateModal.as_view(), name='CDNX_invoicing_reasonmodifications_editmodal'),
    url(r'^reasonmodifications/(?P<pk>\w+)/delete$', ReasonModificationDelete.as_view(), name='CDNX_invoicing_reasonmodifications_delete'),
    url(r'^reasonmodifications/(?P<pk>\w+)/sublist$', ReasonModificationSubList.as_view(), name='CDNX_invoicing_reasonmodifications_sublist'),
    url(r'^reasonmodifications/(?P<pk>\w+)/sublist/add$', ReasonModificationCreateModal.as_view(), name='CDNX_invoicing_reasonmodifications_sublist_add'),
    url(r'^reasonmodifications/(?P<pk>\w+)/sublist/addmodal$', ReasonModificationCreateModal.as_view(), name='CDNX_invoicing_reasonmodifications_sublist_addmodal'),
    url(r'^reasonmodifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ReasonModificationDetailModal.as_view(), name='CDNX_invoicing_reasonmodifications_sublist_details'),
    url(r'^reasonmodifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', ReasonModificationUpdateModal.as_view(), name='CDNX_invoicing_reasonmodifications_sublist_edit'),
    url(r'^reasonmodifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', ReasonModificationUpdateModal.as_view(), name='CDNX_invoicing_reasonmodifications_sublist_editmodal'),
    url(r'^reasonmodifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', ReasonModificationDelete.as_view(), name='CDNX_invoicing_reasonmodifications_sublist_delete'),


    url(r'^reasonmodificationlinebaskets$', ReasonModificationLineBasketList.as_view(), name='CDNX_invoicing_reasonmodificationlinebaskets_list'),
    url(r'^reasonmodificationlinebaskets/add$', ReasonModificationLineBasketCreate.as_view(), name='CDNX_invoicing_reasonmodificationlinebaskets_add'),
    url(r'^reasonmodificationlinebaskets/addmodal$', ReasonModificationLineBasketCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinebaskets_addmodal'),
    url(r'^reasonmodificationlinebaskets/(?P<pk>\w+)$', ReasonModificationLineBasketDetails.as_view(), name='CDNX_invoicing_reasonmodificationlinebaskets_details'),
    url(r'^reasonmodificationlinebaskets/(?P<pk>\w+)/edit$', ReasonModificationLineBasketUpdate.as_view(), name='CDNX_invoicing_reasonmodificationlinebaskets_edit'),
    url(r'^reasonmodificationlinebaskets/(?P<pk>\w+)/editmodal$', ReasonModificationLineBasketUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinebaskets_editmodal'),
    url(r'^reasonmodificationlinebaskets/(?P<pk>\w+)/delete$', ReasonModificationLineBasketDelete.as_view(), name='CDNX_invoicing_reasonmodificationlinebaskets_delete'),
    url(r'^reasonmodificationlinebaskets/(?P<pk>\w+)/sublist$', ReasonModificationLineBasketSubList.as_view(), name='CDNX_invoicing_reasonmodificationlinebaskets_sublist'),
    url(r'^reasonmodificationlinebaskets/(?P<pk>\w+)/sublist/add$', ReasonModificationLineBasketCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinebaskets_sublist_add'),
    url(r'^reasonmodificationlinebaskets/(?P<pk>\w+)/sublist/addmodal$', ReasonModificationLineBasketCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinebaskets_sublist_addmodal'),
    url(r'^reasonmodificationlinebaskets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ReasonModificationLineBasketDetailModal.as_view(), name='CDNX_invoicing_reasonmodificationlinebaskets_sublist_details'),
    url(r'^reasonmodificationlinebaskets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', ReasonModificationLineBasketUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinebaskets_sublist_edit'),
    url(r'^reasonmodificationlinebaskets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', ReasonModificationLineBasketUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinebaskets_sublist_editmodal'),
    url(r'^reasonmodificationlinebaskets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', ReasonModificationLineBasketDelete.as_view(), name='CDNX_invoicing_reasonmodificationlinebaskets_sublist_delete'),


    url(r'^reasonmodificationlineorders$', ReasonModificationLineOrderList.as_view(), name='CDNX_invoicing_reasonmodificationlineorders_list'),
    url(r'^reasonmodificationlineorders/add$', ReasonModificationLineOrderCreate.as_view(), name='CDNX_invoicing_reasonmodificationlineorders_add'),
    url(r'^reasonmodificationlineorders/addmodal$', ReasonModificationLineOrderCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineorders_addmodal'),
    url(r'^reasonmodificationlineorders/(?P<pk>\w+)$', ReasonModificationLineOrderDetails.as_view(), name='CDNX_invoicing_reasonmodificationlineorders_details'),
    url(r'^reasonmodificationlineorders/(?P<pk>\w+)/edit$', ReasonModificationLineOrderUpdate.as_view(), name='CDNX_invoicing_reasonmodificationlineorders_edit'),
    url(r'^reasonmodificationlineorders/(?P<pk>\w+)/editmodal$', ReasonModificationLineOrderUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineorders_editmodal'),
    url(r'^reasonmodificationlineorders/(?P<pk>\w+)/delete$', ReasonModificationLineOrderDelete.as_view(), name='CDNX_invoicing_reasonmodificationlineorders_delete'),
    url(r'^reasonmodificationlineorders/(?P<pk>\w+)/sublist$', ReasonModificationLineOrderSubList.as_view(), name='CDNX_invoicing_reasonmodificationlineorders_sublist'),
    url(r'^reasonmodificationlineorders/(?P<pk>\w+)/sublist/add$', ReasonModificationLineOrderCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineorders_sublist_add'),
    url(r'^reasonmodificationlineorders/(?P<pk>\w+)/sublist/addmodal$', ReasonModificationLineOrderCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineorders_sublist_addmodal'),
    url(r'^reasonmodificationlineorders/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ReasonModificationLineOrderDetailModal.as_view(), name='CDNX_invoicing_reasonmodificationlineorders_sublist_details'),
    url(r'^reasonmodificationlineorders/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', ReasonModificationLineOrderUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineorders_sublist_edit'),
    url(r'^reasonmodificationlineorders/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', ReasonModificationLineOrderUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineorders_sublist_editmodal'),
    url(r'^reasonmodificationlineorders/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', ReasonModificationLineOrderDelete.as_view(), name='CDNX_invoicing_reasonmodificationlineorders_sublist_delete'),


    url(r'^reasonmodificationlinealbarans$', ReasonModificationLineAlbaranList.as_view(), name='CDNX_invoicing_reasonmodificationlinealbarans_list'),
    url(r'^reasonmodificationlinealbarans/add$', ReasonModificationLineAlbaranCreate.as_view(), name='CDNX_invoicing_reasonmodificationlinealbarans_add'),
    url(r'^reasonmodificationlinealbarans/addmodal$', ReasonModificationLineAlbaranCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinealbarans_addmodal'),
    url(r'^reasonmodificationlinealbarans/(?P<pk>\w+)$', ReasonModificationLineAlbaranDetails.as_view(), name='CDNX_invoicing_reasonmodificationlinealbarans_details'),
    url(r'^reasonmodificationlinealbarans/(?P<pk>\w+)/edit$', ReasonModificationLineAlbaranUpdate.as_view(), name='CDNX_invoicing_reasonmodificationlinealbarans_edit'),
    url(r'^reasonmodificationlinealbarans/(?P<pk>\w+)/editmodal$', ReasonModificationLineAlbaranUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinealbarans_editmodal'),
    url(r'^reasonmodificationlinealbarans/(?P<pk>\w+)/delete$', ReasonModificationLineAlbaranDelete.as_view(), name='CDNX_invoicing_reasonmodificationlinealbarans_delete'),
    url(r'^reasonmodificationlinealbarans/(?P<pk>\w+)/sublist$', ReasonModificationLineAlbaranSubList.as_view(), name='CDNX_invoicing_reasonmodificationlinealbarans_sublist'),
    url(r'^reasonmodificationlinealbarans/(?P<pk>\w+)/sublist/add$', ReasonModificationLineAlbaranCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinealbarans_sublist_add'),
    url(r'^reasonmodificationlinealbarans/(?P<pk>\w+)/sublist/addmodal$', ReasonModificationLineAlbaranCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinealbarans_sublist_addmodal'),
    url(r'^reasonmodificationlinealbarans/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ReasonModificationLineAlbaranDetailModal.as_view(), name='CDNX_invoicing_reasonmodificationlinealbarans_sublist_details'),
    url(r'^reasonmodificationlinealbarans/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', ReasonModificationLineAlbaranUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinealbarans_sublist_edit'),
    url(r'^reasonmodificationlinealbarans/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', ReasonModificationLineAlbaranUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinealbarans_sublist_editmodal'),
    url(r'^reasonmodificationlinealbarans/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', ReasonModificationLineAlbaranDelete.as_view(), name='CDNX_invoicing_reasonmodificationlinealbarans_sublist_delete'),


    url(r'^reasonmodificationlinetickets$', ReasonModificationLineTicketList.as_view(), name='CDNX_invoicing_reasonmodificationlinetickets_list'),
    url(r'^reasonmodificationlinetickets/add$', ReasonModificationLineTicketCreate.as_view(), name='CDNX_invoicing_reasonmodificationlinetickets_add'),
    url(r'^reasonmodificationlinetickets/addmodal$', ReasonModificationLineTicketCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinetickets_addmodal'),
    url(r'^reasonmodificationlinetickets/(?P<pk>\w+)$', ReasonModificationLineTicketDetails.as_view(), name='CDNX_invoicing_reasonmodificationlinetickets_details'),
    url(r'^reasonmodificationlinetickets/(?P<pk>\w+)/edit$', ReasonModificationLineTicketUpdate.as_view(), name='CDNX_invoicing_reasonmodificationlinetickets_edit'),
    url(r'^reasonmodificationlinetickets/(?P<pk>\w+)/editmodal$', ReasonModificationLineTicketUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinetickets_editmodal'),
    url(r'^reasonmodificationlinetickets/(?P<pk>\w+)/delete$', ReasonModificationLineTicketDelete.as_view(), name='CDNX_invoicing_reasonmodificationlinetickets_delete'),
    url(r'^reasonmodificationlinetickets/(?P<pk>\w+)/sublist$', ReasonModificationLineTicketSubList.as_view(), name='CDNX_invoicing_reasonmodificationlinetickets_sublist'),
    url(r'^reasonmodificationlinetickets/(?P<pk>\w+)/sublist/add$', ReasonModificationLineTicketCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinetickets_sublist_add'),
    url(r'^reasonmodificationlinetickets/(?P<pk>\w+)/sublist/addmodal$', ReasonModificationLineTicketCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinetickets_sublist_addmodal'),
    url(r'^reasonmodificationlinetickets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ReasonModificationLineTicketDetailModal.as_view(), name='CDNX_invoicing_reasonmodificationlinetickets_sublist_details'),
    url(r'^reasonmodificationlinetickets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', ReasonModificationLineTicketUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinetickets_sublist_edit'),
    url(r'^reasonmodificationlinetickets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', ReasonModificationLineTicketUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlinetickets_sublist_editmodal'),
    url(r'^reasonmodificationlinetickets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', ReasonModificationLineTicketDelete.as_view(), name='CDNX_invoicing_reasonmodificationlinetickets_sublist_delete'),


    url(r'^reasonmodificationlineticketrectifications$', ReasonModificationLineTicketRectificationList.as_view(), name='CDNX_invoicing_reasonmodificationlineticketrectifications_list'),
    url(r'^reasonmodificationlineticketrectifications/add$', ReasonModificationLineTicketRectificationCreate.as_view(), name='CDNX_invoicing_reasonmodificationlineticketrectifications_add'),
    url(r'^reasonmodificationlineticketrectifications/addmodal$', ReasonModificationLineTicketRectificationCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineticketrectifications_addmodal'),
    url(r'^reasonmodificationlineticketrectifications/(?P<pk>\w+)$', ReasonModificationLineTicketRectificationDetails.as_view(), name='CDNX_invoicing_reasonmodificationlineticketrectifications_details'),
    url(r'^reasonmodificationlineticketrectifications/(?P<pk>\w+)/edit$', ReasonModificationLineTicketRectificationUpdate.as_view(), name='CDNX_invoicing_reasonmodificationlineticketrectifications_edit'),
    url(r'^reasonmodificationlineticketrectifications/(?P<pk>\w+)/editmodal$', ReasonModificationLineTicketRectificationUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineticketrectifications_editmodal'),
    url(r'^reasonmodificationlineticketrectifications/(?P<pk>\w+)/delete$', ReasonModificationLineTicketRectificationDelete.as_view(), name='CDNX_invoicing_reasonmodificationlineticketrectifications_delete'),
    url(r'^reasonmodificationlineticketrectifications/(?P<pk>\w+)/sublist$', ReasonModificationLineTicketRectificationSubList.as_view(), name='CDNX_invoicing_reasonmodificationlineticketrectifications_sublist'),
    url(r'^reasonmodificationlineticketrectifications/(?P<pk>\w+)/sublist/add$', ReasonModificationLineTicketRectificationCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineticketrectifications_sublist_add'),
    url(r'^reasonmodificationlineticketrectifications/(?P<pk>\w+)/sublist/addmodal$', ReasonModificationLineTicketRectificationCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineticketrectifications_sublist_addmodal'),
    url(r'^reasonmodificationlineticketrectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ReasonModificationLineTicketRectificationDetailModal.as_view(), name='CDNX_invoicing_reasonmodificationlineticketrectifications_sublist_details'),
    url(r'^reasonmodificationlineticketrectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', ReasonModificationLineTicketRectificationUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineticketrectifications_sublist_edit'),
    url(r'^reasonmodificationlineticketrectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', ReasonModificationLineTicketRectificationUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineticketrectifications_sublist_editmodal'),
    url(r'^reasonmodificationlineticketrectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', ReasonModificationLineTicketRectificationDelete.as_view(), name='CDNX_invoicing_reasonmodificationlineticketrectifications_sublist_delete'),


    url(r'^reasonmodificationlineinvoices$', ReasonModificationLineInvoiceList.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoices_list'),
    url(r'^reasonmodificationlineinvoices/add$', ReasonModificationLineInvoiceCreate.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoices_add'),
    url(r'^reasonmodificationlineinvoices/addmodal$', ReasonModificationLineInvoiceCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoices_addmodal'),
    url(r'^reasonmodificationlineinvoices/(?P<pk>\w+)$', ReasonModificationLineInvoiceDetails.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoices_details'),
    url(r'^reasonmodificationlineinvoices/(?P<pk>\w+)/edit$', ReasonModificationLineInvoiceUpdate.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoices_edit'),
    url(r'^reasonmodificationlineinvoices/(?P<pk>\w+)/editmodal$', ReasonModificationLineInvoiceUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoices_editmodal'),
    url(r'^reasonmodificationlineinvoices/(?P<pk>\w+)/delete$', ReasonModificationLineInvoiceDelete.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoices_delete'),
    url(r'^reasonmodificationlineinvoices/(?P<pk>\w+)/sublist$', ReasonModificationLineInvoiceSubList.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoices_sublist'),
    url(r'^reasonmodificationlineinvoices/(?P<pk>\w+)/sublist/add$', ReasonModificationLineInvoiceCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoices_sublist_add'),
    url(r'^reasonmodificationlineinvoices/(?P<pk>\w+)/sublist/addmodal$', ReasonModificationLineInvoiceCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoices_sublist_addmodal'),
    url(r'^reasonmodificationlineinvoices/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ReasonModificationLineInvoiceDetailModal.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoices_sublist_details'),
    url(r'^reasonmodificationlineinvoices/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', ReasonModificationLineInvoiceUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoices_sublist_edit'),
    url(r'^reasonmodificationlineinvoices/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', ReasonModificationLineInvoiceUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoices_sublist_editmodal'),
    url(r'^reasonmodificationlineinvoices/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', ReasonModificationLineInvoiceDelete.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoices_sublist_delete'),


    url(r'^reasonmodificationlineinvoicerectifications$', ReasonModificationLineInvoiceRectificationList.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoicerectifications_list'),
    url(r'^reasonmodificationlineinvoicerectifications/add$', ReasonModificationLineInvoiceRectificationCreate.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoicerectifications_add'),
    url(r'^reasonmodificationlineinvoicerectifications/addmodal$', ReasonModificationLineInvoiceRectificationCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoicerectifications_addmodal'),
    url(r'^reasonmodificationlineinvoicerectifications/(?P<pk>\w+)$', ReasonModificationLineInvoiceRectificationDetails.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoicerectifications_details'),
    url(r'^reasonmodificationlineinvoicerectifications/(?P<pk>\w+)/edit$', ReasonModificationLineInvoiceRectificationUpdate.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoicerectifications_edit'),
    url(r'^reasonmodificationlineinvoicerectifications/(?P<pk>\w+)/editmodal$', ReasonModificationLineInvoiceRectificationUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoicerectifications_editmodal'),
    url(r'^reasonmodificationlineinvoicerectifications/(?P<pk>\w+)/delete$', ReasonModificationLineInvoiceRectificationDelete.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoicerectifications_delete'),
    url(r'^reasonmodificationlineinvoicerectifications/(?P<pk>\w+)/sublist$', ReasonModificationLineInvoiceRectificationSubList.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoicerectifications_sublist'),
    url(r'^reasonmodificationlineinvoicerectifications/(?P<pk>\w+)/sublist/add$', ReasonModificationLineInvoiceRectificationCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoicerectifications_sublist_add'),
    url(r'^reasonmodificationlineinvoicerectifications/(?P<pk>\w+)/sublist/addmodal$', ReasonModificationLineInvoiceRectificationCreateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoicerectifications_sublist_addmodal'),
    url(r'^reasonmodificationlineinvoicerectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ReasonModificationLineInvoiceRectificationDetailModal.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoicerectifications_sublist_details'),
    url(r'^reasonmodificationlineinvoicerectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', ReasonModificationLineInvoiceRectificationUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoicerectifications_sublist_edit'),
    url(r'^reasonmodificationlineinvoicerectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', ReasonModificationLineInvoiceRectificationUpdateModal.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoicerectifications_sublist_editmodal'),
    url(r'^reasonmodificationlineinvoicerectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', ReasonModificationLineInvoiceRectificationDelete.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoicerectifications_sublist_delete'),

    url(r'^printcounterdocumentbaskets/(?P<pk>\w+)/sublist$', PrintCounterDocumentBasketSublist.as_view(), name='CDNX_invoicing_printcounterdocumentbaskets_sublist'),
    url(r'^printcounterdocumentorders/(?P<pk>\w+)/sublist$', PrintCounterDocumentOrderSublist.as_view(), name='CDNX_invoicing_printcounterdocumentorders_sublist'),
    url(r'^printcounterdocumentalbarans/(?P<pk>\w+)/sublist$', PrintCounterDocumentAlbaranSublist.as_view(), name='CDNX_invoicing_printcounterdocumentalbarans_sublist'),
    url(r'^printcounterdocumenttickets/(?P<pk>\w+)/sublist$', PrintCounterDocumentTicketSublist.as_view(), name='CDNX_invoicing_printcounterdocumenttickets_sublist'),
    url(r'^printcounterdocumentticketrectifications/(?P<pk>\w+)/sublist$', PrintCounterDocumentTicketRectificationSublist.as_view(), name='CDNX_invoicing_printcounterdocumentticketrectifications_sublist'),
    url(r'^printcounterdocumentinvoices/(?P<pk>\w+)/sublist$', PrintCounterDocumentInvoiceSublist.as_view(), name='CDNX_invoicing_printcounterdocumentinvoices_sublist'),
    url(r'^printcounterdocumentinvoicerectifications/(?P<pk>\w+)/sublist$', PrintCounterDocumentInvoiceRectificationSublist.as_view(), name='CDNX_invoicing_printcounterdocumentinvoicerectifications_sublist'),

    url(r'^salesorderdocuments$', OrderDocumentList.as_view(), name='CDNX_invoicing_salesorderdocuments_list'),
    url(r'^salesorderdocuments/add$', OrderDocumentCreate.as_view(), name='CDNX_invoicing_salesorderdocuments_add'),
    url(r'^salesorderdocuments/addmodal$', OrderDocumentCreateModal.as_view(), name='CDNX_invoicing_salesorderdocuments_addmodal'),
    url(r'^salesorderdocuments/(?P<pk>\w+)$', OrderDocumentDetails.as_view(), name='CDNX_invoicing_salesorderdocuments_details'),
    url(r'^salesorderdocuments/(?P<pk>\w+)/edit$', OrderDocumentUpdate.as_view(), name='CDNX_invoicing_salesorderdocuments_edit'),
    url(r'^salesorderdocuments/(?P<pk>\w+)/editmodal$', OrderDocumentUpdateModal.as_view(), name='CDNX_invoicing_salesorderdocuments_editmodal'),
    url(r'^salesorderdocuments/(?P<pk>\w+)/delete$', OrderDocumentDelete.as_view(), name='CDNX_invoicing_salesorderdocuments_delete'),
    url(r'^salesorderdocuments/(?P<pk>\w+)/sublist$', OrderDocumentSubList.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist'),
    url(r'^salesorderdocuments/(?P<pk>\w+)/sublist/add$', OrderDocumentCreateModal.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist_add'),
    url(r'^salesorderdocuments/(?P<pk>\w+)/sublist/addmodal$', OrderDocumentCreateModal.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist_addmodal'),
    url(r'^salesorderdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', OrderDocumentDetailModal.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist_details'),
    url(r'^salesorderdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', OrderDocumentUpdateModal.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist_edit'),
    url(r'^salesorderdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', OrderDocumentUpdateModal.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist_editmodal'),
    url(r'^salesorderdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', OrderDocumentDelete.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist_delete'),

]
