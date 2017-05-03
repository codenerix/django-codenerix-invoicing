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

from django.db import transaction
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.utils import ErrorList
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View

from django.conf import settings

from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail, GenDetailModal, GenForeignKey

from codenerix_extensions.views import GenCreateBridge, GenUpdateBridge
from codenerix_extensions.corporate.models import CorporateImage
from codenerix_extensions.files.views import DocumentFileView

from codenerix_invoicing.models_sales import Customer, CustomerDocument, \
    SalesOrder, SalesLineOrder, SalesAlbaran, SalesLineAlbaran, SalesTicket, SalesLineTicket, \
    SalesTicketRectification, SalesLineTicketRectification, SalesInvoice, SalesLineInvoice, SalesInvoiceRectification, \
    SalesLineInvoiceRectification, SalesReservedProduct, SalesBasket, SalesLineBasket
from codenerix_invoicing.models_sales import ROLE_BASKET_SHOPPINGCART, ROLE_BASKET_BUDGET, ROLE_BASKET_WISHLIST

from codenerix_invoicing.forms_sales import CustomerForm, CustomerDocumentForm, \
    OrderForm, LineOrderForm, AlbaranForm, LineAlbaranForm, TicketForm, LineTicketForm, \
    TicketRectificationForm, TicketRectificationUpdateForm, LineTicketRectificationLinkedForm, LineTicketRectificationForm, InvoiceForm, LineInvoiceForm, \
    InvoiceRectificationForm, InvoiceRectificationUpdateForm, LineInvoiceRectificationForm, LineInvoiceRectificationLinkedForm, \
    ReservedProductForm, BasketForm, LineBasketForm, OrderFromBudgetForm, OrderFromShoppingCartForm
from codenerix_invoicing.views import PrinterHelper

from .helpers import ShoppingCartProxy


# ###########################################
class GenCustomerUrl(object):
    ws_entry_point = '{}/customers'.format(settings.CDNX_INVOICING_URL_SALES)


# Customer
class CustomerList(GenCustomerUrl, GenList):
    model = Customer
    show_details = True
    extra_context = {'menu': ['Customer', 'people'], 'bread': [_('Customer'), _('People')]}


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
    label = "{pk}"

    def get_foreign(self, queryset, search, filters):
        qs = queryset.exclude(basket_sales__order_sales__isnull=False)
        qs = qs.filter(basket_sales__role=ROLE_BASKET_BUDGET)

        return qs.distinct()[:settings.LIMIT_FOREIGNKEY]


class CustomerForeignShoppingCart(GenCustomerUrl, GenForeignKey):
    model = Customer
    label = "{pk}"

    def get_foreign(self, queryset, search, filters):
        qs = queryset.exclude(basket_sales__order_sales__isnull=False)
        qs = qs.filter(basket_sales__role=ROLE_BASKET_SHOPPINGCART)

        return qs[:settings.LIMIT_FOREIGNKEY]


# ###########################################
# CustomerDocument
class GenCustomerDocumentUrl(object):
    ws_entry_point = '{}/customerdocuments'.format(settings.CDNX_INVOICING_URL_SALES)


class CustomerDocumentSubList(GenCustomerDocumentUrl, GenList):
    model = CustomerDocument
    # show_details = False
    # json = False
    # template_model = "sales/customerdocument_sublist.html"
    # extra_context = {'menu': ['CustomerDocument', 'people'], 'bread': [_('CustomerDocument'), _('People')]}

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
    ws_entry_point = '{}/nshoppingcarts'.format(settings.CDNX_INVOICING_URL_SALES)


class GenBasketBUDGETUrl(object):
    ws_entry_point = '{}/nbudgets'.format(settings.CDNX_INVOICING_URL_SALES)


class GenBasketWISHLISTUrl(object):
    ws_entry_point = '{}/nwishlists'.format(settings.CDNX_INVOICING_URL_SALES)


# SalesBasket
class BasketList(GenList):
    model = SalesBasket
    extra_context = {'menu': ['SalesBasket', 'people'], 'bread': [_('SalesBasket'), _('People')]}
    show_details = True
    template_model = "sales/basket_list.html"
    form_ngcontroller = "codenerixSalesDetailsCtrl"


class BasketListSHOPPINGCART(GenBasketSHOPPINGCARTUrl, BasketList):
    def __limitQ__(self, info):
        limit = {}
        limit['role'] = Q(role=ROLE_BASKET_SHOPPINGCART)
        return limit


class BasketListBUDGET(GenBasketBUDGETUrl, BasketList):
    def __limitQ__(self, info):
        limit = {}
        limit['role'] = Q(role=ROLE_BASKET_BUDGET)
        return limit


class BasketListWISHLIST(GenBasketWISHLISTUrl, BasketList):
    def __limitQ__(self, info):
        limit = {}
        limit['role'] = Q(role=ROLE_BASKET_WISHLIST)
        return limit


class BasketDetails(GenBasketUrl, GenDetail):
    model = SalesBasket
    groups = BasketForm.__groups_details__()
    exclude_fields = ['parent_pk', 'payment']
    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_saleslinebaskets_sublist', 'rows': 'base'},
    ]


class BasketDetailsSHOPPINGCART(GenBasketSHOPPINGCARTUrl, BasketDetails):
    pass


class BasketDetailsBUDGET(GenBasketBUDGETUrl, BasketDetails):
    pass


class BasketDetailsWISHLIST(GenBasketWISHLISTUrl, BasketDetails):
    pass


class BasketCreate(GenBasketUrl, GenCreate):
    model = SalesBasket
    form_class = BasketForm


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
    label = "{code}"

    def get_foreign(self, queryset, search, filters):
        qs = queryset.exclude(order_sales__isnull=False)
        qs = qs.filter(role=ROLE_BASKET_BUDGET)

        customer_pk = filters.get('customer', None)
        if customer_pk:
            qs.filter(customer=filters['customer'])

        return qs[:settings.LIMIT_FOREIGNKEY]


class BasketForeignShoppingCart(GenBasketSHOPPINGCARTUrl, GenForeignKey):
    model = SalesBasket
    label = "{code}"

    def get_foreign(self, queryset, search, filters):
        qs = queryset.exclude(order_sales__isnull=False)
        qs = qs.filter(role=ROLE_BASKET_SHOPPINGCART)

        customer_pk = filters.get('customer', None)
        if customer_pk:
            qs.filter(customer=filters['customer'])

        return qs[:settings.LIMIT_FOREIGNKEY]


