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

import ast
import datetime
import json
import pytz

from dateutil import tz
from decimal import Decimal, ROUND_HALF_UP


from django.db.models import Q, Sum
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import formats
from django.utils.translation import get_language
from django.forms.utils import ErrorList
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View

from django.conf import settings

from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail, GenDetailModal, GenForeignKey
from codenerix.middleware import get_current_user
from codenerix.widgets import DynamicInput

from codenerix_corporate.models import CorporateImage
from codenerix_extensions.views import GenCreateBridge, GenUpdateBridge
from codenerix_extensions.files.views import DocumentFileView
# from codenerix_extensions.helpers import get_language_database
from codenerix_products.models import ProductFinal

from codenerix_invoicing.models_sales import Customer, CustomerDocument
# from codenerix_invoicing.models_sales import SalesReservedProduct
from codenerix_invoicing.models_sales import SalesBasket, SalesOrder, SalesAlbaran, SalesTicket, SalesTicketRectification, SalesInvoice, SalesInvoiceRectification
from codenerix_invoicing.models_sales import SalesOrderDocument
from codenerix_invoicing.models_sales import SalesLines

from codenerix_invoicing.models_sales import ROLE_BASKET_SHOPPINGCART, ROLE_BASKET_BUDGET, ROLE_BASKET_WISHLIST, STATUS_ORDER

# from codenerix_invoicing.forms_sales import ReservedProductForm
from codenerix_invoicing.forms_sales import CustomerForm, CustomerDocumentForm
from codenerix_invoicing.forms_sales import BasketForm
from codenerix_invoicing.forms_sales import OrderForm, OrderFromBudgetForm, OrderFromShoppingCartForm
from codenerix_invoicing.forms_sales import OrderDocumentForm, OrderDocumentSublistForm
from codenerix_invoicing.forms_sales import AlbaranForm
from codenerix_invoicing.forms_sales import InvoiceForm
from codenerix_invoicing.forms_sales import InvoiceRectificationForm, InvoiceRectificationUpdateForm
from codenerix_invoicing.forms_sales import TicketForm
from codenerix_invoicing.forms_sales import TicketRectificationForm, TicketRectificationUpdateForm
from codenerix_invoicing.views import PrinterHelper

from .models_sales import CURRENCY_DECIMAL_PLACES

from .models_sales import ReasonModification
# from .forms_reason import ReasonModificationForm

from codenerix_invoicing.models_sales import ReasonModificationLineBasket, ReasonModificationLineOrder, ReasonModificationLineAlbaran, ReasonModificationLineInvoice, ReasonModificationLineTicket, ReasonModificationLineTicketRectification
# , , , , , , , ReasonModificationLineInvoiceRectification
# , ReasonModificationLineBasketForm, ReasonModificationLineOrderForm, ReasonModificationLineAlbaranForm, ReasonModificationLineTicketForm, ReasonModificationLineTicketRectificationForm, ReasonModificationLineInvoiceForm, ReasonModificationLineInvoiceRectificationForm
from .forms_sales import LineOfBasketForm, LineOfBasketFormUpdate, LineOfOrderForm, LineOfAlbaranForm
from .forms_sales import LineOfInvoiceForm, LineOfInvoiceRectificationForm
from .models_sales import PrintCounterDocumentBasket, PrintCounterDocumentOrder, PrintCounterDocumentAlbaran, PrintCounterDocumentTicket, PrintCounterDocumentTicketRectification, PrintCounterDocumentInvoice, PrintCounterDocumentInvoiceRectification

from .helpers import ShoppingCartProxy
from codenerix_pos.helpers import get_POS

from .forms_sales import LineOfInvoiceRectificationUnityForm
from .exceptions import SalesLinesInsufficientStock, SalesLinesProductFinalIsSample, SalesLinesUniqueProductNotExists, SalesLinesNotModifiable

from .forms_sales import SalesLinesInLineForm


# ###########################################
class GenCustomerUrl(object):
    ws_entry_point = '{}/customers'.format(settings.CDNX_INVOICING_URL_SALES)


# Customer
class CustomerList(GenCustomerUrl, GenList):
    model = Customer
    show_details = True
    extra_context = {'menu': ['sales', 'Customer'], 'bread': [_('Sales'), _('Customer')]}
    default_ordering = "-created"


class CustomerCreate(GenCustomerUrl, GenCreate, GenCreateBridge):
    model = Customer
    form_class = CustomerForm
    show_details = True

    def form_valid(self, form):
        field = 'codenerix_external_field'
        model = Customer
        related_field = 'customer'
        error_message = [
            _("The selected entry is already a customer, select another entry!"),
            _("The selected entry is not available anymore, please, try again!")
        ]
        return self.form_valid_bridge(form, field, model, related_field, error_message)


class CustomerCreateModal(GenCreateModal, CustomerCreate):
    pass


class CustomerUpdate(GenCustomerUrl, GenUpdate, GenUpdateBridge):
    model = Customer
    form_class = CustomerForm

    def get_form(self, form_class=None):
        form = super(CustomerUpdate, self).get_form(form_class)
        # initial external field
        form.fields['codenerix_external_field'].initial = form.instance.external
        return form

    def form_valid(self, form):
        field = 'codenerix_external_field'
        model = Customer
        related_field = 'customer'
        error_message = [
            _("The selected entry is not available anymore, please, try again!")
        ]
        return self.form_valid_bridge(form, field, model, related_field, error_message)


class CustomerUpdateModal(GenUpdateModal, CustomerUpdate):
    pass


class CustomerDelete(GenCustomerUrl, GenDelete):
    model = Customer


class CustomerDetails(GenCustomerUrl, GenDetail):
    model = Customer
    groups = CustomerForm.__groups_details__()
    template_model = "sales/customer_details.html"
    tabs = [
        {'id': 'PersonAddresses', 'name': _('Person addresses'), 'ws': 'customer_personaddress_sublist', 'rows': 'base'},
        {'id': 'Documents', 'name': _('Documents'), 'ws': 'CDNX_invoicing_customerdocuments_sublist', 'rows': 'base'}
    ]
    exclude_fields = []


class CustomerForeignBudget(GenCustomerUrl, GenForeignKey):
    model = Customer
    label = "{external}"

    def get_foreign(self, queryset, search, filters):
        qs = queryset.filter(basket_sales__order_sales__isnull=True)
        qs = qs.filter(basket_sales__role=ROLE_BASKET_BUDGET)

        return qs.distinct()[:settings.LIMIT_FOREIGNKEY]


class CustomerForeignShoppingCart(GenCustomerUrl, GenForeignKey):
    model = Customer
    label = "{external}"

    def get_foreign(self, queryset, search, filters):
        qs = queryset.filter(basket_sales__order_sales__isnull=True)
        qs = qs.filter(basket_sales__role=ROLE_BASKET_SHOPPINGCART)

        return qs.distinct()[:settings.LIMIT_FOREIGNKEY]


# ###########################################
# CustomerDocument
class GenCustomerDocumentUrl(object):
    ws_entry_point = '{}/customerdocuments'.format(settings.CDNX_INVOICING_URL_SALES)


class CustomerDocumentSubList(GenCustomerDocumentUrl, GenList):
    model = CustomerDocument
    # show_details = False
    # json = False
    # template_model = "sales/customerdocument_sublist.html"
    # extra_context = {'menu': ['CustomerDocument', 'sales'], 'bread': [_('CustomerDocument'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(customer__pk=pk)
        return limit


class CustomerDocumentCreateModal(GenCustomerDocumentUrl, DocumentFileView, GenCreateModal, GenCreate):
    model = CustomerDocument
    form_class = CustomerDocumentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(CustomerDocumentCreateModal, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            customer = Customer.objects.get(pk=self.__pk)
            self.request.customer = customer
            form.instance.customer = customer

        return super(CustomerDocumentCreateModal, self).form_valid(form)


class CustomerDocumentDetailsModal(GenCustomerDocumentUrl, GenDetailModal, GenDetail):
    model = CustomerDocument
    form_class = CustomerDocumentForm.__groups_details__()


class CustomerDocumentUpdateModal(GenCustomerDocumentUrl, DocumentFileView, GenUpdateModal, GenUpdate):
    model = CustomerDocument
    form_class = CustomerDocumentForm


class CustomerDocumentDelete(GenCustomerDocumentUrl, GenDelete):
    model = CustomerDocument


# ###########################################
class GenBasketUrl(object):
    ws_entry_point = '{}/baskets'.format(settings.CDNX_INVOICING_URL_SALES)


class GenBasketSHOPPINGCARTUrl(object):
    ws_entry_point = '{}/shoppingcarts'.format(settings.CDNX_INVOICING_URL_SALES)


class GenBasketBUDGETUrl(object):
    ws_entry_point = '{}/budgets'.format(settings.CDNX_INVOICING_URL_SALES)


class GenBasketWISHLISTUrl(object):
    ws_entry_point = '{}/wishlists'.format(settings.CDNX_INVOICING_URL_SALES)


# SalesBasket
class BasketList(GenList):
    model = SalesBasket
    extra_context = {'menu': ['sales', 'SalesBasket'], 'bread': [_('Sales'), _('SalesBasket')]}
    show_details = True
    template_model = "sales/basket_list.html"
    form_ngcontroller = "codenerixSalesDetailsCtrl"
    default_ordering = "-created"


class BasketListSHOPPINGCART(GenBasketSHOPPINGCARTUrl, BasketList):
    def __limitQ__(self, info):
        limit = {}
        limit['role'] = Q(role=ROLE_BASKET_SHOPPINGCART)
        limit['removed'] = Q(removed=False)
        return limit


class BasketListBUDGET(GenBasketBUDGETUrl, BasketList):
    def __limitQ__(self, info):
        limit = {}
        limit['role'] = Q(role=ROLE_BASKET_BUDGET)
        limit['removed'] = Q(removed=False)
        return limit


class BasketListWISHLIST(GenBasketWISHLISTUrl, BasketList):
    def __limitQ__(self, info):
        limit = {}
        limit['role'] = Q(role=ROLE_BASKET_WISHLIST)
        limit['removed'] = Q(removed=False)
        return limit


class BasketDetails(GenBasketUrl, GenDetail):
    model = SalesBasket
    groups = BasketForm.__groups_details__()
    template_model = "sales/basket_details.html"
    exclude_fields = ['parent_pk', 'payment']
    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_saleslines_sublist_basket', 'rows': 'base'},
        {'id': 'line_reason', 'name': _('Lines modificed'), 'ws': 'CDNX_invoicing_reasonmodificationlinebaskets_sublist', 'rows': 'base'},
        {'id': 'line_printer', 'name': _('Print counter'), 'ws': 'CDNX_invoicing_printcounterdocumentbaskets_sublist', 'rows': 'base'},
    ]
    linkedit = False
    linkdelete = False

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = self.model.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            self.linkedit = True
            self.linkdelete = True

        return super(BasketDetails, self).dispatch(*args, **kwargs)


class BasketDetailsSHOPPINGCART(GenBasketSHOPPINGCARTUrl, BasketDetails):
    pass


class BasketDetailsBUDGET(GenBasketBUDGETUrl, BasketDetails):
    pass


class BasketDetailsWISHLIST(GenBasketWISHLISTUrl, BasketDetails):
    pass


class BasketCreate(GenBasketUrl, GenCreate):
    model = SalesBasket
    form_class = BasketForm
    show_details = True

    def get_form(self, form_class=None):
        info = get_POS(self.request)
        form = super(BasketCreate, self).get_form(form_class)
        initial = form.initial
        initial['pos'] = getattr(info['POS'], 'pk', None)
        return form


class BasketCreateModal(GenCreateModal, BasketCreate):
    pass


class BasketCreateSHOPPINGCART(GenBasketSHOPPINGCARTUrl, BasketCreate):
    def form_valid(self, form):
        self.request.role = ROLE_BASKET_SHOPPINGCART
        form.instance.role = ROLE_BASKET_SHOPPINGCART

        return super(BasketCreateSHOPPINGCART, self).form_valid(form)


class BasketCreateSHOPPINGCARTModal(GenCreateModal, BasketCreateSHOPPINGCART):
    pass


