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
from codenerix_invoicing.views_sales import AlbaranCreate, AlbaranCreateModal, AlbaranDelete, AlbaranList, AlbaranUpdate, AlbaranUpdateModal, \
    CustomerCreate, CustomerCreateModal, CustomerDelete, CustomerList, CustomerUpdate, CustomerUpdateModal, CustomerDetails,  \
    InvoiceRectificationCreate, InvoiceRectificationCreateModal, InvoiceRectificationDelete, InvoiceRectificationList, InvoiceRectificationUpdate, InvoiceRectificationUpdateModal, InvoiceRectificationDetails, InvoiceRectificationPrint,  \
    InvoiceCreate, InvoiceCreateModal, InvoiceDelete, InvoiceList, InvoiceUpdate, InvoiceUpdateModal, InvoicePrint,  \
    LineAlbaranCreate, LineAlbaranCreateModal, LineAlbaranDelete, LineAlbaranList, LineAlbaranUpdate, LineAlbaranUpdateModal, \
    LineInvoiceRectificationCreate, LineInvoiceRectificationCreateModal, LineInvoiceRectificationDelete, LineInvoiceRectificationList, LineInvoiceRectificationUpdate, LineInvoiceRectificationUpdateModal, LineInvoiceRectificationSubList, LineInvoiceRectificationDetailModal, \
    LineInvoiceCreate, LineInvoiceCreateModal, LineInvoiceDelete, LineInvoiceList, LineInvoiceUpdate, LineInvoiceUpdateModal, \
    LineOrderCreateModal, LineOrderDelete, LineOrderDetailsModal, LineOrderList, LineOrderSubList, LineOrderUpdateModal, \
    LineTicketRectificationCreate, LineTicketRectificationCreateModal, LineTicketRectificationDelete, LineTicketRectificationList, LineTicketRectificationUpdate, LineTicketRectificationUpdateModal, LineTicketRectificationSubList, LineTicketRectificationDetailModal,  \
    LineTicketCreate, LineTicketCreateModal, LineTicketDelete, LineTicketList, LineTicketUpdate, LineTicketUpdateModal, \
    OrderCreate, OrderCreateModal, OrderDelete, OrderDetails, OrderList, OrderUpdate, OrderUpdateModal, OrderPrint, \
    TicketRectificationCreate, TicketRectificationCreateModal, TicketRectificationDelete, TicketRectificationList, TicketRectificationUpdate, TicketRectificationUpdateModal, TicketRectificationDetails, \
    TicketCreate, TicketCreateModal, TicketDelete, TicketList, TicketUpdate, TicketUpdateModal, \
    AlbaranDetails, LineAlbaranSubList, AlbaranPrint, LineAlbaranDetailsModal, \
    TicketDetails, LineTicketSubList, TicketPrint, LineTicketDetailsModal, \
    InvoiceDetails, InvoicePrint, LineInvoiceSubList, LineInvoiceDetailsModal, \
    OrderCreateAlbaran, OrderCreateTicket, OrderCreateInvoice,  \
    AlbaranCreateTicket, AlbaranCreateInvoice, \
    TicketCreateInvoice, \
    OrderForeign, LineOrderForeign, LineOrderForeignCustom, \
    InvoiceCreateRectification, LineInvoiceForeign, TicketCreateRectification, LineTicketForeign, TicketRectificationPrint, \
    CustomerDocumentSubList, CustomerDocumentCreateModal, CustomerDocumentDetailsModal, CustomerDocumentUpdateModal, CustomerDocumentDelete, \
    ReservedProductList, ReservedProductCreate, ReservedProductUpdate, ReservedProductDelete, \
    BasketCreate, BasketCreateModal, BasketUpdate, BasketUpdateModal, BasketDetails, BasketDelete, \
    BasketListSHOPPINGCART, BasketDetailsSHOPPINGCART, BasketCreateSHOPPINGCART, BasketCreateSHOPPINGCARTModal, BasketUpdateSHOPPINGCART, BasketDeleteSHOPPINGCART, \
    BasketListBUDGET, BasketDetailsBUDGET, BasketCreateBUDGET, BasketCreateBUDGETModal, BasketUpdateBUDGET, BasketDeleteBUDGET, \
    BasketListWISHLIST, BasketDetailsWISHLIST, BasketCreateWISHLIST, BasketCreateWISHLISTModal, BasketUpdateWISHLIST, BasketDeleteWISHLIST, \
    BasketPassToBudget, \
    BasketPassToOrder, \
    LineBasketList, LineBasketCreate, LineBasketCreateModal, LineBasketUpdate, LineBasketUpdateModal, LineBasketDelete, LineBasketSubList, LineBasketDetails, LineBasketDetailModal, \
    ShoppingCartManagement, \
    CustomerForeignBudget, CustomerForeignShoppingCart, \
    BasketForeignShoppingCart, BasketForeignBudget, \
    OrderCreateModalFromBudget, OrderCreateModalFromShoppingCart