class BasketPassToBudget(View):
    def get(self, request, *args, **kwargs):
        raise Exception("get")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = {}
        pk = kwargs.get('pk', None)
        list_lines = ast.literal_eval(request._body)['lines']
        if pk:
            obj = SalesBasket.objects.filter(pk=pk).first()
            if obj:
                obj_budget = obj.pass_to_budget(list_lines)
                context['url'] = "{}#/{}".format(reverse("CDNX_invoicing_salesbaskets_budget_list", obj_budget.pk))
                try:
                    json_answer = json.dumps(context)
                except TypeError:
                    raise TypeError("The structure can not be encoded to JSON")
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
        list_lines = ast.literal_eval(request._body)['lines']
        context = SalesLineBasket.create_order_from_budget(pk, list_lines)
        try:
            json_answer = json.dumps(context)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON")
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')

    def post_orign(self, request, *args, **kwargs):
        context = {}
        pk = kwargs.get('pk', None)
        budget = SalesLineBasket.objects.filter(pk=pk).first()
        # list_budget = request.POST.get('lines', None)
        list_budget = ast.literal_eval(request._body)['lines']
        if list_budget and budget:
            list_budget = [int(x) for x in list_budget]
            # raise Exception ([int(x) for x in list_budget])
            lines_budget = SalesLineOrder.objects.filter(line_budget__pk__in=list_budget)
            if not lines_budget:
                order = SalesOrder()
                order.customer = budget.customer
                order.date = datetime.datetime.now()
                with transaction.atomic():
                    order.save()

                    for lb_pk in list_budget:
                        lb = SalesLineBasket.objects.filter(pk=lb_pk).first()
                        lo = SalesLineOrder()
                        lo.order = order
                        lo.line_budget = lb
                        lo.product = lb.product
                        lo.quantity = lb.quantity
                        lo.price = lb.price
                        lo.tax = lb.tax
                        lo.save()

                context['msg'] = _("Order create")
                # context['url'] = reverse('ordersaless_details', kwargs={'pk': order.pk})
                context['url'] = "{}#/{}".format(reverse('CDNX_invoicing_ordersaless_list'), order.pk)
            else:
                context['error'] = _("Hay lineas asignadas a pedidos")
        else:
            context['error'] = _('Budget not found')
        print(context)

        try:
            json_answer = json.dumps(context)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON")
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


# ###########################################
class GenLineBasketUrl(object):
    ws_entry_point = '{}/linebaskets'.format(settings.CDNX_INVOICING_URL_SALES)


# SalesLineBasket
class LineBasketList(GenList):
    model = SalesLineBasket
    extra_context = {'menu': ['SalesLineBasket', 'SalesLineBasket'], 'bread': [_('SalesLineBasket'), _('SalesLineBasket')]}


class LineBasketCreate(GenLineBasketUrl, GenCreate):
    model = SalesLineBasket
    form_class = LineBasketForm


class LineBasketCreateModal(GenCreateModal, LineBasketCreate):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineBasketCreateModal, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            obj = SalesBasket.objects.get(pk=self.__pk)
            self.request.basket = obj
            form.instance.basket = obj
        return super(LineBasketCreateModal, self).form_valid(form)


class LineBasketUpdate(GenLineBasketUrl, GenUpdate):
    model = SalesLineBasket
    form_class = LineBasketForm


class LineBasketUpdateModal(GenUpdateModal, LineBasketUpdate):
    pass


class LineBasketDelete(GenLineBasketUrl, GenDelete):
    model = SalesLineBasket


class LineBasketSubList(GenLineBasketUrl, GenList):
    model = SalesLineBasket
    field_delete = True
    field_check = False
    ngincludes = {"table": "/static/codenerix_invoicing/partials/sales/table_linebasket.html"}
    gentrans = {
        'CreateBudget': _("Create Budget"),
        'CreateOrder': _("Create Order"),
        'Debeseleccionarproducto': ('Debe seleccionar los productos'),
    }

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineBasketSubList, self).dispatch(*args, **kwargs)
    
    def get_context_json(self, context):
        answer = super(LineBasketSubList, self).get_context_json(context)

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
        return limit


class LineBasketDetails(GenLineBasketUrl, GenDetail):
    model = SalesLineBasket
    groups = LineBasketForm.__groups_details__()


class LineBasketDetailModal(GenDetailModal, LineBasketDetails):
    pass


# ###########################################
class GenOrderUrl(object):
    ws_entry_point = '{}/orders'.format(settings.CDNX_INVOICING_URL_SALES)


# Order
class OrderList(GenOrderUrl, GenList):
    model = SalesOrder
    template_model = "sales/order_list.html"
    show_details = True
    linkadd = False
    extra_context = {'menu': ['Order', 'people'], 'bread': [_('Order'), _('People')]}
    ngincludes = {"table": "/static/codenerix_invoicing/partials/sales/table_order.html"}
    gentrans = {
        'CreateFromBudget': _("Create order from budget"),
        'CreateFromShoppingCart': _("Create order from shopping cart"),
    }


class OrderCreate(GenOrderUrl, GenCreate):
    model = SalesOrder
    form_class = OrderForm
    show_details = True


class OrderCreateModal(GenCreateModal, OrderCreate):
    pass


class OrderCreateModalFromBudget(GenCreateModal, OrderCreate):
    form_class = OrderFromBudgetForm

    def form_valid(self, form):
        r = super(OrderCreateModalFromBudget, self).form_valid(form)
        if SalesLineBasket.create_order_from_budget_all(self.object):
            return r
        else:
            self.object.delete()
            errors = form._errors.setdefault("budget", ErrorList())
            errors.append(_("Hubo un error al crear el pedido, reintentelo de nuevo"))
            return super(OrderCreateModalFromBudget, self).form_invalid(form)


class OrderCreateModalFromShoppingCart(GenCreateModal, OrderCreate):
    form_class = OrderFromShoppingCartForm

    def form_valid(self, form):
        r = super(OrderCreateModalFromShoppingCart, self).form_valid(form)
        if SalesLineBasket.create_order_from_budget_all(self.object):
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
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_lineordersaless_sublist', 'rows': 'base'},
    ]


class OrderPrint(PrinterHelper, GenOrderUrl, GenDetail):
    model = SalesOrder
    modelname = "list"
    template_model = 'sales/pdf/order_pdf.html'
    output_filename = '{0}{1}{2}_order'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(OrderPrint, self).get_context_data(**kwargs)

        order = self.object

        # I take address for send.
        if hasattr(order.customer.external, 'person_address'):
            send_address = order.customer.external.person_address.filter(main=True).first()
        else:
            send_address = None

        context["order"] = order
        lines = []
        total_order = 0
        for line in order.line_order_sales.all():
            base = (line.price * line.quantity)
            subtotal = base + (base * line.tax / 100.0)
            total_order += subtotal
            lines.append({
                'product': line.product,
                'price': line.price,
                'quantity': line.quantity,
                'tax': line.tax,
                'total': subtotal
            })
        context['line_order_sales'] = lines
        context['total_order'] = total_order
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
        raise Exception("get")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        list_lines = ast.literal_eval(request._body)['lines']
        try:
            json_answer = json.dumps(SalesLineOrder.create_albaran_from_order(pk, list_lines))
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON")
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