class BasketCreateBUDGET(GenBasketBUDGETUrl, BasketCreate):
    def form_valid(self, form):
        self.request.role = ROLE_BASKET_BUDGET
        form.instance.role = ROLE_BASKET_BUDGET

        return super(BasketCreateBUDGET, self).form_valid(form)


class BasketCreateBUDGETModal(GenCreateModal, BasketCreateBUDGET):
    pass


class BasketCreateWISHLIST(GenBasketWISHLISTUrl, BasketCreate):
    def form_valid(self, form):
        self.request.role = ROLE_BASKET_WISHLIST
        form.instance.role = ROLE_BASKET_WISHLIST

        return super(BasketCreateWISHLIST, self).form_valid(form)


class BasketCreateWISHLISTModal(GenCreateModal, BasketCreateWISHLIST):
    pass


class BasketUpdate(GenBasketUrl, GenUpdate):
    model = SalesBasket
    form_class = BasketForm
    show_details = True


class BasketUpdateModal(GenUpdateModal, BasketUpdate):
    pass


class BasketUpdateSHOPPINGCART(GenBasketSHOPPINGCARTUrl, BasketUpdate):
    pass


class BasketUpdateBasketUpdateSHOPPINGCARTModal(BasketUpdateSHOPPINGCART):
    pass


class BasketUpdateBUDGET(GenBasketBUDGETUrl, BasketUpdate):
    pass


class BasketUpdateBasketUpdateBUDGETModal(BasketUpdateBUDGET):
    pass


class BasketUpdateWISHLIST(GenBasketWISHLISTUrl, BasketUpdate):
    pass


class BasketUpdateBasketUpdateWISHLISTModal(BasketUpdateWISHLIST):
    pass


class BasketDelete(GenBasketUrl, GenDelete):
    model = SalesBasket


class BasketDeleteSHOPPINGCART(GenBasketSHOPPINGCARTUrl, GenDelete):
    model = SalesBasket


class BasketDeleteBUDGET(GenBasketBUDGETUrl, GenDelete):
    model = SalesBasket


class BasketDeleteWISHLIST(GenBasketWISHLISTUrl, GenDelete):
    model = SalesBasket


class BasketForeignBudget(GenBasketBUDGETUrl, GenForeignKey):
    model = SalesBasket
    label = "{code} {name}"

    def get_foreign(self, queryset, search, filters):
        qs = queryset.filter(order_sales__isnull=True)
        qs = qs.filter(role=ROLE_BASKET_BUDGET)

        qs.filter(customer=filters.get('customer', None))

        return qs[:settings.LIMIT_FOREIGNKEY]


class BasketForeignShoppingCart(GenBasketSHOPPINGCARTUrl, GenForeignKey):
    model = SalesBasket
    label = "{code} {name}"

    def get_foreign(self, queryset, search, filters):
        qs = queryset.exclude(order_sales__isnull=False)
        qs = qs.filter(role=ROLE_BASKET_SHOPPINGCART)

        qs.filter(customer=filters.get('customer', None))

        return qs[:settings.LIMIT_FOREIGNKEY]


class BasketPrint(PrinterHelper, GenBasketUrl, GenDetail):
    model = SalesBasket
    modelname = "list"
    template_model = 'sales/pdf/budget_pdf.html'
    output_filename = '{0}{1}{2}_budget'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(BasketPrint, self).get_context_data(**kwargs)

        budget = self.object
        budget.print_counter(get_current_user())

        # I take address for send.
        if hasattr(budget.customer.external, 'person_address'):
            send_address = budget.customer.external.person_address.filter(main=True).first()
        else:
            send_address = None

        context["budget"] = budget
        lines = []
        total_order = 0
        for line in budget.line_basket_sales.all():
            base = (line.price_base * line.quantity)
            subtotal = base + (base * line.tax / 100.0)
            total_order += subtotal
            lines.append({
                'code': line.code,
                'product': line.product,
                'price_base': line.price_base,
                'quantity': line.quantity,
                'tax': line.tax,
                'total': subtotal
            })
        if budget.address_invoice:
            context['address_invoice'] = {
                'address': budget.address_invoice.external_invoice.get_address(),
                'zipcode': budget.address_invoice.external_invoice.get_zipcode(),
                'city': budget.address_invoice.external_invoice.get_city(),
                'province': budget.address_invoice.external_invoice.get_province(),
                'country': budget.address_invoice.external_invoice.get_country(),
            }
        else:
            context['address_invoice'] = {}
        context['line_budget_sales'] = lines
        context['total_budget'] = budget.calculate_price_doc_complete(details=True)
        context['send_address'] = send_address
        context['media_root'] = settings.MEDIA_ROOT + "/"
        corporate_image = CorporateImage.objects.filter(public=True).first()
        context["corporate_image"] = corporate_image
        self.output_filename = "{0}".format(budget.date)

        # bloqueo del documento
        budget.lock = True
        budget.save()
        return context


class BasketPrintSHOPPINGCART(GenBasketSHOPPINGCARTUrl, BasketPrint):
    model = SalesBasket


class BasketPrintBUDGET(GenBasketBUDGETUrl, BasketPrint):
    model = SalesBasket


class BasketPrintWISHLIST(GenBasketWISHLISTUrl, BasketPrint):
    model = SalesBasket


class BasketPassToBudget(View):
    def get(self, request, *args, **kwargs):
        raise Exception("get")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = {}
        pk = kwargs.get('pk', None)
        list_lines = ast.literal_eval(request._body.decode())['lines']
        if pk:
            obj = SalesBasket.objects.filter(pk=pk).first()
            if obj:
                obj_budget = obj.pass_to_budget(list_lines)
                context['url'] = "{}#/{}".format(reverse("CDNX_invoicing_salesbaskets_budget_list"), obj_budget.pk)
                try:
                    json_answer = json.dumps(context)
                except TypeError:
                    raise TypeError("The structure can not be encoded to JSON: {}".format(context))
                return HttpResponse(json_answer, content_type='application/json')
            else:
                context['error'] = _("This is not basket")
        else:
            context['error'] = _("Params invalid")

        raise Exception("cambiar el role del basket y hacer que se redirija hacia el nuevo budget")


class BasketPassToOrder(View):
    def get(self, request, *args, **kwargs):
        raise Exception("get")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):

        # raise Exception("Adatar desde aqui")

        pk = kwargs.get('pk', None)
        list_lines = ast.literal_eval(request._body.decode())['lines']
        try:
            context = SalesLines.create_order_from_budget(pk, list_lines)
            if 'error' in context:
                context['error'] = str(context['error'])
        except SalesLinesProductFinalIsSample as e:
            context = {'error': str(e)}
        except SalesLinesUniqueProductNotExists as e:
            context = {'error': str(e)}
        except SalesLinesInsufficientStock as e:
            context = {'error': str(e)}
        except SalesLinesNotModifiable as e:
            context = {'error': str(e)}

        if 'obj_final' in context:
            context.pop('obj_final')
        try:
            json_answer = json.dumps(context)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON: {}".format(context))
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


# ###########################################
class GenOrderUrl(object):
    ws_entry_point = '{}/orders'.format(settings.CDNX_INVOICING_URL_SALES)


# Order
class OrderList(GenOrderUrl, GenList):
    model = SalesOrder
    template_model = "sales/order_list.html"
    show_details = True
    linkadd = False
    extra_context = {'menu': ['sales', 'sales_order'], 'bread': [_('Sales'), _('Sales orders')]}
    ngincludes = {"table": "/static/codenerix_invoicing/partials/sales/table_order.html"}
    default_ordering = "-created"
    gentrans = {
        'CreateFromBudget': _("Create order from budget"),
        'CreateFromShoppingCart': _("Create order from shopping cart"),
    }
    static_partial_row = "codenerix_invoicing/partials/sales/salesorder_rows.html"

    def __init__(self, *args, **kwargs):
        new = {}
        last = None
        for (key, trans) in STATUS_ORDER:
            if last:
                new[last] = str(trans)
                last = key
            else:
                last = key
        new[key] = None
        self.gentrans['status_order_next'] = new
        return super(OrderList, self).__init__(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        limit['removed'] = Q(removed=False)
        return limit


class OrderCreate(GenOrderUrl, GenCreate):
    model = SalesOrder
    form_class = OrderForm
    show_details = True


class OrderCreateModal(GenCreateModal, OrderCreate):
    pass


class OrderCreateModalFromBudget(GenCreateModal, OrderCreate):
    form_class = OrderFromBudgetForm
    hide_foreignkey_button = True

    def form_valid(self, form):
        r = super(OrderCreateModalFromBudget, self).form_valid(form)
        if SalesLines.create_order_from_budget_all(self.object):
            return r
        else:
            self.object.delete()
            errors = form._errors.setdefault("budget", ErrorList())
            errors.append(_("Hubo un error al crear el pedido, reintentelo de nuevo"))
            return super(OrderCreateModalFromBudget, self).form_invalid(form)


class OrderCreateModalFromShoppingCart(GenCreateModal, OrderCreate):
    form_class = OrderFromShoppingCartForm
    hide_foreignkey_button = True

    def form_valid(self, form):
        r = super(OrderCreateModalFromShoppingCart, self).form_valid(form)
        if SalesLines.create_order_from_budget_all(self.object):
            return r
        else:
            self.object.delete()
            errors = form._errors.setdefault("budget", ErrorList())
            errors.append(_("Hubo un error al crear el pedido, reintentelo de nuevo"))
            return super(OrderCreateModalFromShoppingCart, self).form_invalid(form)


class OrderUpdate(GenOrderUrl, GenUpdate):
    model = SalesOrder
    show_details = True
    form_class = OrderForm


class OrderUpdateModal(GenUpdateModal, OrderUpdate):
    pass


class OrderDelete(GenOrderUrl, GenDelete):
    model = SalesOrder


class OrderDetails(GenOrderUrl, GenDetail):
    model = SalesOrder
    groups = OrderForm.__groups_details__()
    template_model = "sales/order_details.html"
    exclude_fields = ['parent_pk']
    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_saleslines_sublist_order', 'rows': 'base'},
        {'id': 'documents', 'name': _('Documents'), 'ws': 'CDNX_invoicing_salesorderdocuments_sublist', 'rows': 'base'},
        {'id': 'line_reason', 'name': _('Lines modificed'), 'ws': 'CDNX_invoicing_reasonmodificationlineorders_sublist', 'rows': 'base'},
        {'id': 'line_printer', 'name': _('Print counter'), 'ws': 'CDNX_invoicing_printcounterdocumentorders_sublist', 'rows': 'base'},
    ]
    linkedit = False
    linkdelete = False

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = self.model.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            self.linkedit = True
            self.linkdelete = True

        return super(OrderDetails, self).dispatch(*args, **kwargs)


class OrderStatus(View):

    def get(self, request, *args, **kwargs):
        raise Exception("get")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        action = kwargs.get('action', None)

        answer = {'changed': False}
        if action in ['next', 'previous']:
            so = SalesOrder.objects.get(pk=pk)
            first = None
            last = None
            for (key, label) in STATUS_ORDER:
                if not first:
                    first = key
                elif so.status_order == last:
                    so.status_order = key
                    so.save()
                    answer['changed'] = True
                    break
                last = key
        else:
            answer['error'] = True
            answer['errortxt'] = _("Action not allowed here!")

        # Return the new context
        return JsonResponse(answer)