urlpatterns = [
    url(r'^customers$', CustomerList.as_view(), name='CDNX_invoicing_customers_list'),
    url(r'^customers/add$', CustomerCreate.as_view(), name='CDNX_invoicing_customers_add'),
    url(r'^customers/addmodal$', CustomerCreateModal.as_view(), name='CDNX_invoicing_customers_addmodal'),
    url(r'^customers/(?P<pk>\w+)$', CustomerDetails.as_view(), name='CDNX_invoicing_customers_detail'),
    url(r'^customers/(?P<pk>\w+)/edit$', CustomerUpdate.as_view(), name='CDNX_invoicing_customers_edit'),
    url(r'^customers/(?P<pk>\w+)/editmodal$', CustomerUpdateModal.as_view(), name='CDNX_invoicing_customers_editmodal'),
    url(r'^customers/(?P<pk>\w+)/delete$', CustomerDelete.as_view(), name='CDNX_invoicing_customers_delete'),

    url(r'^customers/foreign/(?P<search>[\w\W]+|\*)$', CustomerForeignBudget.as_view(), name='CDNX_invoicing_customers_foreign_from_budget'),
    url(r'^customers/foreign/(?P<search>[\w\W]+|\*)$', CustomerForeignShoppingCart.as_view(), name='CDNX_invoicing_customers_foreign_from_shoppingcart'),

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

    url(r'^linebaskets$', LineBasketList.as_view(), name='CDNX_invoicing_saleslinebaskets_list'),
    url(r'^linebaskets/add$', LineBasketCreate.as_view(), name='CDNX_invoicing_saleslinebaskets_add'),
    url(r'^linebaskets/addmodal$', LineBasketCreateModal.as_view(), name='CDNX_invoicing_saleslinebaskets_addmodal'),
    url(r'^linebaskets/(?P<pk>\w+)$', LineBasketDetails.as_view(), name='CDNX_invoicing_saleslinebaskets_details'),
    url(r'^linebaskets/(?P<pk>\w+)/edit$', LineBasketUpdate.as_view(), name='CDNX_invoicing_saleslinebaskets_edit'),
    url(r'^linebaskets/(?P<pk>\w+)/editmodal$', LineBasketUpdateModal.as_view(), name='CDNX_invoicing_saleslinebaskets_editmodal'),
    url(r'^linebaskets/(?P<pk>\w+)/delete$', LineBasketDelete.as_view(), name='CDNX_invoicing_saleslinebaskets_delete'),
    url(r'^linebaskets/(?P<pk>\w+)/sublist$', LineBasketSubList.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist'),
    url(r'^linebaskets/(?P<pk>\w+)/sublist/addmodal$', LineBasketCreateModal.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist_add'),
    url(r'^linebaskets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineBasketDetailModal.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist_details'),
    url(r'^linebaskets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineBasketUpdateModal.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist_details'),
    url(r'^linebaskets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineBasketDelete.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist_delete'),

]