class OrderCreateTicket(View):

    def get(self, request, *args, **kwargs):
        raise Exception("get")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        list_lines = ast.literal_eval(request._body)['lines']
        try:
            json_answer = json.dumps(SalesLineOrder.create_ticket_from_order(pk, list_lines))
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON")
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


class OrderCreateInvoice(View):

    def get(self, request, *args, **kwargs):
        raise Exception("get")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        list_lines = ast.literal_eval(request._body)['lines']
        try:
            json_answer = json.dumps(SalesLineOrder.create_invoice_from_order(pk, list_lines))
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON")
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
            for line in SalesLineOrder.objects.all():
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
class GenLineOrderUrl(object):
    ws_entry_point = '{}/lineorders'.format(settings.CDNX_INVOICING_URL_SALES)


# LineOrder
class LineOrderList(GenLineOrderUrl, GenList):
    model = SalesLineOrder
    extra_context = {'menu': ['LineOrder', 'people'], 'bread': [_('LineOrder'), _('People')]}


class LineOrderCreate(GenLineOrderUrl, GenCreate):
    model = SalesLineOrder
    form_class = LineOrderForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineOrderCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            obj = SalesOrder.objects.get(pk=self.__pk)
            self.request.order = obj
            form.instance.order = obj

        return super(LineOrderCreate, self).form_valid(form)


class LineOrderCreateModal(GenCreateModal, LineOrderCreate):
    pass


class LineOrderUpdate(GenLineOrderUrl, GenUpdate):
    model = SalesLineOrder
    form_class = LineOrderForm


class LineOrderUpdateModal(GenUpdateModal, LineOrderUpdate):
    pass


class LineOrderDelete(GenLineOrderUrl, GenDelete):
    model = SalesLineOrder


class LineOrderSubList(GenLineOrderUrl, GenList):
    model = SalesLineOrder
    field_delete = True
    field_check = False
    ngincludes = {"table": "/static/codenerix_invoicing/partials/sales/table_lineorder.html"}
    gentrans = {
        'CreateAlbaran': _("Create Albaran"),
        'CreateTicket': _("Create Ticket"),
        'CreateInvoice': _("Create Invoice"),
    }

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(order__pk=pk)
        return limit

    def get_context_data(self, **kwargs):
        context = super(LineOrderSubList, self).get_context_data(**kwargs)
        order_pk = self.kwargs.get('pk', None)
        if order_pk:
            order = SalesOrder.objects.get(pk=order_pk)
            context['total'] = order.calculate_price_doc()
        else:
            context['total'] = 0
        return context


class LineOrderDetails(GenLineOrderUrl, GenDetail):
    model = SalesLineOrder
    groups = LineOrderForm.__groups_details__()


class LineOrderDetailsModal(GenDetailModal, LineOrderDetails):
    pass


class LineOrderForeign(GenLineOrderUrl, GenForeignKey):
    model = SalesLineOrder
    label = "{product} - {quantity}"

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(product__product__code__icontains=search)
        qsobject |= Q(product__product__family__code__icontains=search)
        qsobject |= Q(product__product__family__name__icontains=search)
        qsobject |= Q(product__product__category__code__icontains=search)
        qsobject |= Q(product__product__category__name__icontains=search)
        qs = queryset.filter(qsobject)

        order_pk = filters.get('order', None)
        if order_pk:
            qs = qs.filter(order__pk=order_pk)
        return qs[:settings.LIMIT_FOREIGNKEY]


class LineOrderForeignCustom(GenLineOrderUrl, GenForeignKey):
    model = SalesLineOrder
    label = "{product} - {quantity}"

    def get(self, request, *args, **kwargs):
        search = kwargs.get('search', None)

        filterstxt = self.request.GET.get('filter', '{}')
        filters = json.loads(filterstxt)

        queryset = SalesLineOrder.objects.all()
        if search != '*':
            qsobject = Q(product__product__code__icontains=search)
            qsobject |= Q(product__product__family__code__icontains=search)
            qsobject |= Q(product__product__family__name__icontains=search)
            qsobject |= Q(product__product__category__code__icontains=search)
            qsobject |= Q(product__product__category__name__icontains=search)
            queryset = queryset.filter(qsobject)

        order_pk = filters.get('order', None)
        if order_pk:
            queryset = queryset.filter(order__pk=order_pk)

        answer = {}
        answer['rows'] = []
        answer['clear'] = ['price', 'discount']
        answer['readonly'] = ['price', 'discount']
        answer['rows'].append({
            'price': 0,
            'description': "",
            'discount': 0,
            'label': "---------",
            'id': None,
        })
        for product in queryset[:settings.LIMIT_FOREIGNKEY]:
            answer['rows'].append({
                'price': product.price,
                'description': product.__unicode__(),
                'discount': product.discount,
                'label': product.__unicode__(),
                'id': product.pk,
            })

        try:
            json_answer = json.dumps(answer)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON")
        # Return the new answer
        return HttpResponse(json_answer, content_type='application/json')


# ###########################################
class GenAlbaranUrl(object):
    ws_entry_point = '{}/albarans'.format(settings.CDNX_INVOICING_URL_SALES)


# Albaran
class AlbaranList(GenAlbaranUrl, GenList):
    model = SalesAlbaran
    show_details = True
    template_model = "sales/albaran_list.html"
    extra_context = {'menu': ['Albaran', 'people'], 'bread': [_('Albaran'), _('People')]}


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
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_linealbaransaless_sublist', 'rows': 'base'},
    ]
    exclude_fields = ['parent_pk']