class OrderPrint(PrinterHelper, GenOrderUrl, GenDetail):
    model = SalesOrder
    modelname = "list"
    template_model = 'sales/pdf/order_pdf.html'
    output_filename = '{0}{1}{2}_order'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(OrderPrint, self).get_context_data(**kwargs)

        order = self.object
        order.print_counter(get_current_user())

        # I take address for send.
        if hasattr(order.customer.external, 'person_address'):
            send_address = order.customer.external.person_address.filter(main=True).first()
        else:
            send_address = None

        context["order"] = order
        lines = []
        for line in order.line_order_sales.all():
            lines.append({
                'code': line.code,
                'product': line.product,
                'price_base': line.price_base,
                'quantity': line.quantity,
                'tax': line.tax,
                'total': line.subtotal
            })
        if order.budget and order.budget.address_invoice:
            context['address_invoice'] = {
                'address': order.budget.address_invoice.external_invoice.get_address(),
                'zipcode': order.budget.address_invoice.external_invoice.get_zipcode(),
                'city': order.budget.address_invoice.external_invoice.get_city(),
                'province': order.budget.address_invoice.external_invoice.get_province(),
                'country': order.budget.address_invoice.external_invoice.get_country(),
            }
        else:
            context['address_invoice'] = {}

        context['line_order_sales'] = lines
        context['total_order'] = order.calculate_price_doc_complete(details=True)
        context['send_address'] = send_address
        context['media_root'] = settings.MEDIA_ROOT + "/"
        corporate_image = CorporateImage.objects.filter(public=True).first()
        context["corporate_image"] = corporate_image
        self.output_filename = "{0}".format(order.date)

        # bloqueo del documento
        order.lock = True
        order.save()
        return context


class OrderCreateAlbaran(View):

    def get(self, request, *args, **kwargs):
        raise Exception("GET method not supported!")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        list_lines = ast.literal_eval(request._body.decode())['lines']
        context = SalesLines.create_albaran_from_order(pk, list_lines)
        if 'obj_final' in context:
            context.pop('obj_final')
        if 'error' in context:
            context['error'] = str(context['error'])
        try:
            json_answer = json.dumps(context)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON: {}".format(context))
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


class OrderCreateTicket(View):

    def get(self, request, *args, **kwargs):
        raise Exception("get")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        list_lines = ast.literal_eval(request._body.decode())['lines']
        context = SalesLines.create_ticket_from_order(pk, list_lines)
        if 'obj_final' in context:
            context.pop('obj_final')
        if 'error' in context:
            context['error'] = str(context['error'])
        try:
            json_answer = json.dumps(context)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON: {}".format(context))
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


class OrderCreateInvoice(View):

    def get(self, request, *args, **kwargs):
        raise Exception("get")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        list_lines = ast.literal_eval(request._body.decode())['lines']
        context = SalesLines.create_invoice_from_order(pk, list_lines)
        if 'obj_final' in context:
            context.pop('obj_final')
        if 'error' in context:
            context['error'] = str(context['error'])
        try:
            json_answer = json.dumps(context)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON: {}".format(context))
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


class OrderForeign(GenOrderUrl, GenForeignKey):
    model = SalesOrder
    label = "{code}"

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(code__icontains=search)
        qs = queryset.filter(qsobject)

        albaran_pk = filters.get('albaran_pk', None)
        if albaran_pk:
            qs = qs.filter(customer=Customer.objects.filter(order_sales__line_order_sales__line_albaran_sales__albaran__pk=albaran_pk).first())

        ticket_pk = filters.get('ticket_pk', None)
        if ticket_pk:
            qs = qs.filter(customer=Customer.objects.filter(ticket_sales__pk=ticket_pk).first())

        invoice_pk = filters.get('invoice_pk', None)
        if invoice_pk:
            qs = qs.filter(customer=Customer.objects.filter(invoice_sales__pk=invoice_pk).first())

        if ticket_pk or invoice_pk:
            # excluyo las lineas de pedidos que ya estan en ticket o facturas (tenemos en cuenta que esten todas las cantidades)
            """
            lts = [x[0] for x in LineTicket.objects.all().values_list('line_order')]
            lfs = [x[0] for x in LineInvoice.objects.all().values_list('line_order')]
            lo = list(set(lts + lfs))

            lts = LineTicket.objects.all().annotate(q=Sum('quantity')).values('q', 'line_order', 'line_order__quantity')
            lfs = LineInvoice.objects.all().annotate(q=Sum('quantity')).values('q', 'line_order', 'line_order__quantity')
            lo_pk = []
            for lines in list(lts) + list(lfs):
                if lines['line_order__quantity'] <= lines['q']:
                    lo_pk.append(lines['line_order'])
            """
            orders_pk = {}
            for line in SalesLines.objects.all():
                if line.order.pk not in orders_pk:
                    orders_pk[line.order.pk] = {'count': 0, 'complete': []}
                orders_pk[line.order.pk]['count'] += 1

                quantity = 0
                # solo cuando creamos ticket controlamos que no esten ya en ticket
                # desde un ticket se pueden crear facturas
                if ticket_pk and line.line_ticket_sales.exists():
                    quantity += line.line_ticket_sales.annotate(q=Sum('quantity')).values_list('q')[0][0]
                if line.line_invoice_sales.exists():
                    quantity += line.line_invoice_sales.annotate(q=Sum('quantity')).values_list('q')[0][0]
                if line.quantity <= quantity:
                    orders_pk[line.order.pk]['complete'].append(line.pk)

            list_exclude = []
            if orders_pk:
                for order_pk in orders_pk:
                    if orders_pk[order_pk]['count'] == len(orders_pk[order_pk]['complete']):
                        list_exclude.append(order_pk)

            qs = qs.exclude(pk__in=list_exclude)

        return qs[:settings.LIMIT_FOREIGNKEY]


# ###########################################
class GenOrderDocumentUrl(object):
    ws_entry_point = '{}/orderdocuments'.format(settings.CDNX_INVOICING_URL_SALES)


class OrderDocumentSubList(GenOrderDocumentUrl, GenList):
    model = SalesOrderDocument
    extra_context = {'menu': ['sales', 'SalesOrderDocument'], 'bread': [_('Sales'), _('SalesOrderDocument')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(order__pk=pk)
        limit['removed'] = Q(order__removed=False)
        return limit


class OrderDocumentCreate(GenOrderDocumentUrl, DocumentFileView, GenCreate):
    model = SalesOrderDocument
    form_class = OrderDocumentForm

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        if self.__pk:
            self.form_class = OrderDocumentSublistForm
        return super(OrderDocumentCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            obj = SalesOrder.objects.get(pk=self.__pk)
            self.request.order = obj
            form.instance.order = obj
        return super(OrderDocumentCreate, self).form_valid(form)


class OrderDocumentCreateModal(GenCreateModal, OrderDocumentCreate):
    pass


class OrderDocumentUpdate(GenOrderDocumentUrl, DocumentFileView, GenUpdate):
    model = SalesOrderDocument
    form_class = OrderDocumentForm

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('cpk', None)
        if self.__pk:
            self.form_class = OrderDocumentSublistForm
        return super(OrderDocumentUpdate, self).dispatch(*args, **kwargs)


class OrderDocumentUpdateModal(GenUpdateModal, OrderDocumentUpdate):
    pass


class OrderDocumentDelete(GenOrderDocumentUrl, GenDelete):
    model = SalesOrderDocument


# ###########################################
class GenAlbaranUrl(object):
    ws_entry_point = '{}/albarans'.format(settings.CDNX_INVOICING_URL_SALES)


# Albaran
class AlbaranList(GenAlbaranUrl, GenList):
    model = SalesAlbaran
    show_details = True
    linkadd = False
    template_model = "sales/albaran_list.html"
    extra_context = {'menu': ['sales', 'Albaran'], 'bread': [_('Sales'), _('Albaran')]}
    default_ordering = "-created"

    def __limitQ__(self, info):
        limit = {}
        limit['removed'] = Q(removed=False)
        return limit


class AlbaranCreate(GenAlbaranUrl, GenCreate):
    model = SalesAlbaran
    form_class = AlbaranForm
    show_details = True


class AlbaranCreateModal(GenCreateModal, AlbaranCreate):
    pass


class AlbaranUpdate(GenAlbaranUrl, GenUpdate):
    model = SalesAlbaran
    show_details = True
    form_class = AlbaranForm


class AlbaranUpdateModal(GenUpdateModal, AlbaranUpdate):
    pass


class AlbaranDelete(GenAlbaranUrl, GenDelete):
    model = SalesAlbaran


class AlbaranDetails(GenAlbaranUrl, GenDetail):
    model = SalesAlbaran
    groups = AlbaranForm.__groups_details__()
    template_model = "sales/albaran_details.html"
    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_saleslines_sublist_albaran', 'rows': 'base'},
        {'id': 'line_reason', 'name': _('Lines modificed'), 'ws': 'CDNX_invoicing_reasonmodificationlinealbarans_sublist', 'rows': 'base'},
        {'id': 'line_printer', 'name': _('Print counter'), 'ws': 'CDNX_invoicing_printcounterdocumentalbarans_sublist', 'rows': 'base'},
    ]
    exclude_fields = ['parent_pk']
    linkedit = False
    linkdelete = False

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = self.model.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            self.linkedit = True
            self.linkdelete = True

        return super(AlbaranDetails, self).dispatch(*args, **kwargs)


class AlbaranSend(View):

    @method_decorator(login_required)
    def get(self, *args, **kwargs):

        # Get Inventory PK
        self.pk = kwargs.get('pk', None)
        albaran = SalesAlbaran.objects.filter(pk=self.pk).first()

        # Prepare answer
        answer = {}

        # Check answer
        if not albaran:
            # No albaran
            answer['return'] = _("Albaran not found!")
        elif albaran.send:
            # Already sent
            answer['return'] = _("Albaran already sent!")
        else:

            # Lock it and set it ready to send
            albaran.send = True
            albaran.lock = True
            albaran.save()

            # Return answer
            answer['return'] = "OK"

        # Return answer
        json_answer = json.dumps(answer)
        return HttpResponse(json_answer, content_type='application/json')


class AlbaranPrint(PrinterHelper, GenAlbaranUrl, GenDetail):
    model = SalesAlbaran
    modelname = "list"
    template_model = 'sales/pdf/albaran_pdf.html'
    output_filename = '{0}{1}{2}_albaran'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(AlbaranPrint, self).get_context_data(**kwargs)

        albaran = self.object
        albaran.print_counter(get_current_user())

        # I take address for send.
        context["albaran"] = albaran
        customer = None

        lines = []
        total_albaran = 0
        for line in albaran.line_albaran_sales.all():
            base = (line.line_order.price_base * line.line_order.quantity)
            subtotal = base + (base * line.line_order.tax / 100.0)
            total_albaran += subtotal
            lines.append({
                'product': line.line_order.product,
                'price_base': line.line_order.price_base,
                'quantity': line.line_order.quantity,
                'tax': line.line_order.tax,
                'total': subtotal
            })

            if customer is None:
                customer = line.line_order.order.customer

        send_address = customer.external.person_address.filter(main=True).first()
        corporate_image = CorporateImage.objects.filter(public=True).first()
        context["customer"] = customer
        context['send_address'] = send_address
        context['line_albaran_sales'] = lines
        context['total_albaran'] = total_albaran
        context['media_root'] = settings.MEDIA_ROOT + "/"
        context["corporate_image"] = corporate_image
        self.output_filename = "{0}".format(albaran.date)

        # bloqueo del documento
        albaran.lock = True
        albaran.save()

        return context


class AlbaranCreateTicket(View):

    def get(self, request, *args, **kwargs):
        raise Exception("get")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        list_lines = ast.literal_eval(request._body.decode())['lines']
        context = SalesLines.create_ticket_from_albaran(pk, list_lines)
        if 'obj_final' in context:
            context.pop('obj_final')
        if 'error' in context:
            context['error'] = str(context['error'])
        try:
            json_answer = json.dumps(context)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON: {}".format(context))
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


class AlbaranCreateInvoice(View):

    def get(self, request, *args, **kwargs):
        raise Exception("get")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        list_lines = ast.literal_eval(request._body.decode())['lines']
        context = SalesLines.create_invoice_from_albaran(pk, list_lines)
        if 'obj_final' in context:
            context.pop('obj_final')
        if 'error' in context:
            context['error'] = str(context['error'])
        try:
            json_answer = json.dumps(context)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON: {}".format(context))
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


# ###########################################
class GenTicketUrl(object):
    ws_entry_point = '{}/tickets'.format(settings.CDNX_INVOICING_URL_SALES)


# Ticket
class TicketList(GenTicketUrl, GenList):
    model = SalesTicket
    show_details = True
    linkadd = False
    template_model = "sales/ticket_list.html"
    extra_context = {'menu': ['sales', 'Ticket'], 'bread': [_('Sales'), _('Ticket')]}
    default_ordering = "-created"

    def __limitQ__(self, info):
        limit = {}
        limit['removed'] = Q(removed=False)
        return limit


class TicketCreate(GenTicketUrl, GenCreate):
    model = SalesTicket
    form_class = TicketForm
    show_details = True


class TicketCreateModal(GenCreateModal, TicketCreate):
    pass


class TicketUpdate(GenTicketUrl, GenUpdate):
    model = SalesTicket
    show_details = True
    form_class = TicketForm


class TicketUpdateModal(GenUpdateModal, TicketUpdate):
    pass


class TicketDelete(GenTicketUrl, GenDelete):
    model = SalesTicket


class TicketDetails(GenTicketUrl, GenDetail):
    model = SalesTicket
    groups = TicketForm.__groups_details__()
    template_model = "sales/ticket_details.html"
    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_saleslines_sublist_ticket', 'rows': 'base'},
        {'id': 'line_reason', 'name': _('Lines modificed'), 'ws': 'CDNX_invoicing_reasonmodificationlinetickets_sublist', 'rows': 'base'},
        {'id': 'line_printer', 'name': _('Print counter'), 'ws': 'CDNX_invoicing_printcounterdocumenttickets_sublist', 'rows': 'base'},
    ]
    exclude_fields = ['parent_pk']
    linkedit = False
    linkdelete = False

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = self.model.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            self.linkedit = True
            self.linkdelete = True

        return super(TicketDetails, self).dispatch(*args, **kwargs)


class TicketPrint(PrinterHelper, GenTicketUrl, GenDetail):
    model = SalesTicket
    modelname = "list"
    template_model = 'sales/pdf/ticket_pdf.html'
    output_filename = '{0}{1}{2}_ticket'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(TicketPrint, self).get_context_data(**kwargs)

        ticket = self.object
        ticket.print_counter(get_current_user())

        # I take address for send.
        if hasattr(ticket.customer.external, 'person_address'):
            send_address = ticket.customer.external.person_address.filter(main=True).first()
        else:
            send_address = None

        context["ticket"] = ticket
        lines = []
        total_ticket = 0
        for line in ticket.line_ticket_sales.all():
            base = (line.price_base * line.quantity)
            subtotal = base + (base * line.tax / 100.0)
            total_ticket += subtotal
            lines.append({
                'product': line.line_order.product,
                'price_base': line.price_base,
                'quantity': line.quantity,
                'tax': line.tax,
                'total': subtotal
            })
        context['line_ticket_sales'] = lines
        context['total_ticket'] = total_ticket
        context['send_address'] = send_address
        context['media_root'] = settings.MEDIA_ROOT + "/"
        corporate_image = CorporateImage.objects.filter(public=True).first()
        context["corporate_image"] = corporate_image
        self.output_filename = "{0}".format(ticket.date)

        # bloqueo del documento
        ticket.lock = True
        ticket.save()

        return context


class TicketCreateInvoice(View):

    def get(self, request, *args, **kwargs):
        raise Exception("get")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        list_lines = ast.literal_eval(request._body.decode())['lines']
        context = SalesLines.create_invoice_from_ticket(pk, list_lines)
        if 'obj_final' in context:
            context.pop('obj_final')
        if 'error' in context:
            context['error'] = str(context['error'])
        try:
            json_answer = json.dumps(context)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON: {}".format(context))
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


class TicketCreateRectification(View):
    def get(self, request, *args, **kwargs):
        raise Exception("TicketCreateRectification")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        ticket = SalesTicket.objects.filter(pk=pk).first()

        list_lines = ast.literal_eval(request._body.decode())['lines']
        list_lines = [int(x) for x in list_lines]

        context = {}
        if list_lines and pk and ticket:
            tr = SalesTicketRectification()
            tr.date = datetime.datetime.now()
            tr.ticket = ticket
            tr.billing_series = ticket.billing_series
            try:
                with transaction.atomic():
                    tr.save()

                    for line_pk in list_lines:
                        li = SalesLines.objects.filter(pk=line_pk).first()
                        if li:
                            li.ticket_rectification = tr
                            li.save()
                        else:
                            raise Exception(_('Line not found'))

                    ticket.lock = True
                    ticket.save()
                    context['url'] = "{}#/{}".format(reverse("CDNX_invoicing_ticketrectificationsaless_list"), tr.pk)
            except Exception as e:
                context['error'] = e
        else:
            context['error'] = _("No select lines")

        try:
            json_answer = json.dumps(context)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON: {}".format(context))
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


# ###########################################
class GenTicketRectificationUrl(object):
    ws_entry_point = '{}/ticketrectifications'.format(settings.CDNX_INVOICING_URL_SALES)


# TicketRectification
class TicketRectificationList(GenTicketRectificationUrl, GenList):
    model = SalesTicketRectification
    show_details = True
    linkadd = False
    extra_context = {'menu': ['sales', 'TicketRectification'], 'bread': [_('Sales'), _('TicketRectification')]}
    default_ordering = "-created"

    def __limitQ__(self, info):
        limit = {}
        limit['removed'] = Q(removed=False)
        return limit


class TicketRectificationCreate(GenTicketRectificationUrl, GenCreate):
    model = SalesTicketRectification
    form_class = TicketRectificationForm
    hide_foreignkey_button = True
    show_details = True


class TicketRectificationCreateModal(GenCreateModal, TicketRectificationCreate):
    pass


class TicketRectificationUpdate(GenTicketRectificationUrl, GenUpdate):
    model = SalesTicketRectification
    show_details = True
    form_class = TicketRectificationUpdateForm


class TicketRectificationUpdateModal(GenUpdateModal, TicketRectificationUpdate):
    pass


class TicketRectificationDelete(GenTicketRectificationUrl, GenDelete):
    model = SalesTicketRectification


class TicketRectificationDetails(GenTicketRectificationUrl, GenDetail):
    model = SalesTicketRectification
    groups = TicketRectificationForm.__groups_details__()
    template_model = "sales/ticketrectification_details.html"

    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_saleslines_sublist_ticketrectificaction', 'rows': 'base'},
        {'id': 'line_reason', 'name': _('Lines modificed'), 'ws': 'CDNX_invoicing_reasonmodificationlineticketrectifications_sublist', 'rows': 'base'},
        {'id': 'line_printer', 'name': _('Print counter'), 'ws': 'CDNX_invoicing_printcounterdocumentticketrectifications_sublist', 'rows': 'base'},
    ]
    exclude_fields = ['lock', 'parent_pk']
    linkedit = False
    linkdelete = False

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = self.model.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            self.linkedit = True
            self.linkdelete = True

        return super(TicketRectificationDetails, self).dispatch(*args, **kwargs)


