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
from .views_sales import CustomerCreate, CustomerCreateModal, CustomerDelete, CustomerList, CustomerUpdate, CustomerUpdateModal, CustomerDetails
from .views_sales import CustomerDocumentSubList, CustomerDocumentCreateModal, CustomerDocumentDetailsModal, CustomerDocumentUpdateModal, CustomerDocumentDelete
from .views_sales import CustomerForeignBudget, CustomerForeignShoppingCart

from .views_sales import BasketPassToOrder
from .views_sales import BasketPassToBudget
from .views_sales import BasketListSHOPPINGCART, BasketDetailsSHOPPINGCART, BasketCreateSHOPPINGCART, BasketCreateSHOPPINGCARTModal, BasketUpdateSHOPPINGCART, BasketDeleteSHOPPINGCART
from .views_sales import BasketListBUDGET, BasketDetailsBUDGET, BasketCreateBUDGET, BasketCreateBUDGETModal, BasketUpdateBUDGET, BasketDeleteBUDGET
from .views_sales import BasketListWISHLIST, BasketDetailsWISHLIST, BasketCreateWISHLIST, BasketCreateWISHLISTModal, BasketUpdateWISHLIST, BasketDeleteWISHLIST
from .views_sales import BasketForeignShoppingCart, BasketForeignBudget
from .views_sales import BasketPrintBUDGET

from .views_sales import BasketDetailsSHOPPINGCARTVending, LinesVending, LinesSubListBasketVending
from .views_sales import SalesLinesList, SalesLinesDetails

from .views_sales import OrderForeign
from .views_sales import OrderCreateAlbaran, OrderCreateTicket, OrderCreateInvoice, OrderStatus
from .views_sales import OrderCreate, OrderCreateModal, OrderDelete, OrderDetails, OrderList, OrderUpdate, OrderUpdateModal, OrderPrint
from .views_sales import OrderCreateModalFromBudget, OrderCreateModalFromShoppingCart

from .views_sales import OrderDocumentSubList, OrderDocumentCreateModal, OrderDocumentUpdateModal, OrderDocumentDelete

from .views_sales import AlbaranCreate, AlbaranCreateModal, AlbaranDelete, AlbaranList, AlbaranUpdate, AlbaranUpdateModal
from .views_sales import AlbaranDetails, AlbaranPrint, AlbaranSend
from .views_sales import AlbaranCreateTicket, AlbaranCreateInvoice

from .views_sales import InvoiceCreate, InvoiceCreateModal, InvoiceDelete, InvoiceList, InvoiceUpdate, InvoiceUpdateModal, InvoicePrint
from .views_sales import InvoiceDetails
from .views_sales import InvoiceCreateRectification, InvoiceCreateRectificationUnity
from .views_sales import InvoiceRectificationCreate, InvoiceRectificationCreateModal, InvoiceRectificationDelete, InvoiceRectificationList, InvoiceRectificationUpdate, InvoiceRectificationUpdateModal, InvoiceRectificationDetails, InvoiceRectificationPrint

from .views_sales import TicketCreate, TicketCreateModal, TicketDelete, TicketList, TicketUpdate, TicketUpdateModal
from .views_sales import TicketDetails, TicketPrint
from .views_sales import TicketCreateInvoice, TicketCreateRectification
from .views_sales import TicketRectificationCreate, TicketRectificationCreateModal, TicketRectificationDelete, TicketRectificationList, TicketRectificationUpdate, TicketRectificationUpdateModal, TicketRectificationDetails, TicketRectificationPrint


from .views_sales import PrintCounterDocumentBasketSublist, PrintCounterDocumentOrderSublist, PrintCounterDocumentAlbaranSublist, PrintCounterDocumentTicketSublist, PrintCounterDocumentTicketRectificationSublist, PrintCounterDocumentInvoiceSublist, PrintCounterDocumentInvoiceRectificationSublist

from .views_sales import LinesSubListBasket, LinesCreateModalBasket, LinesUpdateModalBasket
from .views_sales import LinesSubListOrder, LinesDetailModalOrder, LinesUpdateModalOrder
from .views_sales import LinesSubListAlbaran, LinesUpdateModalAlbaran
from .views_sales import LinesSubListInvoice, LinesUpdateModalInvoice, LinesDetailModalInvoice
from .views_sales import LinesSubListInvoiceRectification, LinesUpdateModalInvoiceRectification
from .views_sales import LinesSubListTicket, LinesUpdateModalTicket
from .views_sales import LinesSubListTicketRectification, LinesUpdateModalTicketRectification

from .views_reason import ReasonModificationList, ReasonModificationCreate, ReasonModificationCreateModal, ReasonModificationUpdate, ReasonModificationUpdateModal, ReasonModificationDelete, ReasonModificationSubList, ReasonModificationDetails, ReasonModificationDetailModal