class AlbaranPrint(PrinterHelper, GenAlbaranUrl, GenDetail):
    model = SalesAlbaran
    modelname = "list"
    template_model = 'sales/pdf/albaran_pdf.html'
    output_filename = '{0}{1}{2}_albaran'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(AlbaranPrint, self).get_context_data(**kwargs)

        albaran = self.object

        # I take address for send.
        context["albaran"] = albaran
        customer = None

        lines = []
        total_albaran = 0
        for line in albaran.line_albaran_sales.all():
            base = (line.line_order.price * line.line_order.quantity)
            subtotal = base + (base * line.line_order.tax / 100.0)
            total_albaran += subtotal
            lines.append({
                'product': line.line_order.product,
                'price': line.line_order.price,
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
        list_lines = ast.literal_eval(request._body)['lines']
        xxx = SalesLineOrder.create_ticket_from_albaran(pk, list_lines)
        try:
            json_answer = json.dumps(xxx)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON")
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


class AlbaranCreateInvoice(View):

    def get(self, request, *args, **kwargs):
        raise Exception("get")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        list_lines = ast.literal_eval(request._body)['lines']
        try:
            json_answer = json.dumps(SalesLineOrder.create_invoice_from_albaran(pk, list_lines))
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON")
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


# ###########################################
class GenLineAlbaranUrl(object):
    ws_entry_point = '{}/linealbarans'.format(settings.CDNX_INVOICING_URL_SALES)


# LineAlbaran
class LineAlbaranList(GenLineAlbaranUrl, GenList):
    model = SalesLineAlbaran
    extra_context = {'menu': ['LineAlbaran', 'people'], 'bread': [_('LineAlbaran'), _('People')]}


class LineAlbaranCreate(GenLineAlbaranUrl, GenCreate):
    model = SalesLineAlbaran
    form_class = LineAlbaranForm
    hide_foreignkey_button = True

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineAlbaranCreate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(LineAlbaranCreate, self).get_form(form_class)
        if self.__pk:
            form.fields['albaran_pk'].initial = self.__pk

        return form

    def form_valid(self, form):
        # validate quantity
        line_order = form.instance.line_order
        quantity = form.instance.quantity
        quantity_bd = SalesLineAlbaran.objects.filter(line_order=line_order).aggregate(q=Sum('quantity'))
        units_pending = line_order.quantity
        if quantity_bd['q']:
            quantity += quantity_bd['q']
            units_pending -= quantity_bd['q']

        if line_order.quantity < quantity:
            errors = form._errors.setdefault("quantity", ErrorList())
            errors.append(_("La cantidad seleccionada es excesiva. Quedan pendiente {} unidades por albaranar".format(units_pending)))
            return super(LineAlbaranCreate, self).form_invalid(form)

        # initial albaran
        if self.__pk:
            obj = SalesAlbaran.objects.get(pk=self.__pk)
            self.request.albaran = obj
            form.instance.albaran = obj

        return super(LineAlbaranCreate, self).form_valid(form)


class LineAlbaranCreateModal(GenCreateModal, LineAlbaranCreate):
    pass


class LineAlbaranUpdate(GenLineAlbaranUrl, GenUpdate):
    model = SalesLineAlbaran
    form_class = LineAlbaranForm
    hide_foreignkey_button = True

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineAlbaranUpdate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(LineAlbaranUpdate, self).get_form(form_class)
        form.fields['order'].initial = form.instance.line_order.order
        if self.__pk:
            form.fields['albaran_pk'].initial = self.__pk

        return form


class LineAlbaranUpdateModal(GenUpdateModal, LineAlbaranUpdate):
    pass


class LineAlbaranDelete(GenLineAlbaranUrl, GenDelete):
    model = SalesLineAlbaran


class LineAlbaranSubList(GenLineAlbaranUrl, GenList):
    model = SalesLineAlbaran
    field_delete = True
    field_check = False
    ngincludes = {"table": "/static/codenerix_invoicing/partials/sales/table_linealbaran.html"}
    gentrans = {
        'CreateTicket': _("Create Ticket"),
        'CreateInvoice': _("Create Invoice"),
    }

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(albaran__pk=pk)
        return limit

    def get_context_data(self, **kwargs):
        context = super(LineAlbaranSubList, self).get_context_data(**kwargs)
        obj_pk = self.kwargs.get('pk', None)
        if obj_pk:
            obj = SalesAlbaran.objects.get(pk=obj_pk)
            context['total'] = obj.calculate_price_doc()
        else:
            context['total'] = 0
        return context


class LineAlbaranDetails(GenLineAlbaranUrl, GenDetail):
    model = SalesLineAlbaran
    groups = LineAlbaranForm.__groups_details__()


class LineAlbaranDetailsModal(GenDetailModal, LineAlbaranDetails):
    pass


# ###########################################
class GenTicketUrl(object):
    ws_entry_point = '{}/tickets'.format(settings.CDNX_INVOICING_URL_SALES)


# Ticket
class TicketList(GenTicketUrl, GenList):
    model = SalesTicket
    show_details = True
    template_model = "sales/ticket_list.html"
    extra_context = {'menu': ['Ticket', 'people'], 'bread': [_('Ticket'), _('People')]}


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
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_lineticketsaless_sublist', 'rows': 'base'},
    ]
    exclude_fields = ['parent_pk']


class TicketPrint(PrinterHelper, GenTicketUrl, GenDetail):
    model = SalesTicket
    modelname = "list"
    template_model = 'sales/pdf/ticket_pdf.html'
    output_filename = '{0}{1}{2}_ticket'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(TicketPrint, self).get_context_data(**kwargs)

        ticket = self.object

        # I take address for send.
        send_address = ticket.customer.external.person_address.filter(main=True).first()

        context["ticket"] = ticket
        lines = []
        total_ticket = 0
        for line in ticket.line_ticket_sales.all():
            base = (line.price * line.quantity)
            subtotal = base + (base * line.tax / 100.0)
            total_ticket += subtotal
            lines.append({
                'product': line.line_order.product,
                'price': line.price,
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
        list_lines = ast.literal_eval(request._body)['lines']
        try:
            json_answer = json.dumps(SalesLineOrder.create_invoice_from_ticket(pk, list_lines))
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON")
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


class TicketCreateRectification(View):
    def get(self, request, *args, **kwargs):
        raise Exception("TicketCreateRectification")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        ticket = SalesTicket.objects.filter(pk=pk).first()

        list_lines = ast.literal_eval(request._body)['lines']
        list_lines = [int(x) for x in list_lines]

        context = {}
        if list_lines and pk and ticket:
            tr = SalesTicketRectification()
            tr.date = datetime.datetime.now()
            tr.ticket = ticket
            with transaction.atomic():
                tr.save()

                for line_pk in list_lines:
                    li = SalesLineTicket.objects.filter(pk=line_pk).first()
                    if li:
                        lir = SalesLineTicketRectification()
                        lir.ticket_rectification = tr
                        lir.line_ticket = li
                        lir.quantity = li.quantity
                        lir.save()

                ticket.lock = True
                ticket.save()
                context['url'] = "{}#/{}".format(reverse("CDNX_invoicing_ticketrectificationsaless_list"), tr.pk)
        else:
            context['error'] = _("No select lines")

        try:
            json_answer = json.dumps(context)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON")
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


# ###########################################
class GenLineTicketUrl(object):
    ws_entry_point = '{}/linetickets'.format(settings.CDNX_INVOICING_URL_SALES)


# LineTicket
class LineTicketList(GenLineTicketUrl, GenList):
    model = SalesLineTicket
    extra_context = {'menu': ['LineTicket', 'people'], 'bread': [_('LineTicket'), _('People')]}


class LineTicketCreate(GenLineTicketUrl, GenCreate):
    model = SalesLineTicket
    form_class = LineTicketForm
    hide_foreignkey_button = True

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineTicketCreate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(LineTicketCreate, self).get_form(form_class)
        if self.__pk:
            form.fields['ticket_pk'].initial = self.__pk

        return form

    def form_valid(self, form):
        # validate quantity
        line_order = form.instance.line_order
        quantity = form.instance.quantity
        quantity_ticket = line_order.line_ticket_sales.annotate(q=Sum('quantity')).values_list('q')
        quantity_invoice = line_order.line_invoice_sales.annotate(q=Sum('quantity')).values_list('q')

        quantity_bd = 0
        if quantity_ticket:
            quantity_bd += quantity_ticket[0][0]
        if quantity_invoice:
            quantity_bd += quantity_invoice[0][0]

        units_pending = line_order.quantity - quantity_bd

        if line_order.quantity < quantity:
            errors = form._errors.setdefault("quantity", ErrorList())
            errors.append(_("La cantidad seleccionada es excesiva. Quedan pendiente {} unidades por crear ticket o factura".format(units_pending)))
            return super(LineTicketCreate, self).form_invalid(form)

        # initial ticket
        if self.__pk:
            obj = SalesTicket.objects.get(pk=self.__pk)
            self.request.ticket = obj
            form.instance.ticket = obj

        return super(LineTicketCreate, self).form_valid(form)


class LineTicketCreateModal(GenCreateModal, LineTicketCreate):
    pass


class LineTicketUpdate(GenLineTicketUrl, GenUpdate):
    model = SalesLineTicket
    form_class = LineTicketForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineTicketUpdate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(LineTicketUpdate, self).get_form(form_class)
        if self.__pk:
            form.fields['ticket_pk'].initial = self.__pk
        form.fields['order'].initial = SalesOrder.objects.filter(line_order_sales__pk=form.initial['line_order']).first()
        return form

    def form_valid(self, form):
        # validate quantity
        line_order = form.instance.line_order
        quantity = form.instance.quantity
        quantity_ticket = line_order.line_ticket_sales.annotate(q=Sum('quantity')).values_list('q')
        quantity_invoice = line_order.line_invoice_sales.annotate(q=Sum('quantity')).values_list('q')

        quantity_bd = 0
        if quantity_ticket:
            quantity_bd += quantity_ticket[0][0]
        if quantity_invoice:
            quantity_bd += quantity_invoice[0][0]

        units_pending = line_order.quantity - quantity_bd

        if line_order.quantity < quantity:
            errors = form._errors.setdefault("quantity", ErrorList())
            errors.append(_("La cantidad seleccionada es excesiva. Quedan pendiente {} unidades por crear ticket o factura".format(units_pending)))
            return super(LineTicketUpdate, self).form_invalid(form)


class LineTicketUpdateModal(GenUpdateModal, LineTicketUpdate):
    pass


class LineTicketDelete(GenLineTicketUrl, GenDelete):
    model = SalesLineTicket


class LineTicketSubList(GenLineTicketUrl, GenList):
    model = SalesLineTicket
    field_check = False
    field_delete = True
    ngincludes = {"table": "/static/codenerix_invoicing/partials/sales/table_lineticket.html"}
    gentrans = {
        'CreateInvoice': _("Create Invoice"),
        'CreateTicketRectification': _("Create Ticket Rectification"),
    }

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(ticket__pk=pk)
        return limit

    def get_context_data(self, **kwargs):
        context = super(LineTicketSubList, self).get_context_data(**kwargs)
        obj_pk = self.kwargs.get('pk', None)
        if obj_pk:
            obj = SalesTicket.objects.get(pk=obj_pk)
            context['total'] = obj.calculate_price_doc()
        else:
            context['total'] = 0
        return context


class LineTicketDetails(GenLineTicketUrl, GenDetail):
    model = SalesLineTicket
    groups = LineTicketForm.__groups_details__()


class LineTicketDetailsModal(GenDetailModal, LineTicketDetails):
    pass


class LineTicketForeign(GenLineTicketUrl, GenForeignKey):
    model = SalesLineTicket
    label = "{description} - {quantity}"

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(description__icontains=search)
        qs = queryset.filter(qsobject)

        ticket_rectification_pk = filters.get('ticket_rectification_pk', None)
        if ticket_rectification_pk:
            # mostramos las lineas del ticket salvo las que ya estan en la propia rectificativa
            qs = qs.filter(
                ticket__ticketrectification_sales__pk=ticket_rectification_pk
            ).exclude(
                pk__in=[x[0] for x in SalesLineTicketRectification.objects.filter(ticket_rectification__pk=ticket_rectification_pk).values_list('line_ticket__pk')]
            )
        return qs[:settings.LIMIT_FOREIGNKEY]


# ###########################################
class GenTicketRectificationUrl(object):
    ws_entry_point = '{}/ticketrectifications'.format(settings.CDNX_INVOICING_URL_SALES)


# TicketRectification
class TicketRectificationList(GenTicketRectificationUrl, GenList):
    model = SalesTicketRectification
    show_details = True
    extra_context = {'menu': ['TicketRectification', 'people'], 'bread': [_('TicketRectification'), _('People')]}


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
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_lineticketrectificationsaless_sublist', 'rows': 'base'},
    ]
    exclude_fields = ['lock', 'parent_pk']


class TicketRectificationPrint(PrinterHelper, GenTicketRectificationUrl, GenDetail):
    model = SalesTicketRectification
    modelname = "list"
    template_model = 'sales/pdf/ticketrectification_pdf.html'
    output_filename = '{0}{1}{2}_ticketrectification'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(TicketRectificationPrint, self).get_context_data(**kwargs)

        ticketrectification = self.object

        customer = None

        context["ticketrectification"] = ticketrectification
        lines = []
        total_ticketrectification = 0
        for line in ticketrectification.line_ticketrectification_sales.all():
            base = (line.line_ticket.price * line.line_ticket.quantity)
            subtotal = base + (base * line.line_ticket.tax / 100.0)
            total_ticketrectification += subtotal
            lines.append({
                'product': line.line_ticket.line_order.product,
                'price': line.line_ticket.price,
                'quantity': line.line_ticket.quantity,
                'tax': line.line_ticket.tax,
                'total': subtotal
            })
            if customer is None:
                customer = line.line_ticket.ticket.customer

        # I take address for send.
        send_address = customer.external.person_address.filter(main=True).first()
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
class GenLineTicketRectificationUrl(object):
    ws_entry_point = '{}/lineticketrectifications'.format(settings.CDNX_INVOICING_URL_SALES)


# LineTicketRectification
class LineTicketRectificationList(GenLineTicketRectificationUrl, GenList):
    model = SalesLineTicketRectification
    extra_context = {'menu': ['LineTicketRectification', 'people'], 'bread': [_('LineTicketRectification'), _('People')]}


class LineTicketRectificationCreate(GenLineTicketRectificationUrl, GenCreate):
    model = SalesLineTicketRectification
    form_class = LineTicketRectificationForm


class LineTicketRectificationCreateModal(GenCreateModal, LineTicketRectificationCreate):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineTicketRectificationCreateModal, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(LineTicketRectificationCreateModal, self).get_form(form_class)
        if self.__pk:
            form.fields['ticket_rectification_pk'].initial = self.__pk

        return form

    def form_valid(self, form):
        line_ticket = form.instance.line_ticket
        # sumatorio de las cantidades ya devueltas de la misma linea
        quantity_tmp = SalesLineTicketRectification.objects.filter(
            line_ticket=line_ticket
        ).annotate(
            q=Sum('quantity')
        ).values('q')
        if quantity_tmp:
            quantity_bd = line_ticket.quantity - quantity_tmp[0]['q']
        else:
            quantity_bd = line_ticket.quantity
        # comprobamos que la cantidad correcta
        if quantity_bd < form.instance.quantity:
            errors = form._errors.setdefault("quantity", ErrorList())
            errors.append(_("La cantidad seleccionada es excesiva. Las unidades maximas a devolver son {}".format(quantity_bd)))
            return super(LineTicketRectificationCreateModal, self).form_invalid(form)
        # initial ticket rectification
        if self.__pk:
            ticket_rectification = SalesTicketRectification.objects.get(pk=self.__pk)
            self.request.ticket_rectification = ticket_rectification
            form.instance.ticket_rectification = ticket_rectification

        return super(LineTicketRectificationCreateModal, self).form_valid(form)


class LineTicketRectificationUpdate(GenLineTicketRectificationUrl, GenUpdate):
    model = SalesLineTicketRectification
    form_class = LineTicketRectificationForm

    def form_valid(self, form):
        line_ticket = form.instance.line_ticket
        # sumatorio de las cantidades ya devueltas de la misma linea salvo al actual
        quantity_tmp = SalesLineTicketRectification.objects.filter(
            line_ticket=line_ticket
        ).exclude(
            pk=form.initial.get("id")
        ).annotate(
            q=Sum('quantity')
        ).values('q')
        if quantity_tmp:
            quantity_bd = line_ticket.quantity - quantity_tmp[0]['q']
        else:
            quantity_bd = line_ticket.quantity

        # comprobamos que la cantidad correcta
        if quantity_bd < form.instance.quantity:
            errors = form._errors.setdefault("quantity", ErrorList())
            errors.append(_("La cantidad seleccionada es excesiva. Las unidades maximas a devolver son {}".format(quantity_bd)))
            return super(LineTicketRectificationUpdate, self).form_invalid(form)

        return super(LineTicketRectificationUpdate, self).form_valid(form)


class LineTicketRectificationUpdateModal(GenUpdateModal, LineTicketRectificationUpdate):
    form_class = LineTicketRectificationLinkedForm


class LineTicketRectificationDelete(GenLineTicketRectificationUrl, GenDelete):
    model = SalesLineTicketRectification


class LineTicketRectificationSubList(GenLineTicketRectificationUrl, GenList):
    model = SalesLineTicketRectification

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(ticket_rectification__pk=pk)
        return limit


class LineTicketRectificationDetails(GenLineTicketRectificationUrl, GenDetail):
    model = SalesLineTicketRectification
    groups = LineTicketRectificationForm.__groups_details__()
    exclude_fields = []


class LineTicketRectificationDetailModal(GenDetailModal, LineTicketRectificationDetails):
    pass


# ###########################################
class GenInvoiceUrl(object):
    ws_entry_point = '{}/invoices'.format(settings.CDNX_INVOICING_URL_SALES)


# Invoice
class InvoiceList(GenInvoiceUrl, GenList):
    model = SalesInvoice
    show_details = True
    template_model = "sales/invoice_list.html"
    extra_context = {'menu': ['Invoice', 'people'], 'bread': [_('Invoice'), _('People')]}


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
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_lineinvoicesaless_sublist', 'rows': 'base'},
    ]
    exclude_fields = ['lock', 'parent_pk']


class InvoiceCreateRectification(View):

    def get(self, request, *args, **kwargs):
        raise Exception("InvoiceCreateRectification")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        invoice = SalesInvoice.objects.filter(pk=pk).first()

        list_lines = ast.literal_eval(request._body)['lines']
        list_lines = [int(x) for x in list_lines]

        context = {}
        if list_lines and pk and invoice:
            ir = SalesInvoiceRectification()
            ir.date = datetime.datetime.now()
            ir.invoice = invoice
            with transaction.atomic():
                ir.save()

                alir = []
                for line_pk in list_lines:
                    li = SalesLineInvoice.objects.filter(pk=line_pk).first()
                    if li:
                        lir = SalesLineInvoiceRectification()
                        lir.invoice_rectification = ir
                        lir.line_invoice = li
                        lir.quantity = li.quantity
                        lir.save()
                        alir.append([line_pk, lir.pk])

                invoice.lock = True
                invoice.save()
                context['alir'] = alir
                context['lir'] = lir.pk
                context['url'] = "{}#/{}".format(reverse("CDNX_invoicing_invoicerectificationsaless_list"), ir.pk)
        else:
            context['error'] = _("No select lines")

        try:
            json_answer = json.dumps(context)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON")
        # Return the new context
        return HttpResponse(json_answer, content_type='application/json')


class InvoicePrint(PrinterHelper, GenInvoiceUrl, GenDetail):
    model = SalesInvoice
    modelname = "list"
    template_model = 'sales/pdf/invoice_pdf.html'
    output_filename = '{0}{1}{2}_invoice'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(InvoicePrint, self).get_context_data(**kwargs)

        invoice = self.object

        # I take address for send.
        send_address = invoice.customer.external.person_address.filter(main=True).first()

        context["invoice"] = invoice
        lines = []
        total_invoice = 0
        for line in invoice.line_invoice_sales.all():
            base = (line.price * line.quantity)
            subtotal = base + (base * line.tax / 100.0)
            total_invoice += subtotal
            lines.append({
                'product': line.line_order.product,
                'price': line.price,
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
class GenLineInvoiceUrl(object):
    ws_entry_point = '{}/lineinvoices'.format(settings.CDNX_INVOICING_URL_SALES)


# LineInvoice
class LineInvoiceList(GenLineInvoiceUrl, GenList):
    model = SalesLineInvoice
    extra_context = {'menu': ['LineInvoice', 'people'], 'bread': [_('LineInvoice'), _('People')]}


class LineInvoiceCreate(GenLineInvoiceUrl, GenCreate):
    model = SalesLineInvoice
    form_class = LineInvoiceForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineInvoiceCreate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(LineInvoiceCreate, self).get_form(form_class)
        if self.__pk:
            form.fields['invoice_pk'].initial = self.__pk

        return form

    def form_valid(self, form):
        # validate quantity
        line_order = form.instance.line_order
        quantity = form.instance.quantity
        quantity_invoice = line_order.line_invoice_sales.annotate(q=Sum('quantity')).values_list('q')

        quantity_bd = 0
        if quantity_invoice:
            quantity_bd += quantity_invoice[0][0]

        units_pending = line_order.quantity - quantity_bd

        if line_order.quantity < quantity:
            errors = form._errors.setdefault("quantity", ErrorList())
            errors.append(_("La cantidad seleccionada es excesiva. Quedan pendiente {} unidades por crear facturar".format(units_pending)))
            return super(LineInvoiceCreate, self).form_invalid(form)

        # initial invoice
        if self.__pk:
            obj = SalesInvoice.objects.get(pk=self.__pk)
            self.request.invoice = obj
            form.instance.invoice = obj

        return super(LineInvoiceCreate, self).form_valid(form)


class LineInvoiceCreateModal(GenCreateModal, LineInvoiceCreate):
    pass


class LineInvoiceUpdate(GenLineInvoiceUrl, GenUpdate):
    model = SalesLineInvoice
    form_class = LineInvoiceForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineInvoiceUpdate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(LineInvoiceUpdate, self).get_form(form_class)
        if self.__pk:
            form.fields['invoice_pk'].initial = self.__pk
        form.fields['order'].initial = SalesOrder.objects.filter(line_order_sales__pk=form.initial['line_order']).first()
        return form

    def form_valid(self, form):
        # validate quantity
        line_order = form.instance.line_order
        quantity = form.instance.quantity
        quantity_invoice = line_order.line_invoice_sales.annotate(q=Sum('quantity')).values_list('q')

        quantity_bd = 0
        if quantity_invoice:
            quantity_bd += quantity_invoice[0][0]

        units_pending = line_order.quantity - quantity_bd

        if line_order.quantity < quantity:
            errors = form._errors.setdefault("quantity", ErrorList())
            errors.append(_("La cantidad seleccionada es excesiva. Quedan pendiente {} unidades por facturar".format(units_pending)))
            return super(LineInvoiceUpdate, self).form_invalid(form)

        return super(LineInvoiceUpdate, self).form_valid(form)


class LineInvoiceUpdateModal(GenUpdateModal, LineInvoiceUpdate):
    pass


class LineInvoiceDelete(GenLineInvoiceUrl, GenDelete):
    model = SalesLineInvoice


class LineInvoiceSubList(GenLineInvoiceUrl, GenList):
    model = SalesLineInvoice
    field_check = False
    ngincludes = {"table": "/static/codenerix_invoicing/partials/sales/table_lineinvoice.html"}
    gentrans = {
        'CreateInvoiceRectification': _("Create Invoice Rectification"),
    }

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(invoice__pk=pk)
        return limit

    def get_context_data(self, **kwargs):
        context = super(LineInvoiceSubList, self).get_context_data(**kwargs)
        obj_pk = self.kwargs.get('pk', None)
        if obj_pk:
            obj = SalesInvoice.objects.get(pk=obj_pk)
            context['total'] = obj.calculate_price_doc()
        else:
            context['total'] = 0
        return context


class LineInvoiceDetails(GenLineInvoiceUrl, GenDetail):
    model = SalesLineInvoice
    groups = LineInvoiceForm.__groups_details__()


class LineInvoiceDetailsModal(GenDetailModal, LineInvoiceDetails):
    pass


class LineInvoiceForeign(GenLineInvoiceUrl, GenForeignKey):
    model = SalesLineInvoice
    label = "{description} - {quantity}"

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(description__icontains=search)
        qs = queryset.filter(qsobject)

        invoice_rectification_pk = filters.get('invoice_rectification_pk', None)
        if invoice_rectification_pk:
            # mostramos las lineas de la factura salvo las que ya estan en la propia rectificativa
            qs = qs.filter(
                invoice__invoicerectification_sales__pk=invoice_rectification_pk
            ).exclude(
                pk__in=[x[0] for x in SalesLineInvoiceRectification.objects.filter(invoice_rectification__pk=invoice_rectification_pk).values_list('line_invoice__pk')]
            )
        return qs[:settings.LIMIT_FOREIGNKEY]


# ###########################################
class GenInvoiceRectificationUrl(object):
    ws_entry_point = '{}/invoicerectifications'.format(settings.CDNX_INVOICING_URL_SALES)


# InvoiceRectification
class InvoiceRectificationList(GenInvoiceRectificationUrl, GenList):
    model = SalesInvoiceRectification
    show_details = True
    extra_context = {'menu': ['InvoiceRectification', 'people'], 'bread': [_('InvoiceRectification'), _('People')]}


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
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_lineinvoicerectificationsaless_sublist', 'rows': 'base'},
    ]
    exclude_fields = ['lock', 'parent_pk']


class InvoiceRectificationPrint(PrinterHelper, GenInvoiceRectificationUrl, GenDetail):
    model = SalesInvoiceRectification
    modelname = "list"
    template_model = 'sales/pdf/invoicerectification_pdf.html'
    output_filename = '{0}{1}{2}_invoicerectification'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(InvoiceRectificationPrint, self).get_context_data(**kwargs)

        invoicerectification = self.object

        customer = None

        context["invoicerectification"] = invoicerectification
        lines = []
        total_invoicerectification = 0
        for line in invoicerectification.line_invoicerectification_sales.all():
            base = (line.line_invoice.price * line.line_invoice.quantity)
            subtotal = base + (base * line.line_invoice.tax / 100.0)
            total_invoicerectification += subtotal
            lines.append({
                'product': line.line_invoice.line_order.product,
                'price': line.line_invoice.price,
                'quantity': line.line_invoice.quantity,
                'tax': line.line_invoice.tax,
                'total': subtotal
            })
            if customer is None:
                customer = line.line_invoice.invoice.customer

        # I take address for send.
        send_address = customer.external.person_address.filter(main=True).first()
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


# ###########################################
class GenLineInvoiceRectificationUrl(object):
    ws_entry_point = '{}/lineinvoicerectifications'.format(settings.CDNX_INVOICING_URL_SALES)


# LineInvoiceRectification
class LineInvoiceRectificationList(GenLineInvoiceRectificationUrl, GenList):
    model = SalesLineInvoiceRectification
    extra_context = {'menu': ['LineInvoiceRectification', 'people'], 'bread': [_('LineInvoiceRectification'), _('People')]}


class LineInvoiceRectificationCreate(GenLineInvoiceRectificationUrl, GenCreate):
    model = SalesLineInvoiceRectification
    form_class = LineInvoiceRectificationForm
    hide_foreignkey_button = True


class LineInvoiceRectificationCreateModal(GenCreateModal, LineInvoiceRectificationCreate):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__invoice_rectification_pk = kwargs.get('pk', None)
        return super(LineInvoiceRectificationCreateModal, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(LineInvoiceRectificationCreateModal, self).get_form(form_class)
        if self.__invoice_rectification_pk:
            form.fields['invoice_rectification_pk'].initial = self.__invoice_rectification_pk

        return form

    def form_valid(self, form):
        line_invoice = form.instance.line_invoice
        # sumatorio de las cantidades ya devueltas de la misma linea
        quantity_tmp = SalesLineInvoiceRectification.objects.filter(
            line_invoice=line_invoice
        ).annotate(
            q=Sum('quantity')
        ).values('q')
        if quantity_tmp:
            quantity_bd = line_invoice.quantity - quantity_tmp[0]['q']
        else:
            quantity_bd = line_invoice.quantity
        # comprobamos que la cantidad correcta
        if quantity_bd < form.instance.quantity:
            errors = form._errors.setdefault("quantity", ErrorList())
            errors.append(_("La cantidad seleccionada es excesiva. Las unidades maximas a devolver son {}".format(quantity_bd)))
            return super(LineInvoiceRectificationCreateModal, self).form_invalid(form)
        # initial invoice rectifications
        if self.__invoice_rectification_pk:
            invoice_rectification = SalesInvoiceRectification.objects.get(pk=self.__invoice_rectification_pk)
            self.request.invoice_rectification = invoice_rectification
            form.instance.invoice_rectification = invoice_rectification

        return super(LineInvoiceRectificationCreateModal, self).form_valid(form)


class LineInvoiceRectificationUpdate(GenLineInvoiceRectificationUrl, GenUpdate):
    model = SalesLineInvoiceRectification
    form_class = LineInvoiceRectificationForm

    def form_valid(self, form):
        # raise Exception(form.initial)
        line_invoice = form.instance.line_invoice
        # sumatorio de las cantidades ya devueltas de la misma linea salvo al actual
        quantity_tmp = SalesLineInvoiceRectification.objects.filter(
            line_invoice=line_invoice
        ).exclude(
            pk=form.initial.get("id")
        ).annotate(
            q=Sum('quantity')
        ).values('q')
        if quantity_tmp:
            quantity_bd = line_invoice.quantity - quantity_tmp[0]['q']
        else:
            quantity_bd = line_invoice.quantity

        # comprobamos que la cantidad correcta
        if quantity_bd < form.instance.quantity:
            errors = form._errors.setdefault("quantity", ErrorList())
            errors.append(_("La cantidad seleccionada es excesiva. Las unidades maximas a devolver son {}".format(quantity_bd)))
            return super(LineInvoiceRectificationUpdate, self).form_invalid(form)

        return super(LineInvoiceRectificationUpdate, self).form_valid(form)


class LineInvoiceRectificationUpdateModal(GenUpdateModal, LineInvoiceRectificationUpdate):
    form_class = LineInvoiceRectificationLinkedForm


class LineInvoiceRectificationDelete(GenLineInvoiceRectificationUrl, GenDelete):
    model = SalesLineInvoiceRectification


class LineInvoiceRectificationSubList(GenLineInvoiceRectificationUrl, GenList):
    model = SalesLineInvoiceRectification
    gentrans = {
        'CreateInvoice': _("Create Invoice leches"),
    }

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(invoice_rectification__pk=pk)
        return limit


class LineInvoiceRectificationDetails(GenLineInvoiceRectificationUrl, GenDetail):
    model = SalesLineInvoiceRectification
    groups = LineInvoiceRectificationForm.__groups_details__()
    exclude_fields = []


class LineInvoiceRectificationDetailModal(GenDetailModal, LineInvoiceRectificationDetails):
    pass


# ###########################################
class GenReservedProduct(object):
    ws_entry_point = '{}/reservedproducts'.format(settings.CDNX_INVOICING_URL_SALES)


# SalesReservedProduct
class ReservedProductList(GenReservedProduct, GenList):
    model = SalesReservedProduct
    extra_context = {'menu': ['SalesReservedProduct', 'people'], 'bread': [_('SalesReservedProduct'), _('People')]}


class ReservedProductCreate(GenReservedProduct, GenCreate):
    model = SalesReservedProduct
    form_class = ReservedProductForm


class ReservedProductUpdate(GenReservedProduct, GenUpdate):
    model = SalesReservedProduct
    form_class = ReservedProductForm


class ReservedProductDelete(GenReservedProduct, GenDelete):
    model = SalesReservedProduct


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
        return JsonResponse(cart.products)

    def post(self, request, *args, **kwargs):
        """
        Adds new product to the current shopping cart
        """
        POST = json.loads(request.body)

        if 'product_pk' in POST and 'quantity' in POST:
            cart = ShoppingCartProxy(request)
            cart.add(
                product_pk=int(POST['product_pk']),
                quantity=int(POST['quantity'])
            )
            return JsonResponse(cart.products)

        return HttpResponseBadRequest()

    def put(self, request, *args, **kwargs):
        PUT = json.loads(request.body)

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
        DELETE = json.loads(request.body)

        if 'product_pk' in DELETE:
            cart = ShoppingCartProxy(request)
            cart.remove(product_pk=int(DELETE['product_pk']))
            return JsonResponse(cart.totals)

        return HttpResponseBadRequest()