class TicketRectificationPrint(PrinterHelper, GenTicketRectificationUrl, GenDetail):
    model = SalesTicketRectification
    modelname = "list"
    template_model = 'sales/pdf/ticketrectification_pdf.html'
    output_filename = '{0}{1}{2}_ticketrectification'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(TicketRectificationPrint, self).get_context_data(**kwargs)

        ticketrectification = self.object
        ticketrectification.print_counter(get_current_user())

        customer = None

        context["ticketrectification"] = ticketrectification
        lines = []
        total_ticketrectification = 0
        for line in ticketrectification.line_ticketrectification_sales.all():
            base = (line.line_ticket.price_base * line.line_ticket.quantity)
            subtotal = base + (base * line.line_ticket.tax / 100.0)
            total_ticketrectification += subtotal
            lines.append({
                'product': line.line_ticket.line_order.product,
                'price_base': line.line_ticket.price_base,
                'quantity': line.line_ticket.quantity,
                'tax': line.line_ticket.tax,
                'total': subtotal
            })
            if customer is None:
                customer = line.line_ticket.ticket.customer

        # I take address for send.
        if customer and hasattr(customer.external, 'person_address'):
            send_address = customer.external.person_address.filter(main=True).first()
        else:
            send_address = None
        corporate_image = CorporateImage.objects.filter(public=True).first()

        context['customer'] = customer
        context['line_ticketrectification_sales'] = lines
        context['total_ticketrectification'] = total_ticketrectification
        context['send_address'] = send_address
        context['media_root'] = settings.MEDIA_ROOT + "/"
        context["corporate_image"] = corporate_image
        self.output_filename = "{0}".format(ticketrectification.date)

        # bloqueo del documento
        ticketrectification.lock = True
        ticketrectification.save()

        return context


# ###########################################
class GenInvoiceUrl(object):
    ws_entry_point = '{}/invoices'.format(settings.CDNX_INVOICING_URL_SALES)


# Invoice
class InvoiceList(GenInvoiceUrl, GenList):
    model = SalesInvoice
    show_details = True
    linkadd = False
    template_model = "sales/invoice_list.html"
    extra_context = {'menu': ['sales', 'Invoice'], 'bread': [_('Sales'), _('Invoice')]}
    default_ordering = "-created"

    def __limitQ__(self, info):
        limit = {}
        limit['removed'] = Q(removed=False)
        return limit


class InvoiceCreate(GenInvoiceUrl, GenCreate):
    model = SalesInvoice
    form_class = InvoiceForm
    show_details = True


class InvoiceCreateModal(GenCreateModal, InvoiceCreate):
    pass


class InvoiceUpdate(GenInvoiceUrl, GenUpdate):
    model = SalesInvoice
    show_details = True
    form_class = InvoiceForm


class InvoiceUpdateModal(GenUpdateModal, InvoiceUpdate):
    pass


class InvoiceDelete(GenInvoiceUrl, GenDelete):
    model = SalesInvoice


class InvoiceDetails(GenInvoiceUrl, GenDetail):
    model = SalesInvoice
    groups = InvoiceForm.__groups_details__()
    template_model = "sales/invoice_details.html"
    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_saleslines_sublist_invoice', 'rows': 'base'},
        {'id': 'line_reason', 'name': _('Lines modificed'), 'ws': 'CDNX_invoicing_reasonmodificationlineinvoices_sublist', 'rows': 'base'},
        {'id': 'line_printer', 'name': _('Print counter'), 'ws': 'CDNX_invoicing_printcounterdocumentinvoices_sublist', 'rows': 'base'},
    ]
    exclude_fields = ['lock', 'parent_pk']
    linkedit = False
    linkdelete = False

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = self.model.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            self.linkedit = True
            self.linkdelete = True

        return super(InvoiceDetails, self).dispatch(*args, **kwargs)


class InvoiceCreateRectification(View):

    def get(self, request, *args, **kwargs):
        raise Exception("InvoiceCreateRectification")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        invoice = SalesInvoice.objects.filter(pk=pk).first()

        list_lines = ast.literal_eval(request._body.decode())['lines']
        list_lines = [int(x) for x in list_lines]

        context = {}
        if list_lines and pk and invoice:
            ir = SalesInvoiceRectification()
            ir.date = datetime.datetime.now()
            ir.invoice = invoice
            ir.billing_series = invoice.billing_series
            try:
                with transaction.atomic():
                    ir.save()

                    alir = []
                    for line_pk in list_lines:
                        li = SalesLines.objects.filter(pk=line_pk).first()
                        if li:
                            li.invoice_rectification = ir
                            li.save()
                        else:
                            raise Exception(_('Line not found'))

                    invoice.lock = True
                    invoice.save()
                    context['alir'] = alir
                    context['lir'] = li.pk
                    context['url'] = "{}#/{}".format(reverse("CDNX_invoicing_invoicerectificationsaless_list"), ir.pk)
            except Exception as e:
                context['error'] = e
        else:
            context['error'] = _("No select lines")

        try:
            json_answer = json.dumps(context)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON: {}".format(context))
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