from .views_reason import ReasonModificationLineTicketSubList, ReasonModificationLineTicketDetailModal
from .views_reason import ReasonModificationLineBasketSubList, ReasonModificationLineBasketDetailModal
from .views_reason import ReasonModificationLineOrderSubList, ReasonModificationLineOrderDetailModal
from .views_reason import ReasonModificationLineAlbaranSubList, ReasonModificationLineAlbaranDetailModal
from .views_reason import ReasonModificationLineTicketRectificationSubList, ReasonModificationLineTicketRectificationDetailModal
from .views_reason import ReasonModificationLineInvoiceSubList, ReasonModificationLineInvoiceDetailModal
from .views_reason import ReasonModificationLineInvoiceRectificationSubList, ReasonModificationLineInvoiceRectificationDetailModal
"""
  # , LinesDetailModalBasket, LinesDeleteBasket, LinesForeignBasket
from .views_sales import LineAlbaranCreate, LineAlbaranCreateModal, LineAlbaranDelete, LineAlbaranList, LineAlbaranUpdate, LineAlbaranUpdateModal
from .views_sales import LineInvoiceRectificationCreate, LineInvoiceRectificationCreateModal, LineInvoiceRectificationDelete, LineInvoiceRectificationList, LineInvoiceRectificationUpdate, LineInvoiceRectificationUpdateModal, LineInvoiceRectificationSubList, LineInvoiceRectificationDetailModal
from .views_sales import LineOrderCreateModal, LineOrderDelete, LineOrderDetailsModal, LineOrderList, LineOrderSubList, LineOrderUpdateModal
from .views_sales import LineInvoiceCreate, LineInvoiceCreateModal, LineInvoiceDelete, LineInvoiceList, LineInvoiceUpdate, LineInvoiceUpdateModal
from .views_sales import LineTicketRectificationCreate, LineTicketRectificationCreateModal, LineTicketRectificationDelete, LineTicketRectificationList, LineTicketRectificationUpdate, LineTicketRectificationUpdateModal, LineTicketRectificationSubList, LineTicketRectificationDetailModal
from .views_sales import LineTicketCreate, LineTicketCreateModal, LineTicketDelete, LineTicketList, LineTicketUpdate, LineTicketUpdateModal
, LineAlbaranDetailsModal, LineAlbaranSubList
, LineTicketSubList, LineTicketDetailsModal
, LineInvoiceSubList, LineInvoiceDetailsModal
, LineOrderForeign, LineOrderForeignCustom
, LineInvoiceForeign, LineTicketForeign

from .views_sales import LineBasketList, LineBasketCreate, LineBasketCreateModal, LineBasketUpdate, LineBasketUpdateModal, LineBasketDelete, LineBasketSubList, LineBasketDetails, LineBasketDetailModal, LineBasketForeign
from .views_sales import  LineBasketCreateModalPack

from .views_sales import ReservedProductList, ReservedProductCreate, ReservedProductUpdate, ReservedProductDelete
from .views_sales import BasketCreate, BasketCreateModal, BasketUpdate, BasketUpdateModal, BasketDetails, BasketDelete

from .views_sales import ShoppingCartManagement


from .views_sales import LineAlbaranForeign, LineTicketRectificationForeign, LineInvoiceRectificationForeign
from .views_sales import OrderDocumentList, OrderDocumentCreate, OrderDocumentUpdate,
, OrderDocumentDetails, OrderDocumentDetailModal
"""


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

    url(r'^shoppingcarts$', BasketListSHOPPINGCART.as_view(), name='CDNX_invoicing_salesbaskets_shoppingcart_list'),
    url(r'^budgets$', BasketListBUDGET.as_view(), name='CDNX_invoicing_salesbaskets_budget_list'),
    url(r'^wishlists$', BasketListWISHLIST.as_view(), name='CDNX_invoicing_salesbaskets_wishlist_list'),

    url(r'^shoppingcarts/add$', BasketCreateSHOPPINGCART.as_view(), name='CDNX_invoicing_salesbaskets_SHOPPINGCART_add'),
    url(r'^budgets/add$', BasketCreateBUDGET.as_view(), name='CDNX_invoicing_salesbaskets_BUDGET_add'),
    url(r'^wishlists/add$', BasketCreateWISHLIST.as_view(), name='CDNX_invoicing_salesbaskets_WISHLIST_add'),


    # ################
    # url(r'^salesliness$', SalesLinesList.as_view(), name='CDNX_invoicing_saleslines_list'),
    # url(r'^salesliness/(?P<pk>\w+)$', SalesLinesDetails.as_view(), name='CDNX_invoicing_saleslines_details'),
    # url(r'^vending$', LinesSubListBasketVending.as_view(), name='CDNX_invoicing_salesbaskets_shoppingcart_vending_list'),
    # url(r'^lines/(?P<pk>\w+)/vending$', LinesSubListBasketVending.as_view(), name='CDNX_invoicing_saleslines_sublist_vending'),
    # url(r'^shoppingcarts/vending$', LinesVending.as_view(), name='CDNX_invoicing_salesbaskets_shoppingcart_vending_list'),
    url(r'^vending$', LinesVending.as_view(), name='CDNX_invoicing_salesbaskets_SHOPPINGCART_vending_details'),
    url(r'^vending/(?P<bpk>\w+)$', LinesVending.as_view(), name='CDNX_invoicing_salesbaskets_shoppingcart_vending_list'),
    url(r'^vending/(?P<bpk>\w+)/(?P<pk>\w+)$', SalesLinesDetails.as_view(), name='CDNX_invoicing_saleslines_vending_details'),
    # url(r'^vending/(?P<bpk>\w+)/(?P<pk>\w+)$', LinesVending.as_view(), name='CDNX_invoicing_salesbaskets_SHOPPINGCART_vending_details'),
    # url(r'^shoppingcarts/vending/(?P<pk>\w+)$', BasketDetailsSHOPPINGCARTVending.as_view(), name='CDNX_invoicing_salesbaskets_SHOPPINGCART_vending_details'),
    # ################
    # url(r'^lines/(?P<pk>\w+)/vending/addmodal$', LinesCreateModalBasket.as_view(), name='CDNX_invoicing_saleslines_sublist_addmodal_vending'),
    # url(r'^lines/(?P<cpk>\w+)/vending/(?P<pk>\w+)/editmodal$', LinesUpdateModalBasket.as_view(), name='CDNX_invoicing_saleslines_sublist_editmodal_vending'),


    url(r'^shoppingcarts/(?P<pk>\w+)$', BasketDetailsSHOPPINGCART.as_view(), name='CDNX_invoicing_salesbaskets_SHOPPINGCART_details'),
    url(r'^budgets/(?P<pk>\w+)$', BasketDetailsBUDGET.as_view(), name='CDNX_invoicing_salesbaskets_BUDGET_details'),
    url(r'^wishlists/(?P<pk>\w+)$', BasketDetailsWISHLIST.as_view(), name='CDNX_invoicing_salesbaskets_WISHLIST_details'),

    url(r'^shoppingcarts/addmodal$', BasketCreateSHOPPINGCARTModal.as_view(), name='CDNX_invoicing_salesbaskets_SHOPPINGCART_addmodal'),
    url(r'^budgets/addmodal$', BasketCreateBUDGETModal.as_view(), name='CDNX_invoicing_salesbaskets_BUDGET_addmodal'),
    url(r'^wishlists/addmodal$', BasketCreateWISHLISTModal.as_view(), name='CDNX_invoicing_salesbaskets_WISHLIST_addmodal'),

    url(r'^shoppingcarts/(?P<pk>\w+)/edit$', BasketUpdateSHOPPINGCART.as_view(), name='CDNX_invoicing_salesbaskets_SHOPPINGCART_edit'),
    url(r'^budgets/(?P<pk>\w+)/edit$', BasketUpdateBUDGET.as_view(), name='CDNX_invoicing_salesbaskets_BUDGET_edit'),
    url(r'^wishlists/(?P<pk>\w+)/edit$', BasketUpdateWISHLIST.as_view(), name='CDNX_invoicing_salesbaskets_WISHLIST_edit'),

    url(r'^shoppingcarts/(?P<pk>\w+)/delete$', BasketDeleteSHOPPINGCART.as_view(), name='CDNX_invoicing_salesbaskets_SHOPPINGCART_delete'),
    url(r'^budgets/(?P<pk>\w+)/delete$', BasketDeleteBUDGET.as_view(), name='CDNX_invoicing_salesbaskets_BUDGET_delete'),
    url(r'^wishlists/(?P<pk>\w+)/delete$', BasketDeleteWISHLIST.as_view(), name='CDNX_invoicing_salesbaskets_WISHLIST_delete'),

    url(r'^shoppingcarts/(?P<pk>\w+)/createbudget$', BasketPassToBudget.as_view(), name='CDNX_invoicing_salesbaskets_createbudget'),
    url(r'^budgets/(?P<pk>\w+)/createorder$', BasketPassToOrder.as_view(), name='CDNX_invoicing_salesbaskets_createorder'),

    url(r'^shoppingcarts/foreign/(?P<search>[\w\W]+|\*)$', BasketForeignShoppingCart.as_view(), name='CDNX_invoicing_salesbaskets_foreignkey_shoppingcart'),
    url(r'^budgets/foreign/(?P<search>[\w\W]+|\*)$', BasketForeignBudget.as_view(), name='CDNX_invoicing_salesbaskets_foreignkey_budget'),

    url(r'^budgets/(?P<pk>\w+)/print$', BasketPrintBUDGET.as_view(), name='CDNX_invoicing_budgetsaless_print'),

    # ################
    url(r'^lines/(?P<pk>\w+)/basket_sublist$', LinesSubListBasket.as_view(), name='CDNX_invoicing_saleslines_sublist_basket'),
    url(r'^lines/(?P<pk>\w+)/basket_sublist/addmodal$', LinesCreateModalBasket.as_view(), name='CDNX_invoicing_saleslines_sublist_addmodal_basket'),
    url(r'^lines/(?P<cpk>\w+)/basket_sublist/(?P<pk>\w+)/editmodal$', LinesUpdateModalBasket.as_view(), name='CDNX_invoicing_saleslines_sublist_editmodal_basket'),
    # url(r'^lines/basket_foreign/(?P<search>[\w\W]+|\*)$', LinesForeignBasketOrder.as_view(), name='CDNX_invoicing_linessaless_foreign_for_order'),

    url(r'^lines/(?P<pk>\w+)/order_sublist$', LinesSubListOrder.as_view(), name='CDNX_invoicing_saleslines_sublist_order'),
    # url(r'^lines/(?P<pk>\w+)/order_sublist/addmodal$', LinesCreateModalOrder.as_view(), name='CDNX_invoicing_saleslines_sublist_addmodal_order'),
    url(r'^lines/(?P<cpk>\w+)/order_sublist/(?P<pk>\w+)/modal$', LinesDetailModalOrder.as_view(), name='CDNX_invoicing_saleslines_sublist_details_order'),
    url(r'^lines/(?P<cpk>\w+)/order_sublist/(?P<pk>\w+)/editmodal$', LinesUpdateModalOrder.as_view(), name='CDNX_invoicing_saleslines_sublist_editmodal_order'),

    url(r'^lines/(?P<pk>\w+)/albaran_sublist$', LinesSubListAlbaran.as_view(), name='CDNX_invoicing_saleslines_sublist_albaran'),
    url(r'^lines/(?P<cpk>\w+)/albaran_sublist/(?P<pk>\w+)/editmodal$', LinesUpdateModalAlbaran.as_view(), name='CDNX_invoicing_saleslines_sublist_editmodal_albaran'),

    url(r'^lines/(?P<pk>\w+)/invoice_sublist$', LinesSubListInvoice.as_view(), name='CDNX_invoicing_saleslines_sublist_invoice'),
    url(r'^lines/(?P<cpk>\w+)/invoice_sublist/(?P<pk>\w+)/modal$', LinesDetailModalInvoice.as_view(), name='CDNX_invoicing_saleslines_sublist_details_invoice'),
    url(r'^lines/(?P<cpk>\w+)/invoice_sublist/(?P<pk>\w+)/editmodal$', LinesUpdateModalInvoice.as_view(), name='CDNX_invoicing_saleslines_sublist_editmodal_invoice'),

    url(r'^lines/(?P<pk>\w+)/invoicerectification_sublist$', LinesSubListInvoiceRectification.as_view(), name='CDNX_invoicing_saleslines_sublist_invoicerectification'),
    url(r'^lines/(?P<cpk>\w+)/invoicerectification_sublist/(?P<pk>\w+)/editmodal$', LinesUpdateModalInvoiceRectification.as_view(), name='CDNX_invoicing_saleslines_sublist_editmodal_invoicerectification'),

    url(r'^lines/(?P<pk>\w+)/ticket_sublist$', LinesSubListTicket.as_view(), name='CDNX_invoicing_saleslines_sublist_ticket'),
    url(r'^lines/(?P<pk>\w+)/ticket_sublist$', LinesUpdateModalTicket.as_view(), name='CDNX_invoicing_saleslines_sublist_ticket'),

    url(r'^lines/(?P<pk>\w+)/ticketrectification_sublist$', LinesSubListTicketRectification.as_view(), name='CDNX_invoicing_saleslines_sublist_ticketrectificaction'),
    url(r'^lines/(?P<pk>\w+)/ticketrectification_sublist$', LinesUpdateModalTicketRectification.as_view(), name='CDNX_invoicing_saleslines_sublist_editmodal_ticketrectification'),

    # ###############
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

    url(r'^salesorderdocuments/(?P<pk>\w+)/sublist$', OrderDocumentSubList.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist'),
    url(r'^salesorderdocuments/(?P<pk>\w+)/sublist/addmodal$', OrderDocumentCreateModal.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist_addmodal'),
    url(r'^salesorderdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', OrderDocumentUpdateModal.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist_editmodal'),
    url(r'^salesorderdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', OrderDocumentDelete.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist_delete'),

    url(r'^printcounterdocumentbaskets/(?P<pk>\w+)/sublist$', PrintCounterDocumentBasketSublist.as_view(), name='CDNX_invoicing_printcounterdocumentbaskets_sublist'),
    url(r'^printcounterdocumentorders/(?P<pk>\w+)/sublist$', PrintCounterDocumentOrderSublist.as_view(), name='CDNX_invoicing_printcounterdocumentorders_sublist'),
    url(r'^printcounterdocumentalbarans/(?P<pk>\w+)/sublist$', PrintCounterDocumentAlbaranSublist.as_view(), name='CDNX_invoicing_printcounterdocumentalbarans_sublist'),
    url(r'^printcounterdocumenttickets/(?P<pk>\w+)/sublist$', PrintCounterDocumentTicketSublist.as_view(), name='CDNX_invoicing_printcounterdocumenttickets_sublist'),
    url(r'^printcounterdocumentticketrectifications/(?P<pk>\w+)/sublist$', PrintCounterDocumentTicketRectificationSublist.as_view(), name='CDNX_invoicing_printcounterdocumentticketrectifications_sublist'),
    url(r'^printcounterdocumentinvoices/(?P<pk>\w+)/sublist$', PrintCounterDocumentInvoiceSublist.as_view(), name='CDNX_invoicing_printcounterdocumentinvoices_sublist'),
    url(r'^printcounterdocumentinvoicerectifications/(?P<pk>\w+)/sublist$', PrintCounterDocumentInvoiceRectificationSublist.as_view(), name='CDNX_invoicing_printcounterdocumentinvoicerectifications_sublist'),

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
    url(r'^albarans/(?P<pk>\w+)/send$', AlbaranSend.as_view(), name='CDNX_invoicing_albaransaless_send'),

    url(r'^invoices$', InvoiceList.as_view(), name='CDNX_invoicing_invoicesaless_list'),
    url(r'^invoices/add$', InvoiceCreate.as_view(), name='CDNX_invoicing_invoicesaless_add'),
    url(r'^invoices/addmodal$', InvoiceCreateModal.as_view(), name='CDNX_invoicing_invoicesaless_addmodal'),
    url(r'^invoices/(?P<pk>\w+)$', InvoiceDetails.as_view(), name='CDNX_invoicing_invoicesales_details'),
    url(r'^invoices/(?P<pk>\w+)/edit$', InvoiceUpdate.as_view(), name='CDNX_invoicing_invoicesaless_edit'),
    url(r'^invoices/(?P<pk>\w+)/editmodal$', InvoiceUpdateModal.as_view(), name='CDNX_invoicing_invoicesaless_editmodal'),
    url(r'^invoices/(?P<pk>\w+)/delete$', InvoiceDelete.as_view(), name='CDNX_invoicing_invoicesaless_delete'),
    url(r'^invoices/(?P<pk>\w+)/createinvoicerectification$', InvoiceCreateRectification.as_view(), name='CDNX_invoicing_invoicesaless_create_rectification'),
    url(r'^invoices/(?P<pk>\w+)/print$', InvoicePrint.as_view(), name='CDNX_invoicing_invoicesaless_print'),
    url(r'^invoices/(?P<ipk>\w+)/createinvoicerectification/(?P<pk>\w+)$', InvoiceCreateRectificationUnity.as_view(), name='CDNX_invoicing_invoicesaless_create_rectification_unity'),

    url(r'^invoicerectifications$', InvoiceRectificationList.as_view(), name='CDNX_invoicing_invoicerectificationsaless_list'),
    url(r'^invoicerectifications/add$', InvoiceRectificationCreate.as_view(), name='CDNX_invoicing_invoicerectificationsaless_add'),
    url(r'^invoicerectifications/addmodal$', InvoiceRectificationCreateModal.as_view(), name='CDNX_invoicing_invoicerectificationsaless_addmodal'),
    url(r'^invoicerectifications/(?P<pk>\w+)$', InvoiceRectificationDetails.as_view(), name='CDNX_invoicing_invoicerectificationsaless_detail'),
    url(r'^invoicerectifications/(?P<pk>\w+)/edit$', InvoiceRectificationUpdate.as_view(), name='CDNX_invoicing_invoicerectificationsaless_edit'),
    url(r'^invoicerectifications/(?P<pk>\w+)/editmodal$', InvoiceRectificationUpdateModal.as_view(), name='CDNX_invoicing_invoicerectificationsaless_editmodal'),
    url(r'^invoicerectifications/(?P<pk>\w+)/delete$', InvoiceRectificationDelete.as_view(), name='CDNX_invoicing_invoicerectificationsaless_delete'),
    url(r'^invoicerectifications/(?P<pk>\w+)/print$', InvoiceRectificationPrint.as_view(), name='CDNX_invoicing_invoicerectificationsaless_print'),

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

    url(r'^ticketrectifications$', TicketRectificationList.as_view(), name='CDNX_invoicing_ticketrectificationsaless_list'),
    url(r'^ticketrectifications/add$', TicketRectificationCreate.as_view(), name='CDNX_invoicing_ticketrectificationsaless_add'),
    url(r'^ticketrectifications/addmodal$', TicketRectificationCreateModal.as_view(), name='CDNX_invoicing_ticketrectificationsaless_addmodal'),
    url(r'^ticketrectifications/(?P<pk>\w+)$', TicketRectificationDetails.as_view(), name='CDNX_invoicing_invoicesales_details'),
    url(r'^ticketrectifications/(?P<pk>\w+)/edit$', TicketRectificationUpdate.as_view(), name='CDNX_invoicing_ticketrectificationsaless_edit'),
    url(r'^ticketrectifications/(?P<pk>\w+)/editmodal$', TicketRectificationUpdateModal.as_view(), name='CDNX_invoicing_ticketrectificationsaless_editmodal'),
    url(r'^ticketrectifications/(?P<pk>\w+)/delete$', TicketRectificationDelete.as_view(), name='CDNX_invoicing_ticketrectificationsaless_delete'),
    url(r'^ticketrectifications/(?P<pk>\w+)/print$', TicketRectificationPrint.as_view(), name='CDNX_invoicing_ticketrectificationsaless_print'),

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

    # ####################

    url(r'^reasonmodificationlinebaskets/(?P<pk>\w+)/sublist$', ReasonModificationLineBasketSubList.as_view(), name='CDNX_invoicing_reasonmodificationlinebaskets_sublist'),
    url(r'^reasonmodificationlinebaskets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/modal$', ReasonModificationLineBasketDetailModal.as_view(), name='CDNX_invoicing_reasonmodificationlinebaskets_sublist_modal'),

    url(r'^reasonmodificationlineorders/(?P<pk>\w+)/sublist$', ReasonModificationLineOrderSubList.as_view(), name='CDNX_invoicing_reasonmodificationlineorders_sublist'),
    url(r'^reasonmodificationlineorders/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/modal$', ReasonModificationLineOrderDetailModal.as_view(), name='CDNX_invoicing_reasonmodificationlineorders_sublist_modal'),

    url(r'^reasonmodificationlinealbarans/(?P<pk>\w+)/sublist$', ReasonModificationLineAlbaranSubList.as_view(), name='CDNX_invoicing_reasonmodificationlinealbarans_sublist'),
    url(r'^reasonmodificationlinealbarans/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/modal$', ReasonModificationLineAlbaranDetailModal.as_view(), name='CDNX_invoicing_reasonmodificationlinealbarans_sublist_modal'),

    url(r'^reasonmodificationlinetickets/(?P<pk>\w+)/sublist$', ReasonModificationLineTicketSubList.as_view(), name='CDNX_invoicing_reasonmodificationlinetickets_sublist'),
    url(r'^reasonmodificationlinetickets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/modal$', ReasonModificationLineTicketDetailModal.as_view(), name='CDNX_invoicing_reasonmodificationlinetickets_sublist_modal'),

    url(r'^reasonmodificationlineticketrectifications/(?P<pk>\w+)/sublist$', ReasonModificationLineTicketRectificationSubList.as_view(), name='CDNX_invoicing_reasonmodificationlineticketrectifications_sublist'),
    url(r'^reasonmodificationlineticketrectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/modal$', ReasonModificationLineTicketRectificationDetailModal.as_view(), name='CDNX_invoicing_reasonmodificationlineticketrectifications_sublist_modal'),

    url(r'^reasonmodificationlineinvoices/(?P<pk>\w+)/sublist$', ReasonModificationLineInvoiceSubList.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoices_sublist'),
    url(r'^reasonmodificationlineinvoices/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ReasonModificationLineInvoiceDetailModal.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoices_sublist_modal'),

    url(r'^reasonmodificationlineinvoicerectifications/(?P<pk>\w+)/sublist$', ReasonModificationLineInvoiceRectificationSubList.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoicerectifications_sublist'),
    url(r'^reasonmodificationlineinvoicerectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/modal$', ReasonModificationLineInvoiceRectificationDetailModal.as_view(), name='CDNX_invoicing_reasonmodificationlineinvoicerectifications_sublist_modal'),

]
"""
    url(r'^reservedproducts$', ReservedProductList.as_view(), name='CDNX_invoicing_reservedproducts_list'),
    url(r'^reservedproducts/add$', ReservedProductCreate.as_view(), name='CDNX_invoicing_reservedproducts_add'),
    url(r'^reservedproducts/(?P<pk>\w+)/edit$', ReservedProductUpdate.as_view(), name='CDNX_invoicing_reservedproducts_edit'),
    url(r'^reservedproducts/(?P<pk>\w+)/delete$', ReservedProductDelete.as_view(), name='CDNX_invoicing_reservedproducts_delete'),

    # url(r'^shoppingcarts/management$', ShoppingCartManagement.as_view(), name='CDNX_invoicing_shoppingcarts_management'),



"""


"""
    url(r'^linebaskets$', LineBasketList.as_view(), name='CDNX_invoicing_saleslinebaskets_list'),
    url(r'^linebaskets/add$', LineBasketCreate.as_view(), name='CDNX_invoicing_saleslinebaskets_add'),
    url(r'^linebaskets/addmodal$', LineBasketCreateModal.as_view(), name='CDNX_invoicing_saleslinebaskets_addmodal'),
    url(r'^linebaskets/(?P<pk>\w+)$', LineBasketDetails.as_view(), name='CDNX_invoicing_saleslinebaskets_details'),
    url(r'^linebaskets/(?P<pk>\w+)/edit$', LineBasketUpdate.as_view(), name='CDNX_invoicing_saleslinebaskets_edit'),
    url(r'^linebaskets/(?P<pk>\w+)/editmodal$', LineBasketUpdateModal.as_view(), name='CDNX_invoicing_saleslinebaskets_editmodal'),
    url(r'^linebaskets/(?P<pk>\w+)/delete$', LineBasketDelete.as_view(), name='CDNX_invoicing_saleslinebaskets_delete'),
    url(r'^linebaskets/(?P<pk>\w+)/sublist$', LineBasketSubList.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist'),
    url(r'^linebaskets/(?P<pk>\w+)/sublist/addmodal$', LineBasketCreateModal.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist_add'),
    # url(r'^linebaskets/(?P<pk>\w+)/sublist/addpackmodal$', LineBasketCreateModalPack.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist_addpack'),
    url(r'^linebaskets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineBasketDetailModal.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist_details'),
    url(r'^linebaskets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineBasketUpdateModal.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist_details'),
    url(r'^linebaskets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineBasketDelete.as_view(), name='CDNX_invoicing_saleslinebaskets_sublist_delete'),
    url(r'^linebaskets/foreign/(?P<search>[\w\W]+|\*)$', LineBasketForeign.as_view(), name='CDNX_invoicing_linebasketsaless_foreign'),

    url(r'^salesorderdocuments$', OrderDocumentList.as_view(), name='CDNX_invoicing_salesorderdocuments_list'),
    url(r'^salesorderdocuments/add$', OrderDocumentCreate.as_view(), name='CDNX_invoicing_salesorderdocuments_add'),
    url(r'^salesorderdocuments/addmodal$', OrderDocumentCreateModal.as_view(), name='CDNX_invoicing_salesorderdocuments_addmodal'),
    url(r'^salesorderdocuments/(?P<pk>\w+)$', OrderDocumentDetails.as_view(), name='CDNX_invoicing_salesorderdocuments_details'),
    url(r'^salesorderdocuments/(?P<pk>\w+)/edit$', OrderDocumentUpdate.as_view(), name='CDNX_invoicing_salesorderdocuments_edit'),
    url(r'^salesorderdocuments/(?P<pk>\w+)/editmodal$', OrderDocumentUpdateModal.as_view(), name='CDNX_invoicing_salesorderdocuments_editmodal'),
    url(r'^salesorderdocuments/(?P<pk>\w+)/delete$', OrderDocumentDelete.as_view(), name='CDNX_invoicing_salesorderdocuments_delete'),

    url(r'^salesorderdocuments/(?P<pk>\w+)/sublist/add$', OrderDocumentCreateModal.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist_add'),
    url(r'^salesorderdocuments/(?P<pk>\w+)/sublist/addmodal$', OrderDocumentCreateModal.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist_addmodal'),
    url(r'^salesorderdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', OrderDocumentDetailModal.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist_details'),
    url(r'^salesorderdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', OrderDocumentUpdateModal.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist_edit'),
    url(r'^salesorderdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', OrderDocumentUpdateModal.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist_editmodal'),
    url(r'^salesorderdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', OrderDocumentDelete.as_view(), name='CDNX_invoicing_salesorderdocuments_sublist_delete'),


    url(r'^lineorders$', LineOrderList.as_view(), name='CDNX_invoicing_lineordersaless_list'),
    url(r'^lineorders/(?P<pk>\w+)/delete$', LineOrderDelete.as_view(), name='CDNX_invoicing_lineordersaless_delete'),
    url(r'^lineorders/(?P<pk>\w+)/sublist$', LineOrderSubList.as_view(), name='CDNX_invoicing_lineordersaless_sublist'),
    url(r'^lineorders/(?P<pk>\w+)/sublist/addmodal$', LineOrderCreateModal.as_view(), name='CDNX_invoicing_lineordersaless_sublist_add'),
    url(r'^lineorders/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineOrderDetailsModal.as_view(), name='CDNX_invoicing_lineordersaless_sublist_details'),
    url(r'^lineorders/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineOrderUpdateModal.as_view(), name='CDNX_invoicing_lineordersaless_sublist_details'),
    url(r'^lineorders/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineOrderDelete.as_view(), name='CDNX_invoicing_lineordersaless_sublist_delete'),
    url(r'^lineorders/foreign/(?P<search>[\w\W]+|\*)$', LineOrderForeign.as_view(), name='CDNX_invoicing_lineordersaless_foreign'),
    url(r'^lineorders/foreigncustom/(?P<search>[\w\W]+|\*)$', LineOrderForeignCustom.as_view(), name='CDNX_invoicing_lineordersaless_foreign_custom'),


    url(r'^linealbarans$', LineAlbaranList.as_view(), name='CDNX_invoicing_linealbaransaless_list'),
    url(r'^linealbarans/(?P<pk>\w+)/delete$', LineAlbaranDelete.as_view(), name='CDNX_invoicing_linealbaransaless_delete'),
    url(r'^linealbarans/(?P<pk>\w+)/sublist$', LineAlbaranSubList.as_view(), name='CDNX_invoicing_linealbaransaless_sublist'),
    url(r'^linealbarans/(?P<pk>\w+)/sublist/addmodal$', LineAlbaranCreateModal.as_view(), name='CDNX_invoicing_linealbaransaless_sublist_add'),
    url(r'^linealbarans/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineAlbaranDetailsModal.as_view(), name='CDNX_invoicing_linealbaransaless_sublist_details'),
    url(r'^linealbarans/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineAlbaranUpdateModal.as_view(), name='CDNX_invoicing_linealbaransaless_sublist_details'),
    url(r'^linealbarans/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineAlbaranDelete.as_view(), name='CDNX_invoicing_linealbaransaless_sublist_delete'),
    url(r'^linealbarans/foreign/(?P<search>[\w\W]+|\*)$', LineAlbaranForeign.as_view(), name='CDNX_invoicing_linealbaransaless_foreign'),


    url(r'^linetickets$', LineTicketList.as_view(), name='CDNX_invoicing_lineticketsaless_list'),
    url(r'^linetickets/(?P<pk>\w+)/delete$', LineTicketDelete.as_view(), name='CDNX_invoicing_lineticketsaless_delete'),
    url(r'^linetickets/(?P<pk>\w+)/sublist$', LineTicketSubList.as_view(), name='CDNX_invoicing_lineticketsaless_sublist'),
    url(r'^linetickets/(?P<pk>\w+)/sublist/addmodal$', LineTicketCreateModal.as_view(), name='CDNX_invoicing_lineticketsaless_sublist_add'),
    url(r'^linetickets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineTicketDetailsModal.as_view(), name='CDNX_invoicing_lineticketsaless_sublist_details'),
    url(r'^linetickets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineTicketUpdateModal.as_view(), name='CDNX_invoicing_lineticketsaless_sublist_details'),
    url(r'^linetickets/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineTicketDelete.as_view(), name='CDNX_invoicing_lineticketsaless_sublist_delete'),
    url(r'^linetickets/foreign/(?P<search>[\w\W]+|\*)$', LineTicketForeign.as_view(), name='CDNX_invoicing_lineticketsaless_foreign'),


    url(r'^lineticketrectifications/(?P<pk>\w+)/sublist$', LineTicketRectificationSubList.as_view(), name='CDNX_invoicing_lineticketrectificationsaless_sublist'),
    url(r'^lineticketrectifications/(?P<pk>\w+)/sublist/addmodal$', LineTicketRectificationCreateModal.as_view(), name='CDNX_invoicing_lineticketrectificationsaless_sublist_add'),
    url(r'^lineticketrectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineTicketRectificationDetailModal.as_view(), name='CDNX_invoicing_lineticketrectificationsaless_sublist_details'),
    url(r'^lineticketrectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineTicketRectificationUpdateModal.as_view(), name='CDNX_invoicing_lineticketrectificationsaless_sublist_details'),
    url(r'^lineticketrectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineTicketRectificationDelete.as_view(), name='CDNX_invoicing_lineticketrectificationsaless_sublist_delete'),
    url(r'^lineticketrectifications/foreign/(?P<search>[\w\W]+|\*)$', LineTicketRectificationForeign.as_view(), name='CDNX_invoicing_lineticketrectificationsaless_sublist_foreign'),


    url(r'^lineinvoices$', LineInvoiceList.as_view(), name='CDNX_invoicing_lineinvoicesaless_list'),
    url(r'^lineinvoices/(?P<pk>\w+)/delete$', LineInvoiceDelete.as_view(), name='CDNX_invoicing_lineinvoicesaless_delete'),
    url(r'^lineinvoices/(?P<pk>\w+)/sublist$', LineInvoiceSubList.as_view(), name='CDNX_invoicing_lineinvoicesaless_sublist'),
    url(r'^lineinvoices/(?P<pk>\w+)/sublist/addmodal$', LineInvoiceCreateModal.as_view(), name='CDNX_invoicing_lineinvoicesaless_sublist_add'),
    url(r'^lineinvoices/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineInvoiceDetailsModal.as_view(), name='CDNX_invoicing_lineinvoicesaless_sublist_details'),
    url(r'^lineinvoices/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineInvoiceUpdateModal.as_view(), name='CDNX_invoicing_lineinvoicesaless_sublist_details'),
    url(r'^lineinvoices/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineInvoiceDelete.as_view(), name='CDNX_invoicing_lineinvoicesaless_sublist_delete'),
    url(r'^lineinvoices/foreign/(?P<search>[\w\W]+|\*)$', LineInvoiceForeign.as_view(), name='CDNX_invoicing_lineinvoicessaless_foreign'),

    url(r'^lineinvoicerectifications/(?P<pk>\w+)/sublist$', LineInvoiceRectificationSubList.as_view(), name='CDNX_invoicing_lineinvoicerectificationsaless_sublist'),
    url(r'^lineinvoicerectifications/(?P<pk>\w+)/sublist/addmodal$', LineInvoiceRectificationCreateModal.as_view(), name='CDNX_invoicing_lineinvoicerectificationsaless_sublist_add'),
    url(r'^lineinvoicerectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', LineInvoiceRectificationDetailModal.as_view(), name='CDNX_invoicing_lineinvoicerectificationsaless_sublist_details'),
    url(r'^lineinvoicerectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', LineInvoiceRectificationUpdateModal.as_view(), name='CDNX_invoicing_lineinvoicerectificationsaless_sublist_details'),
    url(r'^lineinvoicerectifications/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', LineInvoiceRectificationDelete.as_view(), name='CDNX_invoicing_lineinvoicerectificationsaless_sublist_delete'),
    url(r'^lineinvoicerectifications/foreign/(?P<search>[\w\W]+|\*)$', LineInvoiceRectificationForeign.as_view(), name='CDNX_invoicing_lineinvoicerectificationsaless_sublist_foreign'),



    # url(r'^lines$', LinesList.as_view(), name='CDNX_invoicing_saleslines_list'),
    # url(r'^lines/add$', LinesCreate.as_view(), name='CDNX_invoicing_saleslines_add'),
    # url(r'^lines/addmodal$', LinesCreateModal.as_view(), name='CDNX_invoicing_saleslines_addmodal'),
    # url(r'^lines/(?P<pk>\w+)$', LinesDetails.as_view(), name='CDNX_invoicing_saleslines_details'),
    # url(r'^lines/(?P<pk>\w+)/edit$', LinesUpdate.as_view(), name='CDNX_invoicing_saleslines_edit'),
    # url(r'^lines/(?P<pk>\w+)/editmodal$', LinesUpdateModal.as_view(), name='CDNX_invoicing_saleslines_editmodal'),
    # url(r'^lines/(?P<pk>\w+)/delete$', LinesDelete.as_view(), name='CDNX_invoicing_saleslines_delete'),
    # url(r'^lines/(?P<pk>\w+)/sublist/addpackmodal$', LinesCreateModalPack.as_view(), name='CDNX_invoicing_saleslines_sublist_addpack'),
    # url(r'^lines/(?P<cpk>\w+)/basket_sublist/(?P<pk>\w+)$', LinesDetailModalBasket.as_view(), name='CDNX_invoicing_saleslines_sublist_details'),
    # url(r'^lines/(?P<cpk>\w+)/basket_sublist/(?P<pk>\w+)/delete$', LinesDeleteBasket.as_view(), name='CDNX_invoicing_saleslines_sublist_delete'),
    # url(r'^lines/foreign/(?P<search>[\w\W]+|\*)$', LinesForeignBasket.as_view(), name='CDNX_invoicing_linesaless_foreign'),
"""