class InvoiceCreateRectificationUnity(GenUpdate):
    model = SalesLines
    form_class = LineOfInvoiceRectificationUnityForm

    def get_form(self, form_class=None):
        form = super(InvoiceCreateRectificationUnity, self).get_form(form_class)
        initial = form.initial
        initial['quantity_original'] = initial['quantity']
        return form

    def form_valid(self, form):
        quantity = form.data['quantity']
        if quantity > self.object.quantity:
            errors = form._errors.setdefault("reason", ErrorList())
            errors.append(_("Quantity invalid. More quantity than allowed"))
            return super(InvoiceCreateRectificationUnity, self).form_invalid(form)
        elif quantity == self.object.quantity:
            # generar TR y asociar
            # crear PU?
            pass
        else:
            # duplicar saleslines
            # generar TR y asociar
            # crear PU?
            pass
        raise Exception("form_valid pending!!!!")


class InvoicePrint(PrinterHelper, GenInvoiceUrl, GenDetail):
    model = SalesInvoice
    modelname = "list"
    template_model = 'sales/pdf/invoice_pdf.html'
    output_filename = '{0}{1}{2}_invoice'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(InvoicePrint, self).get_context_data(**kwargs)

        invoice = self.object
        invoice.print_counter(get_current_user())

        # I take address for send.
        if hasattr(invoice.customer.external, 'person_address'):
            send_address = invoice.customer.external.person_address.filter(main=True).first()
        else:
            send_address = None

        context["invoice"] = invoice
        lines = []
        total_invoice = 0
        for line in invoice.line_invoice_sales.all():
            base = (line.price_base * line.quantity)
            subtotal = base + (base * line.tax / 100.0)
            total_invoice += subtotal
            lines.append({
                'product': line.line_order.product,
                'price_base': line.price_base,
                'quantity': line.quantity,
                'tax': line.tax,
                'total': subtotal
            })
        context['line_invoice_sales'] = lines
        context['total_invoice'] = total_invoice
        context['send_address'] = send_address
        context['media_root'] = settings.MEDIA_ROOT + "/"
        corporate_image = CorporateImage.objects.filter(public=True).first()
        context["corporate_image"] = corporate_image
        self.output_filename = "{0}".format(invoice.date)

        # bloqueo del documento
        invoice.lock = True
        invoice.save()

        return context


# ###########################################
class GenInvoiceRectificationUrl(object):
    ws_entry_point = '{}/invoicerectifications'.format(settings.CDNX_INVOICING_URL_SALES)


# InvoiceRectification
class InvoiceRectificationList(GenInvoiceRectificationUrl, GenList):
    model = SalesInvoiceRectification
    show_details = True
    linkadd = False
    extra_context = {'menu': ['sales', 'InvoiceRectification'], 'bread': [_('Sales'), _('InvoiceRectification')]}
    default_ordering = "-created"

    def __limitQ__(self, info):
        limit = {}
        limit['removed'] = Q(removed=False)
        return limit


class InvoiceRectificationCreate(GenInvoiceRectificationUrl, GenCreate):
    model = SalesInvoiceRectification
    form_class = InvoiceRectificationForm
    hide_foreignkey_button = True
    show_details = True


class InvoiceRectificationCreateModal(GenCreateModal, InvoiceRectificationCreate):
    pass


class InvoiceRectificationUpdate(GenInvoiceRectificationUrl, GenUpdate):
    model = SalesInvoiceRectification
    show_details = True
    form_class = InvoiceRectificationUpdateForm


class InvoiceRectificationUpdateModal(GenUpdateModal, InvoiceRectificationUpdate):
    pass


class InvoiceRectificationDelete(GenInvoiceRectificationUrl, GenDelete):
    model = SalesInvoiceRectification


class InvoiceRectificationDetails(GenInvoiceRectificationUrl, GenDetail):
    model = SalesInvoiceRectification
    groups = InvoiceRectificationForm.__groups_details__()
    template_model = "sales/invoicerectification_details.html"

    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_saleslines_sublist_invoicerectification', 'rows': 'base'},
        {'id': 'line_reason', 'name': _('Lines modificed'), 'ws': 'CDNX_invoicing_reasonmodificationlineinvoicerectifications_sublist', 'rows': 'base'},
        {'id': 'line_printer', 'name': _('Print counter'), 'ws': 'CDNX_invoicing_printcounterdocumentinvoicerectifications_sublist', 'rows': 'base'},
    ]
    exclude_fields = ['lock', 'parent_pk']
    linkedit = False
    linkdelete = False

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = self.model.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            self.linkedit = True
            self.linkdelete = True

        return super(InvoiceRectificationDetails, self).dispatch(*args, **kwargs)


class InvoiceRectificationPrint(PrinterHelper, GenInvoiceRectificationUrl, GenDetail):
    model = SalesInvoiceRectification
    modelname = "list"
    template_model = 'sales/pdf/invoicerectification_pdf.html'
    output_filename = '{0}{1}{2}_invoicerectification'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(InvoiceRectificationPrint, self).get_context_data(**kwargs)

        invoicerectification = self.object
        invoicerectification.print_counter(get_current_user())

        customer = None

        context["invoicerectification"] = invoicerectification
        lines = []
        total_invoicerectification = 0
        for line in invoicerectification.line_invoicerectification_sales.all():
            base = (line.line_invoice.price_base * line.line_invoice.quantity)
            subtotal = base + (base * line.line_invoice.tax / 100.0)
            total_invoicerectification += subtotal
            lines.append({
                'product': line.line_invoice.line_order.product,
                'price_base': line.line_invoice.price_base,
                'quantity': line.line_invoice.quantity,
                'tax': line.line_invoice.tax,
                'total': subtotal
            })
            if customer is None:
                customer = line.line_invoice.invoice.customer

        # I take address for send.
        if customer and hasattr(customer.external, 'person_address'):
            send_address = customer.external.person_address.filter(main=True).first()
        else:
            send_address = None
        corporate_image = CorporateImage.objects.filter(public=True).first()

        context['customer'] = customer
        context['line_invoicerectification_sales'] = lines
        context['total_invoicerectification'] = total_invoicerectification
        context['send_address'] = send_address
        context['media_root'] = settings.MEDIA_ROOT + "/"
        context["corporate_image"] = corporate_image
        self.output_filename = "{0}".format(invoicerectification.date)

        # bloqueo del documento
        invoicerectification.lock = True
        invoicerectification.save()

        return context


"""
# ###########################################
class GenReservedProduct(object):
    ws_entry_point = '{}/reservedproducts'.format(settings.CDNX_INVOICING_URL_SALES)


# SalesReservedProduct
class ReservedProductList(GenReservedProduct, GenList):
    model = SalesReservedProduct
    extra_context = {'menu': ['sales', 'SalesReservedProduct'], 'bread': [_('Sales'), _('SalesReservedProduct')]}
    default_ordering = "-created"


class ReservedProductCreate(GenReservedProduct, GenCreate):
    model = SalesReservedProduct
    form_class = ReservedProductForm


class ReservedProductUpdate(GenReservedProduct, GenUpdate):
    model = SalesReservedProduct
    form_class = ReservedProductForm


class ReservedProductDelete(GenReservedProduct, GenDelete):
    model = SalesReservedProduct

"""


# ###########################################
class GenShoppingCart(object):
    ws_entry_point = '{}/shoppingcarts'.format(settings.CDNX_INVOICING_URL_SALES)


class ShoppingCartManagement(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def get(self, request, *args, **kwargs):
        """
        List all products in the shopping cart
        """
        cart = ShoppingCartProxy(request)
        return JsonResponse(cart.get_products(onlypublic=request.GET.get('onlypublic', True)))

    def post(self, request, *args, **kwargs):
        """
        Adds new product to the current shopping cart
        """
        POST = json.loads(request.body.decode('utf-8'))

        if 'product_pk' in POST and 'quantity' in POST:
            cart = ShoppingCartProxy(request)
            cart.add(
                product_pk=int(POST['product_pk']),
                quantity=int(POST['quantity'])
            )
            return JsonResponse(cart.products)

        return HttpResponseBadRequest()

    def put(self, request, *args, **kwargs):
        PUT = json.loads(request.body.decode('utf-8'))

        if 'product_pk' in PUT and 'quantity' in PUT:
            cart = ShoppingCartProxy(request)
            product_pk = int(PUT['product_pk'])
            cart.edit(
                product_pk=product_pk,
                quantity=int(PUT['quantity'])
            )
            return JsonResponse(cart.product(product_pk))

        return HttpResponseBadRequest()

    def delete(self, request, *args, **kwargs):
        DELETE = json.loads(request.body.decode('utf-8'))

        if 'product_pk' in DELETE:
            cart = ShoppingCartProxy(request)
            cart.remove(product_pk=int(DELETE['product_pk']))
            return JsonResponse(cart.totals)

        return HttpResponseBadRequest()


# ###########################################
# PrintCounterDocumentBasket
class PrintCounterDocumentBasketSublist(GenList):
    model = PrintCounterDocumentBasket
    extra_context = {'menu': ['sales', 'ReasonModificationLineInvoiceRectification'], 'bread': [_('Sales'), _('ReasonModificationLineInvoiceRectification')]}
    linkadd = False
    linkedit = False
    default_ordering = "-date"

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(basket__pk=pk)
        return limit


# ###########################################
# PrintCounterDocumentOrder
class PrintCounterDocumentOrderSublist(GenList):
    model = PrintCounterDocumentOrder
    extra_context = {'menu': ['sales', 'PrintCounterDocumentOrder'], 'bread': [_('Sales'), _('PrintCounterDocumentOrder')]}
    linkadd = False
    linkedit = False
    default_ordering = "-date"

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(order__pk=pk)
        return limit


# ###########################################
# PrintCounterDocumentAlbaran
class PrintCounterDocumentAlbaranSublist(GenList):
    model = PrintCounterDocumentAlbaran
    extra_context = {'menu': ['sales', 'PrintCounterDocumentAlbaran'], 'bread': [_('Sales'), _('PrintCounterDocumentAlbaran')]}
    linkadd = False
    linkedit = False
    default_ordering = "-date"

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(albaran__pk=pk)
        return limit


# ###########################################
# PrintCounterDocumentTicket
class PrintCounterDocumentTicketSublist(GenList):
    model = PrintCounterDocumentTicket
    extra_context = {'menu': ['sales', 'PrintCounterDocumentTicket'], 'bread': [_('Sales'), _('PrintCounterDocumentTicket')]}
    linkadd = False
    linkedit = False
    default_ordering = "-date"

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(ticket__pk=pk)
        return limit


# ###########################################
# PrintCounterDocumentTicketRectification
class PrintCounterDocumentTicketRectificationSublist(GenList):
    model = PrintCounterDocumentTicketRectification
    extra_context = {'menu': ['sales', 'PrintCounterDocumentTicketRectification'], 'bread': [_('Sales'), _('PrintCounterDocumentTicketRectification')]}
    linkadd = False
    linkedit = False
    default_ordering = "-date"

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(ticket_rectification__pk=pk)
        return limit


# ###########################################
# PrintCounterDocumentInvoice
class PrintCounterDocumentInvoiceSublist(GenList):
    model = PrintCounterDocumentInvoice
    extra_context = {'menu': ['sales', 'PrintCounterDocumentInvoice'], 'bread': [_('Sales'), _('PrintCounterDocumentInvoice')]}
    linkadd = False
    linkedit = False
    default_ordering = "-date"

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(invoice__pk=pk)
        return limit


# ###########################################
# PrintCounterDocumentInvoiceRectification
class PrintCounterDocumentInvoiceRectificationSublist(GenList):
    model = PrintCounterDocumentInvoiceRectification
    extra_context = {'menu': ['sales', 'PrintCounterDocumentInvoiceRectification'], 'bread': [_('Sales'), _('PrintCounterDocumentInvoiceRectification')]}
    linkadd = False
    linkedit = False
    default_ordering = "-date"

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(invoice_rectification__pk=pk)
        return limit


# ###########################################
# ######### SalesLines ######################
# ###########################################
class LinesSubListBasket(GenList):
    model = SalesLines
    field_delete = False
    field_check = False
    ngincludes = {"table": "/static/codenerix_invoicing/partials/sales/table_linebasket.html"}
    gentrans = {
        'CreateBudget': _("Create Budget"),
        'CreateOrder': _("Create Order"),
        'Debeseleccionarproducto': ('Debe seleccionar los productos'),
    }
    linkadd = False
    linkedit = False
    client_context = {
        'order_btn': False,
        # 'budget_btn': False,
        # 'invoice_btn': False,
    }

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = SalesBasket.objects.filter(pk=self.__pk).first()
        if obj:
            if not obj.lock:
                self.linkadd = True
                self.linkedit = True
                self.field_delete = True

            num_lines = obj.lines_sales.filter(removed=False).count()
            if num_lines != obj.lines_sales.filter(removed=False, order__isnull=False).count():
                self.client_context['order_btn'] = True
            self.client_context['num_lines'] = num_lines
            self.client_context['num_lines_order'] = obj.lines_sales.filter(removed=False, order__isnull=False).count()
            # elif obj.role == ROLE_BASKET_BUDGET:
            #     self.field_check = None

        return super(LinesSubListBasket, self).dispatch(*args, **kwargs)

    def get_context_json(self, context):
        answer = super(LinesSubListBasket, self).get_context_json(context)

        obj = SalesBasket.objects.filter(pk=self.__pk).first()
        answer['meta']['role_shoppingcart'] = None
        answer['meta']['role_budget'] = None
        answer['meta']['role_wishlist'] = None
        if obj:
            if obj.role == ROLE_BASKET_SHOPPINGCART:
                answer['meta']['role_shoppingcart'] = True
            elif obj.role == ROLE_BASKET_BUDGET:
                answer['meta']['role_budget'] = True
        return answer

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(basket__pk=pk)
        limit['removed'] = Q(removed=False)
        return limit


class LinesCreateBasket(GenCreate):
    model = SalesLines
    form_class = LineOfBasketForm


class LinesCreateModalBasket(GenCreateModal, LinesCreateBasket):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LinesCreateModalBasket, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            obj = SalesBasket.objects.filter(pk=self.__pk).first()
            if obj:
                self.request.basket = obj
                form.instance.basket = obj
            else:
                errors = form._errors.setdefault("product_final", ErrorList())
                errors.append(_('Budget not found'))
                return self.form_invalid(form)
        else:
            errors = form._errors.setdefault("product_final", ErrorList())
            errors.append(_('Budget undefined'))
            return self.form_invalid(form)

        try:
            return super(LinesCreateModalBasket, self).form_valid(form)
        except ValidationError as e:
            errors = form._errors.setdefault("product_final", ErrorList())
            errors.append(e)
            return self.form_invalid(form)
        except IntegrityError as e:
            errors = form._errors.setdefault("product_final", ErrorList())
            errors.append(e)
            return self.form_invalid(form)


class LinesUpdateBasket(GenUpdate):
    model = SalesLines
    form_class = LineOfBasketFormUpdate


class LinesUpdateModalBasket(GenUpdateModal, LinesUpdateBasket):
    # form_class = LineBasketForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__line_pk = kwargs.get('pk', None)
        """
        if SalesLineBasketOption.objects.filter(line_budget__pk=self.__line_pk).exists():
            self.form_class = LineBasketFormPack
            self.__is_pack = True
        else:
            self.__is_pack = False
        """
        return super(LinesUpdateModalBasket, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        # form_kwargs = super(LineBasketUpdateModal, self).get_form_kwargs(*args, **kwargs)
        form = super(LinesUpdateModalBasket, self).get_form(form_class)
        initial = form.initial
        initial['type_tax'] = self.object.product_final.product.tax.pk
        initial['tax'] = self.object.tax_basket
        initial['price'] = float(self.object.price_base_basket) * (1 + (self.object.tax_basket / 100))
        """
        if self.__is_pack:
            options = []
            lang = get_language_database()

            for option in SalesLineBasketOption.objects.filter(line_budget__pk=self.__line_pk):
                initial['packs[{}]'.format(option.product_option.pk)] = option.product_final.pk
                a = {
                    'id': option.product_option.pk,
                    'label': getattr(option.product_option, lang).name,
                    'products': list(option.product_option.products_pack.all().values('pk').annotate(name=F('{}__name'.format(lang)))),
                    'selected': option.product_final.pk,
                }
                options.append(a)
            # compatibility with GenForeignKey
            initial['packs'] = json.dumps({'__JSON_DATA__': options})
        """
        return form

    def form_valid(self, form):
        # lb = SalesLines.objects.filter(pk=self.__line_pk).first()

        # product_old = lb.product_final
        product_pk = self.request.POST.get("product_final", None)
        quantity = self.request.POST.get("quantity", None)
        product_final = ProductFinal.objects.filter(pk=product_pk).first()
        """
        if product:
            is_pack = product.is_pack()
        else:
            is_pack = False
        """
        if product_final and quantity:
            reason = form.data['reason']
            if reason:
                reason_obj = ReasonModification.objects.filter(pk=reason).first()
                if reason_obj:
                    try:
                        with transaction.atomic():
                            result = super(LinesUpdateModalBasket, self).form_valid(form)

                            reason_basket = ReasonModificationLineBasket()
                            reason_basket.basket = self.object.basket
                            reason_basket.reason = reason_obj
                            reason_basket.line = self.object
                            reason_basket.user = get_current_user()
                            reason_basket.quantity = self.object.quantity
                            reason_basket.save()
                            return result
                    except ValidationError as e:
                        errors = form._errors.setdefault("product_final", ErrorList())
                        errors.append(e)
                        return super(LinesUpdateModalBasket, self).form_invalid(form)
                else:
                    errors = form._errors.setdefault("reason", ErrorList())
                    errors.append(_("Reason of modification invalid"))
                    return super(LinesUpdatelOrder, self).form_invalid(form)
            else:
                errors = form._errors.setdefault("reason", ErrorList())
                errors.append(_("Reason of modification invalid"))
                return super(LinesUpdatelOrder, self).form_invalid(form)

            """
            if is_pack:
                options = product.productfinals_option.filter(active=True)
                options_pack = []
                for option in options:
                    field = 'packs[{}]'.format(option.pk)
                    opt = self.request.POST.get(field, None)
                    if opt:
                        opt_product = ProductFinal.objects.filter(pk=opt).first()
                        if opt_product:
                            options_pack.append({
                                'product_option': option,
                                'product_final': opt_product,
                                'quantity': quantity
                            })
                        else:
                            errors = form._errors.setdefault(field, ErrorList())
                            errors.append(_("Product Option invalid"))
                            return super(LinesUpdateModalBasket, self).form_invalid(form)
                    else:
                        errors = form._errors.setdefault(field, ErrorList())
                        errors.append(_("Option invalid"))
                        return super(LinesUpdateModalBasket, self).form_invalid(form)
            """
        else:
            errors = form._errors.setdefault("product_final", ErrorList())
            errors.append((_("Product invalid"), quantity, product_final))
            return super(LinesUpdateModalBasket, self).form_invalid(form)

        """
        ret = super(LinesUpdateModalBasket, self).form_valid(form)
        if product_old != self.object.product:
            self.object.remove_options()
        if is_pack:
            self.object.set_options(options_pack)
        return ret
        """


class LineBasketDelete(GenDelete):
    model = SalesLines


# ###########################################
class LinesSubListOrder(GenList):
    model = SalesLines
    field_delete = False
    field_check = False
    ngincludes = {"table": "/static/codenerix_invoicing/partials/sales/table_lineorder.html"}
    gentrans = {
        'CreateAlbaran': _("Create Albaran"),
        'CreateTicket': _("Create Ticket"),
        'CreateInvoice': _("Create Invoice"),
    }
    linkadd = False
    linkedit = False
    show_details = True
    static_partial_row = 'sales/partials/line_order_rows.html'
    client_context = {
        'albaran_btn': False,
        'ticket_btn': False,
        'invoice_btn': False,
    }

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = SalesOrder.objects.filter(pk=self.__pk).first()
        if obj:
            if not obj.lock:  # and obj.albaran is None and obj.ticket is None and obj.invoice is None and obj.ticket_rectification is None and obj.invoice_rectification is None:
                self.linkedit = True
                self.field_delete = True
                self.linkedit = True
                self.show_details = False

            num_lines = obj.lines_sales.filter(removed=False).count()
            if num_lines != obj.lines_sales.filter(removed=False, albaran__isnull=False).count():
                self.client_context['albaran_btn'] = True
            if num_lines != obj.lines_sales.filter(removed=False, ticket__isnull=False).count():
                self.client_context['ticket_btn'] = True
            if num_lines != obj.lines_sales.filter(removed=False, invoice__isnull=False).count():
                self.client_context['invoice_btn'] = True

            if self.client_context['albaran_btn'] is False and self.client_context['ticket_btn'] is False and self.client_context['invoice_btn'] is False:
                self.field_check = None
            return super(LinesSubListOrder, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(order__pk=pk)
        limit['removed'] = Q(removed=False)
        return limit

    def get_context_data(self, **kwargs):
        context = super(LinesSubListOrder, self).get_context_data(**kwargs)
        order_pk = self.kwargs.get('pk', None)
        if order_pk:
            order = SalesOrder.objects.get(pk=order_pk)
            context['total'] = order.calculate_price_doc()
        else:
            context['total'] = 0
        return context


class LinesDetailOrder(GenDetail):
    model = SalesLines
    groups = LineOfOrderForm.__groups_details__()
    exclude_fields = [
        'order',
        'removed',
        'subtotal', 'discounts', 'taxes', 'equivalence_surcharges', 'total',
        'code',
        'price_recommended_basket', 'description_basket', 'price_base_basket', 'discount_basket', 'tax_basket', 'equivalence_surcharge_basket', 'tax_label_basket', 'notes_basket',
        'price_recommended_order',
        'notes_albaran',
        'price_recommended_ticket', 'description_ticket', 'price_base_ticket', 'discount_ticket', 'tax_ticket', 'equivalence_surcharge_ticket', 'tax_label_ticket', 'notes_ticket',
        'notes_ticket_rectification',
        'price_recommended_invoice', 'description_invoice', 'price_base_invoice', 'discount_invoice', 'tax_invoice', 'equivalence_surcharge_invoice', 'tax_label_invoice', 'notes_invoice', 'notes_invoice_rectification',
    ]
    linkedit = False
    linkdelete = False

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = self.model.objects.filter(pk=self.__pk).first()
        if obj and (not obj.order.lock or obj.albaran is None or obj.ticket is None or obj.invoice is None or obj.ticket_rectification is None or obj.invoice_rectification is None):
            self.linkedit = True
            self.linkdelete = True

        return super(LinesDetailOrder, self).dispatch(*args, **kwargs)


class LinesDetailModalOrder(GenDetailModal, LinesDetailOrder):
    pass


class LinesUpdatelOrder(GenUpdate):
    model = SalesLines
    form_class = LineOfOrderForm

    def get_form(self, form_class=None):
        form = super(LinesUpdatelOrder, self).get_form(form_class)
        initial = form.initial
        price = initial['price_base_order'] * Decimal(1 + (initial['tax_order'] / 100))
        initial['price'] = price.quantize(Decimal(1 / Decimal(10) ** CURRENCY_DECIMAL_PLACES), rounding=ROUND_HALF_UP)
        initial['tax'] = initial['tax_order']
        return form

    def form_valid(self, form):
        reason = form.data['reason']
        if reason:
            reason_obj = ReasonModification.objects.filter(pk=reason).first()
            if reason_obj:
                try:
                    with transaction.atomic():
                        result = super(LinesUpdatelOrder, self).form_valid(form)

                        reason_order = ReasonModificationLineOrder()
                        reason_order.order = self.object.order
                        reason_order.reason = reason_obj
                        reason_order.line = self.object
                        reason_order.user = get_current_user()
                        reason_order.quantity = self.object.quantity
                        reason_order.save()
                        return result
                except Exception as e:
                    errors = form._errors.setdefault("other", ErrorList())
                    errors.append(e)
                    return super(LinesUpdatelOrder, self).form_invalid(form)
            else:
                errors = form._errors.setdefault("reason", ErrorList())
                errors.append(_("Reason of modification invalid"))
                return super(LinesUpdatelOrder, self).form_invalid(form)
        else:
            errors = form._errors.setdefault("reason", ErrorList())
            errors.append(_("Reason of modification invalid"))
            return super(LinesUpdatelOrder, self).form_invalid(form)


class LinesUpdateModalOrder(GenUpdateModal, LinesUpdatelOrder):
    pass


# ###########################################
class LinesSubListAlbaran(GenList):
    model = SalesLines
    field_delete = False
    ngincludes = {"table": "/static/codenerix_invoicing/partials/sales/table_linealbaran.html"}
    gentrans = {
        'CreateTicket': _("Create Ticket"),
        'CreateInvoice': _("Create Invoice"),
    }
    linkadd = False
    linkedit = False
    client_context = {
        'ticket_btn': False,
        'invoice_btn': False,
    }

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = SalesAlbaran.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            # self.linkadd = True
            self.linkedit = True
            self.field_delete = True

            num_lines = obj.lines_sales.filter(removed=False).count()
            if num_lines != obj.lines_sales.filter(removed=False, ticket__isnull=False).count():
                self.client_context['ticket_btn'] = True
            if num_lines != obj.lines_sales.filter(removed=False, invoice__isnull=False).count():
                self.client_context['invoice_btn'] = True

            if self.client_context['ticket_btn'] is True or self.client_context['invoice_btn'] is True:
                self.field_check = False

        return super(LinesSubListAlbaran, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(albaran__pk=pk)
        limit['removed'] = Q(removed=False)
        return limit

    def get_context_data(self, **kwargs):
        context = super(LinesSubListAlbaran, self).get_context_data(**kwargs)
        obj_pk = self.kwargs.get('pk', None)
        if obj_pk:
            obj = SalesAlbaran.objects.get(pk=obj_pk)
            context['total'] = obj.calculate_price_doc()
        else:
            context['total'] = 0
        return context


class LinesUpdateAlbaran(GenUpdate):
    model = SalesLines
    form_class = LineOfAlbaranForm
    hide_foreignkey_button = True

    def form_valid(self, form):
        reason = form.data['reason']
        if reason:
            reason_obj = ReasonModification.objects.filter(pk=reason).first()
            if reason_obj:
                try:
                    with transaction.atomic():
                        result = super(LinesUpdateAlbaran, self).form_valid(form)

                        reason_order = ReasonModificationLineAlbaran()
                        reason_order.albaran = self.object.albaran
                        reason_order.reason = reason_obj
                        reason_order.line = self.object
                        reason_order.user = get_current_user()
                        reason_order.quantity = self.object.quantity
                        reason_order.save()
                        return result
                except Exception as e:
                    errors = form._errors.setdefault("other", ErrorList())
                    errors.append(e)
                    return super(LinesUpdatelOrder, self).form_invalid(form)
            else:
                errors = form._errors.setdefault("reason", ErrorList())
                errors.append(_("Reason of modification invalid"))
                return super(LinesUpdatelOrder, self).form_invalid(form)
        else:
            errors = form._errors.setdefault("reason", ErrorList())
            errors.append(_("Reason of modification invalid"))
            return super(LinesUpdatelOrder, self).form_invalid(form)


class LinesUpdateModalAlbaran(GenUpdateModal, LinesUpdateAlbaran):
    pass


# ###########################################
class LinesSubListInvoice(GenList):
    model = SalesLines
    field_check = False
    ngincludes = {"table": "/static/codenerix_invoicing/partials/sales/table_lineinvoice.html"}
    gentrans = {
        'CreateInvoiceRectification': _("Create Invoice Rectification"),
    }
    linkadd = False
    show_details = True

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = SalesInvoice.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            self.linkedit = True
        return super(LinesSubListInvoice, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(invoice__pk=pk)
        limit['removed'] = Q(removed=False)
        return limit

    def get_context_data(self, **kwargs):
        context = super(LinesSubListInvoice, self).get_context_data(**kwargs)
        obj_pk = self.kwargs.get('pk', None)
        if obj_pk:
            obj = SalesInvoice.objects.get(pk=obj_pk)
            context['total'] = obj.calculate_price_doc()
        else:
            context['total'] = 0
        return context


class LinesDetailInvoice(GenDetail):
    model = SalesLines
    groups = LineOfInvoiceForm.__groups_details__()
    gentrans = {
        'CreateInvoiceRectification': _("Create Invoice Rectification"),
    }
    linkedit = False
    linkdelete = False
    exclude_fields = [
        'basket', 'tax_basket_fk', 'order', 'tax_order_fk', 'albaran', 'ticket', 'tax_ticket_fk', 'ticket_rectification', 'invoice', 'tax_invoice_fk', 'invoice_rectification', 'product_final', 'product_unique',
        # logical deletion
        'removed',
        # additional information
        'subtotal', 'discounts', 'taxes', 'equivalence_surcharges', 'total',
        # info basket
        'price_recommended_basket', 'description_basket', 'price_base_basket', 'discount_basket', 'tax_basket', 'equivalence_surcharge_basket', 'tax_label_basket', 'notes_basket',
        # info order
        'price_recommended_order', 'description_order', 'price_base_order', 'discount_order', 'tax_order', 'equivalence_surcharge_order', 'tax_label_order', 'notes_order',
        # info albaran - basic
        'notes_albaran',
        # info ticket
        'price_recommended_ticket', 'description_ticket', 'price_base_ticket', 'discount_ticket', 'tax_ticket', 'equivalence_surcharge_ticket', 'tax_label_ticket', 'notes_ticket',
        # info ticket rectification - basic
        'notes_ticket_rectification',
        # info invoice
        'price_recommended_invoice',
        # info invoice rectification - basic
        'notes_invoice_rectification',
    ]


class LinesDetailModalInvoice(GenDetailModal, LinesDetailInvoice):
    template_model = "sales/saleslines_invoice_detailsmodal.html"


class LinesUpdateModalInvoice(GenUpdate):
    model = SalesLines
    form_class = LineOfInvoiceForm
    hide_foreignkey_button = True

    def form_valid(self, form):
        reason = form.data['reason']
        if reason:
            reason_obj = ReasonModification.objects.filter(pk=reason).first()
            if reason_obj:
                try:
                    with transaction.atomic():
                        result = super(LinesUpdateModalInvoice, self).form_valid(form)

                        reason_order = ReasonModificationLineInvoice()
                        reason_order.invoice = self.object.invoice
                        reason_order.reason = reason_obj
                        reason_order.line = self.object
                        reason_order.user = get_current_user()
                        reason_order.quantity = self.object.quantity
                        reason_order.save()
                        return result
                except Exception as e:
                    errors = form._errors.setdefault("other", ErrorList())
                    errors.append(e)
                    return super(LinesUpdateModalInvoice, self).form_invalid(form)
            else:
                errors = form._errors.setdefault("reason", ErrorList())
                errors.append(_("Reason of modification invalid"))
                return super(LinesUpdateModalInvoice, self).form_invalid(form)
        else:
            errors = form._errors.setdefault("reason", ErrorList())
            errors.append(_("Reason of modification invalid"))
            return super(LinesUpdateModalInvoice, self).form_invalid(form)


# ###########################################
class LinesSubListInvoiceRectification(GenList):
    model = SalesLines
    gentrans = {
        'CreateInvoice': _("Create Invoice Rectification"),
    }
    linkadd = False
    linkedit = False

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = SalesInvoiceRectification.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            self.linkadd = True
            self.linkedit = True
        return super(LinesSubListInvoiceRectification, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(invoice_rectification__pk=pk)
        limit['removed'] = Q(removed=False)
        return limit


class LinesUpdateModalInvoiceRectification(GenUpdate):
    model = SalesLines
    form_class = LineOfInvoiceRectificationForm
    hide_foreignkey_button = True

    def form_valid(self, form):
        reason = form.data['reason']
        if reason:
            reason_obj = ReasonModification.objects.filter(pk=reason).first()
            if reason_obj:
                try:
                    with transaction.atomic():
                        result = super(LinesUpdateModalInvoiceRectification, self).form_valid(form)

                        reason_order = ReasonModificationLineInvoice()
                        reason_order.invoice_rectification = self.object.invoice_rectification
                        reason_order.reason = reason_obj
                        reason_order.line = self.object
                        reason_order.user = get_current_user()
                        reason_order.quantity = self.object.quantity
                        reason_order.save()
                        return result
                except Exception as e:
                    errors = form._errors.setdefault("other", ErrorList())
                    errors.append(e)
                    return super(LinesUpdateModalInvoiceRectification, self).form_invalid(form)
            else:
                errors = form._errors.setdefault("reason", ErrorList())
                errors.append(_("Reason of modification invalid"))
                return super(LinesUpdateModalInvoiceRectification, self).form_invalid(form)
        else:
            errors = form._errors.setdefault("reason", ErrorList())
            errors.append(_("Reason of modification invalid"))
            return super(LinesUpdateModalInvoiceRectification, self).form_invalid(form)


# ###########################################
class LinesSubListTicket(GenList):
    model = SalesLines
    field_delete = False
    field_check = False
    ngincludes = {"table": "/static/codenerix_invoicing/partials/sales/table_lineticket.html"}
    gentrans = {
        'CreateInvoice': _("Create Invoice"),
        'CreateTicketRectification': _("Create Ticket Rectification"),
    }
    linkadd = False
    linkedit = False

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = SalesTicket.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            self.linkadd = True
            self.linkedit = True
            self.field_delete = True
        return super(LinesSubListTicket, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(ticket__pk=pk)
        limit['removed'] = Q(removed=False)
        return limit

    def get_context_data(self, **kwargs):
        context = super(LinesSubListTicket, self).get_context_data(**kwargs)
        obj_pk = self.kwargs.get('pk', None)
        if obj_pk:
            obj = SalesTicket.objects.get(pk=obj_pk)
            context['total'] = obj.calculate_price_doc()
        else:
            context['total'] = 0
        return context


class LinesUpdateModalTicket(GenUpdate):
    model = SalesLines
    form_class = LineOfInvoiceRectificationForm
    hide_foreignkey_button = True

    def form_valid(self, form):
        reason = form.data['reason']
        if reason:
            reason_obj = ReasonModification.objects.filter(pk=reason).first()
            if reason_obj:
                try:
                    with transaction.atomic():
                        result = super(LinesUpdateModalTicket, self).form_valid(form)

                        reason_order = ReasonModificationLineTicket()
                        reason_order.ticket = self.object.ticket
                        reason_order.reason = reason_obj
                        reason_order.line = self.object
                        reason_order.user = get_current_user()
                        reason_order.quantity = self.object.quantity
                        reason_order.save()
                        return result
                except Exception as e:
                    errors = form._errors.setdefault("other", ErrorList())
                    errors.append(e)
                    return super(LinesUpdateModalTicket, self).form_invalid(form)
            else:
                errors = form._errors.setdefault("reason", ErrorList())
                errors.append(_("Reason of modification invalid"))
                return super(LinesUpdateModalTicket, self).form_invalid(form)
        else:
            errors = form._errors.setdefault("reason", ErrorList())
            errors.append(_("Reason of modification invalid"))
            return super(LinesUpdateModalTicket, self).form_invalid(form)


# ###########################################
class LinesSubListTicketRectification(GenList):
    model = SalesLines
    linkadd = False
    linkedit = False

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = SalesTicketRectification.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            self.linkadd = True
            self.linkedit = True
        return super(LinesSubListTicketRectification, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(ticket_rectification__pk=pk)
        limit['removed'] = Q(removed=False)
        return limit


class LinesUpdateModalTicketRectification(GenUpdate):
    model = SalesLines
    form_class = LineOfInvoiceRectificationForm
    hide_foreignkey_button = True

    def form_valid(self, form):
        reason = form.data['reason']
        if reason:
            reason_obj = ReasonModification.objects.filter(pk=reason).first()
            if reason_obj:
                try:
                    with transaction.atomic():
                        result = super(LinesUpdateModalTicketRectification, self).form_valid(form)

                        reason_order = ReasonModificationLineTicketRectification()
                        reason_order.ticket_rectification = self.object.ticket_rectification
                        reason_order.reason = reason_obj
                        reason_order.line = self.object
                        reason_order.user = get_current_user()
                        reason_order.quantity = self.object.quantity
                        reason_order.save()
                        return result
                except Exception as e:
                    errors = form._errors.setdefault("other", ErrorList())
                    errors.append(e)
                    return super(LinesUpdateModalTicketRectification, self).form_invalid(form)
            else:
                errors = form._errors.setdefault("reason", ErrorList())
                errors.append(_("Reason of modification invalid"))
                return super(LinesUpdateModalTicketRectification, self).form_invalid(form)
        else:
            errors = form._errors.setdefault("reason", ErrorList())
            errors.append(_("Reason of modification invalid"))
            return super(LinesUpdateModalTicketRectification, self).form_invalid(form)


##############################
class LinesVending(GenList):
    extra_context = {'menu': ['vending', 'vending'], 'bread': [_('Vending'), _('Vending')]}
    ws_entry_point = '{}/vending/CDNX_INVOICING_URL_SALES'.format(settings.CDNX_INVOICING_URL_SALES)
    model = SalesLines
    show_details = False
    linkedit = False
    template_model = "vendings/lines_work.html"
    static_partial_header = 'vendings/vending_header.html'
    static_app_row = 'vendings/vending_app.js'
    static_controllers_row = 'vendings/vending_controllers.js'
    # quitar paginacion
    gentrans = {
        'Pay': _("Pay"),
        'Print': _("Print"),
        'Cancel': ('Cancel'),
    }

    def dispatch(self, *args, **kwargs):
        self.budget_pk = kwargs.get('bpk', None)

        budget = SalesBasket.objects.filter(pk=self.budget_pk).first()
        if budget:
            self.extra_context['budget_pk'] = budget.pk

            history_customer = []
            for basket in SalesBasket.objects.filter(customer=budget.customer).exclude(pk=budget.pk).order_by('-date')[:5]:
                history_customer.append({
                    'date': basket.date.replace(tzinfo=pytz.utc).astimezone(tz.tzlocal()).strftime(formats.get_format('DATETIME_INPUT_FORMATS', lang=get_language())[0]),
                    'code': basket.code,
                    'total': basket.total,
                })
            # budget information
            self.extra_context.update({
                'customer': budget.customer.__str__(),
                'name': budget.name,
                'code': budget.code,
                'date': budget.date.replace(tzinfo=pytz.utc).astimezone(tz.tzlocal()).strftime(formats.get_format('DATETIME_INPUT_FORMATS', lang=get_language())[0]),
                'address_delivery': budget.address_delivery,
                'address_invoice': budget.address_invoice,
                'subtotal': float(budget.subtotal),
                'discounts': budget.discounts,
                'taxes': budget.taxes,
                'total': float(budget.total),
                'lock': budget.lock,
                # descuento del cliente
                'cusomer_discount': '123',
                # historial del cliente
                'history': history_customer,
            })
            # budget total
            summary = {}
            totals = {
                'subtotal': 0,
                'tax': 0,
                'total': 0,
            }
            for line in budget.lines_sales.all().values(
                'price_base_basket',
                'quantity',
                'tax_label_basket',
                'tax_basket',
                'tax_basket_fk',
            ):
                if line['tax_basket_fk'] not in summary:
                    summary[line['tax_basket_fk']] = {
                        'label': line['tax_label_basket'],
                        'subtotal': 0,
                        'tax': 0,
                        'total': 0
                    }
                summary[line['tax_basket_fk']]['subtotal'] += float(line['price_base_basket']) * line['quantity']
                summary[line['tax_basket_fk']]['tax'] += (float(line['tax_basket']) * line['quantity']) / 100
                summary[line['tax_basket_fk']]['total'] += summary[line['tax_basket_fk']]['subtotal'] + summary[line['tax_basket_fk']]['tax']
                totals['subtotal'] += summary[line['tax_basket_fk']]['subtotal']
                totals['tax'] += summary[line['tax_basket_fk']]['tax']
                totals['total'] += summary[line['tax_basket_fk']]['total']

            self.extra_context.update({
                'summary': summary,
                'totals': totals,
            })
        else:
            self.extra_context['budget_pk'] = None

        self.ws_entry_point = self.ws_entry_point.replace('CDNX_INVOICING_URL_SALES', self.budget_pk)

        # Prepare form
        self.ws_ean13_fullinfo = reverse('CDNX_storages_inventoryoutline_ean13_fullinfo', kwargs={"ean13": 'PRODUCT_FINAL_EAN13'})[1:]
        self.ws_unique_fullinfo = reverse('CDNX_storages_inventoryoutline_unique_fullinfo', kwargs={"unique": 'PRODUCT_FINAL_UNIQUE'})[1:]
        self.ws_submit = reverse('CDNX_storages_inventoryoutline_addws', kwargs={"ipk": self.budget_pk})[1:]

        fields = []
        fields.append((DynamicInput, 'product_final', 3, 'CDNX_products_productfinalsean13_foreign', [], {}))
        fields.append((DynamicInput, 'product_unique', 3, 'CDNX_products_productuniquescode_foreign', ['product_final'], {}))
        form = SalesLinesInLineForm()
        for (widget, key, minchars, url, autofill, newattrs) in fields:
            wattrs = form.fields[key].widget.attrs
            wattrs.update(newattrs)
            form.fields[key].widget = widget(wattrs)
            form.fields[key].widget.form_name = form.form_name
            form.fields[key].widget.field_name = key
            form.fields[key].widget.autofill_deepness = minchars
            form.fields[key].widget.autofill_url = url
            form.fields[key].widget.autofill = autofill

        # Prepare context
        self.client_context = {
            'budget_pk': self.budget_pk,
            'final_focus': True,
            'unique_focus': False,
            'unique_disabled': True,
            'errors': {
                'quantity': None,
                'product': None,
                'unique': None,
            },
            'ws': {
                'ean13_fullinfo': self.ws_ean13_fullinfo,
                'unique_fullinfo': self.ws_unique_fullinfo,
                'submit': self.ws_submit,
            },
            'form_quantity': form.fields['quantity'].widget.render('quantity', None, {
                'ng-init': 'quantity=1.0',
                'codenerix-on-enter': 'product_changed(this)',
                'ng-class': '{"bg-danger": data.meta.context.errors.quantity}',
            }),
            'form_product': form.fields['product_final'].widget.render('product_final', None, {
                'codenerix-on-enter': 'product_changed(this)',
                'ng-disabled': '(quantity<=0)',
                'codenerix-focus': 'data.meta.context.final_focus',
                'ng-class': '{"bg-danger": final_error || data.meta.context.errors.product}',
                'autofocus': '',
            }),
            'form_price': form.fields['price_tmp'].widget.render('price_tmp', None, {
                'ng-disabled': 'true',
                'ng-value': 'price',
            }),
            'form_tax': form.fields['tax_tmp'].widget.render('tax_tmp', None, {
                'ng-disabled': 'true',
                'ng-value': 'tax',
            }),
            'form_unique': form.fields['product_unique'].widget.render('unique', None, {
                'codenerix-on-enter': 'unique_changed()',
                'codenerix-focus': 'data.meta.context.unique_focus',
                'ng-disabled': 'data.meta.context.unique_disabled',
                'ng-class': '{"bg-danger": data.meta.context.errors.unique || unique_error}',
            }) + " <span class='fa fa-exclamation-triangle text-danger' ng-show='unique_error' alt='{{unique_error}}' title='{{unique_error}}'></span>",
        }

        return super(LinesVending, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        if self.budget_pk:
            limit['budget__pk'] = Q(basket__pk=self.budget_pk)
        limit['removed'] = Q(removed=False)
        return limit

    def __fields__(self, info):
        fields = []
        fields.append(('quantity', _("Quantity")))
        fields.append(('product_final', _("Product")))
        fields.append(('product_unique', _("Unique")))
        fields.append(('price_base_basket', _("Price")))
        fields.append(('tax_basket', _("Tax (%)")))
        return fields


class SalesLinesDetails(GenList):
    model = SalesLines
    ws_entry_point = '{}/vending/0'.format(settings.CDNX_INVOICING_URL_SALES)


class LinesVendingPayment(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.template = 'vendings/vending_payment.html'
        slot_pk = kwargs.get('pk', None)

        context = self.prepare_context()
        context["slot"] = slot_pk
        context['basket'] = SalesBasket.objects.filter(
            pos_slot__pk=slot_pk,
            order_sales__payment__isnull=True,
            role=ROLE_BASKET_SHOPPINGCART,
            order_sales__removed=False,
            removed=False
        ).last()
        if context['basket']:
            context['ticket'] = context['basket'].list_tickets().first()
        # context['PAYMENT_DETAILS_CARD'] = PAYMENT_DETAILS_CARD
        # context['PAYMENT_DETAILS_CASH'] = PAYMENT_DETAILS_CASH
        # context['KIND_CARD_VISA'] = KIND_CARD_VISA
        # context['KIND_CARD_MASTER'] = KIND_CARD_MASTER
        # context['KIND_CARD_AMERICAN'] = KIND_CARD_AMERICAN
        # context['KIND_CARD_OTHER'] = KIND_CARD_OTHER
        context['url_vending_payment'] = 'vending_payment'

        # return render(request, self.template, context)


class BasketDetailsSHOPPINGCARTVending(GenDetail):
    template_model = "vendings/basket_details.html"
    # ws_entry_point = '{}/shoppingcarts/vending'.format(settings.CDNX_INVOICING_URL_SALES)
    model = SalesBasket
    groups = BasketForm.__groups_details__()
    exclude_fields = ['parent_pk', 'payment']
    tabs_XXXXXXXX = [
        {
            'id': 'lines',
            'name': _('Products'),
            'ws': 'CDNX_invoicing_saleslines_sublist_vending',
            'rows': 'base',
            'static_partial_header': 'vendings/vending_header.html',
        },
    ]
    # linkedit = False
    # linkdelete = False
    # linkback = False

    def dispatch(self, *args, **kwargs):
        raise Exception("A!")


######################
class SalesLinesList(GenList):
    model = SalesLines


class LinesSubListBasketVending(GenList):
    model = SalesLines
    # ws_entry_point = '{}/shoppingcarts/vending'.format(settings.CDNX_INVOICING_URL_SALES)
    show_details = False
    field_delete = False
    field_check = False
    linkadd = False
    linkedit = False
    # static_app_row = 'vendings/vending_app.js'
    # static_controllers_row = 'vendings/vending_controllers.js'

    def dispatchX(self, *args, **kwargs):
        raise Exception("A")


class XLinesSubListBasketVending(GenList):
    """
    mejor hacer un genlist de SalesLines de ese 'pedido' y meter la info del 'pedido' en el contexto
    """

    # form_ngcontroller = 'vendings/vending_controllers.js'

    # static_partial_row = 'vendings/vending_rowxxxxxxxxxx'

    # ngincludes = {"table": "/static/codenerix_invoicing/partials/sales/table_linebasket.html"}
    # gentrans = {
    #     'CreateBudget': _("Create Budget"),
    #     'CreateOrder': _("Create Order"),
    #     'Debeseleccionarproducto': ('Debe seleccionar los productos'),
    # }
    # client_context = {
    #     'order_btn': False,
    #     # 'budget_btn': False,
    #     # 'invoice_btn': False,
    # }

    def dispatch(self, *args, **kwargs):
        # Get constants
        self.ipk = kwargs.get('ipk')

        return super(LinesSubListBasketVending, self).dispatch(*args, **kwargs)

    def X_get_context_json(self, context):
        answer = super(LinesSubListBasket, self).get_context_json(context)

        obj = SalesBasket.objects.filter(pk=self.__pk).first()
        answer['meta']['role_shoppingcart'] = None
        answer['meta']['role_budget'] = None
        answer['meta']['role_wishlist'] = None
        if obj:
            if obj.role == ROLE_BASKET_SHOPPINGCART:
                answer['meta']['role_shoppingcart'] = True
            elif obj.role == ROLE_BASKET_BUDGET:
                answer['meta']['role_budget'] = True
        return answer

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(basket__pk=pk)
        limit['removed'] = Q(removed=False)
        return limit
