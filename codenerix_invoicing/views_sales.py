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
from django.db.models import Q, Sum, F
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.forms.utils import ErrorList
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View

from django.conf import settings

from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail, GenDetailModal, GenForeignKey
from codenerix.middleware import get_current_user

from codenerix_corporate.models import CorporateImage
from codenerix_extensions.views import GenCreateBridge, GenUpdateBridge
from codenerix_extensions.files.views import DocumentFileView
from codenerix_extensions.helpers import get_language_database
from codenerix_products.models import ProductFinal

from codenerix_invoicing.models_sales import Customer, CustomerDocument, \
    SalesOrder, SalesLineOrder, SalesAlbaran, SalesLineAlbaran, SalesTicket, SalesLineTicket, \
    SalesTicketRectification, SalesLineTicketRectification, SalesInvoice, SalesLineInvoice, SalesInvoiceRectification, \
    SalesLineInvoiceRectification, SalesReservedProduct, SalesBasket, SalesLineBasket
from codenerix_invoicing.models_sales import ROLE_BASKET_SHOPPINGCART, ROLE_BASKET_BUDGET, ROLE_BASKET_WISHLIST, STATUS_ORDER
from codenerix_invoicing.models_sales import SalesLineBasketOption, SalesOrderDocument

from codenerix_invoicing.forms_sales import CustomerForm, CustomerDocumentForm
from codenerix_invoicing.forms_sales import OrderForm, LineOrderForm, LineOrderFormEdit, OrderFromBudgetForm, OrderFromShoppingCartForm
from codenerix_invoicing.forms_sales import AlbaranForm, LineAlbaranForm
from codenerix_invoicing.forms_sales import TicketForm, LineTicketForm
from codenerix_invoicing.forms_sales import TicketRectificationForm, TicketRectificationUpdateForm, LineTicketRectificationLinkedForm, LineTicketRectificationForm
from codenerix_invoicing.forms_sales import InvoiceForm, LineInvoiceForm
from codenerix_invoicing.forms_sales import InvoiceRectificationForm, InvoiceRectificationUpdateForm, LineInvoiceRectificationForm, LineInvoiceRectificationLinkedForm
from codenerix_invoicing.forms_sales import ReservedProductForm
from codenerix_invoicing.forms_sales import BasketForm, LineBasketForm, LineBasketFormPack
from codenerix_invoicing.forms_sales import OrderDocumentForm, OrderDocumentSublistForm

from codenerix_invoicing.views import PrinterHelper

from .models_sales import ReasonModification, ReasonModificationLineBasket, ReasonModificationLineOrder, ReasonModificationLineAlbaran, ReasonModificationLineTicket, ReasonModificationLineTicketRectification, ReasonModificationLineInvoice, ReasonModificationLineInvoiceRectification
from .forms_sales import ReasonModificationForm, ReasonModificationLineBasketForm, ReasonModificationLineOrderForm, ReasonModificationLineAlbaranForm, ReasonModificationLineTicketForm, ReasonModificationLineTicketRectificationForm, ReasonModificationLineInvoiceForm, ReasonModificationLineInvoiceRectificationForm

from .models_sales import PrintCounterDocumentBasket, PrintCounterDocumentOrder, PrintCounterDocumentAlbaran, PrintCounterDocumentTicket, PrintCounterDocumentTicketRectification, PrintCounterDocumentInvoice, PrintCounterDocumentInvoiceRectification

from .helpers import ShoppingCartProxy


# ###########################################
class GenCustomerUrl(object):
    ws_entry_point = '{}/customers'.format(settings.CDNX_INVOICING_URL_SALES)


# Customer
class CustomerList(GenCustomerUrl, GenList):
    model = Customer
    show_details = True
    extra_context = {'menu': ['Customer', 'sales'], 'bread': [_('Customer'), _('Sales')]}
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
        qs = queryset.exclude(basket_sales__order_sales__isnull=False)
        qs = qs.filter(basket_sales__role=ROLE_BASKET_BUDGET)

        return qs.distinct()[:settings.LIMIT_FOREIGNKEY]


class CustomerForeignShoppingCart(GenCustomerUrl, GenForeignKey):
    model = Customer
    label = "{external}"

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
    ws_entry_point = '{}/nshoppingcarts'.format(settings.CDNX_INVOICING_URL_SALES)


class GenBasketBUDGETUrl(object):
    ws_entry_point = '{}/nbudgets'.format(settings.CDNX_INVOICING_URL_SALES)


class GenBasketWISHLISTUrl(object):
    ws_entry_point = '{}/nwishlists'.format(settings.CDNX_INVOICING_URL_SALES)


# SalesBasket
class BasketList(GenList):
    model = SalesBasket
    extra_context = {'menu': ['SalesBasket', 'sales'], 'bread': [_('SalesBasket'), _('Sales')]}
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
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_saleslinebaskets_sublist', 'rows': 'base'},
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
    label = "{code}"

    def get_foreign(self, queryset, search, filters):
        qs = queryset.exclude(order_sales__isnull=False)
        qs = qs.filter(role=ROLE_BASKET_BUDGET)

        qs.filter(customer=filters.get('customer', None))

        return qs[:settings.LIMIT_FOREIGNKEY]


class BasketForeignShoppingCart(GenBasketSHOPPINGCARTUrl, GenForeignKey):
    model = SalesBasket
    label = "{code}"

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
        list_lines = ast.literal_eval(request._body.decode())['lines']
        context = SalesLineBasket.create_order_from_budget(pk, list_lines)
        try:
            context['obj_final'] = None
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
        list_budget = ast.literal_eval(request._body.decode())['lines']
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
                        lo.price_base = lb.price_base
                        lo.tax = lb.tax
                        lo.save()

                context['msg'] = _("Order create")
                # context['url'] = reverse('ordersaless_details', kwargs={'pk': order.pk})
                context['url'] = "{}#/{}".format(reverse('CDNX_invoicing_ordersaless_list'), order.pk)
            else:
                context['error'] = _("Hay lineas asignadas a pedidos")
        else:
            context['error'] = _('Budget not found')

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
    extra_context = {'menu': ['SalesLineBasket', 'sales'], 'bread': [_('SalesLineBasket'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
        limit['removed'] = Q(removed=False)
        return limit


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


class LineBasketCreateModalPack(GenCreateModal, LineBasketCreate):
    form_class = LineBasketFormPack

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineBasketCreateModalPack, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        product_pk = self.request.POST.get("product", None)
        quantity = self.request.POST.get("quantity", None)
        product = ProductFinal.objects.filter(pk=product_pk).first()
        if product and quantity:
            if product.is_pack():
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
                            return super(LineBasketCreateModalPack, self).form_invalid(form)
                    else:
                        errors = form._errors.setdefault(field, ErrorList())
                        errors.append(_("Option invalid"))
                        return super(LineBasketCreateModalPack, self).form_invalid(form)
            else:
                errors = form._errors.setdefault("product", ErrorList())
                errors.append(_("The product does not pack"))
                return super(LineBasketCreateModalPack, self).form_invalid(form)
        else:
            errors = form._errors.setdefault("product", ErrorList())
            errors.append(_("Product invalid"))
            return super(LineBasketCreateModalPack, self).form_invalid(form)

        if self.__pk:
            obj = SalesBasket.objects.get(pk=self.__pk)
            self.request.basket = obj
            form.instance.basket = obj
        ret = super(LineBasketCreateModalPack, self).form_valid(form)
        # raise Exception(ret)
        # raise Exception(self.object, type(self.object), isinstance(self.object, SalesLineBasket), self.object.__dict__)
        self.object.set_options(options_pack)
        return ret


class LineBasketUpdate(GenLineBasketUrl, GenUpdate):
    model = SalesLineBasket
    form_class = LineBasketForm


class ZZZ___LineBasketUpdateModal(GenUpdateModal, LineBasketUpdate):
    pass


class LineBasketUpdateModal(GenUpdateModal, LineBasketUpdate):
    form_class = LineBasketForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__line_pk = kwargs.get('pk', None)
        if SalesLineBasketOption.objects.filter(line_budget__pk=self.__line_pk).exists():
            self.form_class = LineBasketFormPack
            self.__is_pack = True
        else:
            self.__is_pack = False
        return super(LineBasketUpdateModal, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        # form_kwargs = super(LineBasketUpdateModal, self).get_form_kwargs(*args, **kwargs)
        form = super(LineBasketUpdateModal, self).get_form(form_class)
        initial = form.initial
        initial['type_tax'] = self.object.product.product.tax.pk
        initial['price'] = self.object.total
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
        return form

    def form_valid(self, form):
        lb = SalesLineBasket.objects.filter(pk=self.__line_pk).first()

        product_old = lb.product
        product_pk = self.request.POST.get("product", None)
        quantity = self.request.POST.get("quantity", None)
        product = ProductFinal.objects.filter(pk=product_pk).first()
        if product:
            is_pack = product.is_pack()
        else:
            is_pack = False
        if product and quantity:
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
                            return super(LineBasketUpdateModal, self).form_invalid(form)
                    else:
                        errors = form._errors.setdefault(field, ErrorList())
                        errors.append(_("Option invalid"))
                        return super(LineBasketUpdateModal, self).form_invalid(form)
        else:
            errors = form._errors.setdefault("product", ErrorList())
            errors.append(_("Product invalid"))
            return super(LineBasketUpdateModal, self).form_invalid(form)

        ret = super(LineBasketUpdateModal, self).form_valid(form)
        if product_old != self.object.product:
            self.object.remove_options()
        if is_pack:
            self.object.set_options(options_pack)
        return ret


class LineBasketDelete(GenLineBasketUrl, GenDelete):
    model = SalesLineBasket


class LineBasketSubList(GenLineBasketUrl, GenList):
    model = SalesLineBasket
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

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = SalesBasket.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            self.linkadd = True
            self.linkedit = True
            self.field_delete = True
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
        limit['removed'] = Q(removed=False)
        return limit


class LineBasketDetails(GenLineBasketUrl, GenDetail):
    model = SalesLineBasket
    groups = LineBasketForm.__groups_details__()


class LineBasketDetailModal(GenDetailModal, LineBasketDetails):
    pass


class LineBasketForeign(GenLineBasketUrl, GenForeignKey):
    model = SalesLineBasket
    label = "{product}: {quantity}"

    def get_foreign(self, queryset, search, filters):
        qsobject = Q(description__icontains=search)
        qs = queryset.filter(qsobject)
        doc = filters.get('doc', None)
        if doc:
            qs = qs.filter(basket__pk=doc)

        return qs


# ###########################################
class GenOrderUrl(object):
    ws_entry_point = '{}/orders'.format(settings.CDNX_INVOICING_URL_SALES)


# Order
class OrderList(GenOrderUrl, GenList):
    model = SalesOrder
    template_model = "sales/order_list.html"
    show_details = True
    linkadd = False
    extra_context = {'menu': ['sales_order', 'sales'], 'bread': [_('Sales orders'), _('Sales')]}
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
        if SalesLineBasket.create_order_from_budget_all(self.object):
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
            first=None
            last=None
            for (key, label) in STATUS_ORDER:
                if not first:
                    first=key
                elif so.status_order == last:
                    so.status_order = key
                    so.save()
                    answer['changed']=True
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
        total_order = 0
        for line in order.line_order_sales.all():
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
        if order.budget.address_invoice:
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
        raise Exception("get")

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        list_lines = ast.literal_eval(request._body.decode())['lines']
        try:
            context = SalesLineOrder.create_albaran_from_order(pk, list_lines)
            context.pop('obj_final')
            json_answer = json.dumps(context)
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
        list_lines = ast.literal_eval(request._body.decode())['lines']
        try:
            context = SalesLineOrder.create_ticket_from_order(pk, list_lines)
            context.pop('obj_final')
            json_answer = json.dumps(context)
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
        list_lines = ast.literal_eval(request._body.decode())['lines']
        try:
            context = SalesLineOrder.create_invoice_from_order(pk, list_lines)
            context.pop('obj_final')
            json_answer = json.dumps(context)
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
    extra_context = {'menu': ['LineOrder', 'sales'], 'bread': [_('LineOrder'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
        limit['removed'] = Q(removed=False)
        return limit


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
    form_class = LineOrderFormEdit

    def form_valid(self, form):
        reason = form.data['reason']
        if reason:
            reason_obj = ReasonModification.objects.filter(pk=reason).first()
            if reason_obj:
                try:
                    with transaction.atomic():
                        result = super(LineOrderUpdate, self).form_valid(form)

                        reason_order = ReasonModificationLineOrder()
                        reason_order.reason = reason_obj
                        reason_order.line = self.object
                        reason_order.user = get_current_user()
                        reason_order.quantity = self.object.quantity
                        reason_order.save()
                        return result
                except Exception as e:
                    errors = form._errors.setdefault("other", ErrorList())
                    errors.append(e)
                    return super(LineOrderUpdate, self).form_invalid(form)
            else:
                errors = form._errors.setdefault("reason", ErrorList())
                errors.append(_("Reason of modification invalid"))
                return super(LineOrderUpdate, self).form_invalid(form)
        else:
            errors = form._errors.setdefault("reason", ErrorList())
            errors.append(_("Reason of modification invalid"))
            return super(LineOrderUpdate, self).form_invalid(form)


class LineOrderUpdateModal(GenUpdateModal, LineOrderUpdate):
    pass


class LineOrderDelete(GenLineOrderUrl, GenDelete):
    model = SalesLineOrder


class LineOrderSubList(GenLineOrderUrl, GenList):
    model = SalesLineOrder
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

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = SalesOrder.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            self.linkadd = True
            self.linkedit = True
            self.field_delete = True

        self.__btn_invoice = getattr(settings, 'CDNX_INVOICING_ORDER_BTN_INVOICE', True)
        self.__btn_ticket = getattr(settings, 'CDNX_INVOICING_ORDER_BTN_TICKET', True)
        self.__btn_albaran = getattr(settings, 'CDNX_INVOICING_ORDER_BTN_ALBARAN', True)
        if self.__btn_invoice is False and self.__btn_ticket is False and self.__btn_albaran is False:
            self.field_check = None
        return super(LineOrderSubList, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(order__pk=pk)
        limit['removed'] = Q(removed=False)
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

    def get_context_json(self, context):
        answer = super(LineOrderSubList, self).get_context_json(context)
        answer['meta']['btn_invoice'] = self.__btn_invoice
        answer['meta']['btn_ticket'] = self.__btn_ticket
        answer['meta']['btn_albaran'] = self.__btn_albaran
        return answer


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

        order_pk = filters.get('doc', None)
        if order_pk:
            qs = qs.filter(order__pk=order_pk)
        return qs[:settings.LIMIT_FOREIGNKEY]


class LineOrderForeignCustom(GenLineOrderUrl, GenForeignKey):
    model = SalesLineOrder
    label = "{product} - {quantity}"

    def get(self, request, *args, **kwargs):
        search = kwargs.get('search', None)

        filterstxt = self.request.GET.get('filter', '{}')
        filters = json.loads(filterstxt.decode('utf-8'))

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
        answer['clear'] = ['price_base', 'discount']
        answer['readonly'] = ['price_base', 'discount']
        answer['rows'].append({
            'price_base': 0,
            'description': "",
            'discount': 0,
            'label': "---------",
            'id': None,
        })
        for product in queryset[:settings.LIMIT_FOREIGNKEY]:
            answer['rows'].append({
                'price_base': product.price_base,
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
class GenOrderDocumentUrl(object):
    ws_entry_point = '{}/orderdocuments'.format(settings.CDNX_INVOICING_URL_SALES)


# OrderDocument
class OrderDocumentList(GenOrderDocumentUrl, GenList):
    model = SalesOrderDocument
    extra_context = {'menu': ['OrderDocument', 'sales'], 'bread': [_('OrderDocument'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
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


class OrderDocumentSubList(GenOrderDocumentUrl, GenList):
    model = SalesOrderDocument
    extra_context = {'menu': ['SalesOrderDocument', 'sales'], 'bread': [_('SalesOrderDocument'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(order__pk=pk)
        limit['removed'] = Q(order__removed=False)
        return limit


class OrderDocumentDetails(GenDetail):
    model = SalesOrderDocument
    groups = OrderDocumentForm.__groups_details__()


class OrderDocumentDetailModal(GenDetailModal, OrderDocumentDetails):
    pass


# ###########################################
class GenAlbaranUrl(object):
    ws_entry_point = '{}/albarans'.format(settings.CDNX_INVOICING_URL_SALES)


# Albaran
class AlbaranList(GenAlbaranUrl, GenList):
    model = SalesAlbaran
    show_details = True
    template_model = "sales/albaran_list.html"
    extra_context = {'menu': ['Albaran', 'sales'], 'bread': [_('Albaran'), _('Sales')]}
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
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_linealbaransaless_sublist', 'rows': 'base'},
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
        list_lines = ast.literal_eval(request._body.decode())['lines']
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
    extra_context = {'menu': ['LineAlbaran', 'sales'], 'bread': [_('LineAlbaran'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
        limit['removed'] = Q(removed=False)
        return limit


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
    field_delete = False
    field_check = False
    ngincludes = {"table": "/static/codenerix_invoicing/partials/sales/table_linealbaran.html"}
    gentrans = {
        'CreateTicket': _("Create Ticket"),
        'CreateInvoice': _("Create Invoice"),
    }
    linkadd = False
    linkedit = False

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = SalesAlbaran.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            self.linkadd = True
            self.linkedit = True
            self.field_delete = True
        return super(LineAlbaranSubList, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(albaran__pk=pk)
        limit['removed'] = Q(removed=False)
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


class LineAlbaranForeign(GenLineAlbaranUrl, GenForeignKey):
    model = SalesLineAlbaran
    label = "{product} - {quantity}"

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(description__icontains=search)
        qs = queryset.filter(qsobject)

        order_pk = filters.get('doc', None)
        if order_pk:
            qs = qs.filter(albaran__pk=order_pk)
        return qs


# ###########################################
class GenTicketUrl(object):
    ws_entry_point = '{}/tickets'.format(settings.CDNX_INVOICING_URL_SALES)


# Ticket
class TicketList(GenTicketUrl, GenList):
    model = SalesTicket
    show_details = True
    template_model = "sales/ticket_list.html"
    extra_context = {'menu': ['Ticket', 'sales'], 'bread': [_('Ticket'), _('Sales')]}
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
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_lineticketsaless_sublist', 'rows': 'base'},
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

        list_lines = ast.literal_eval(request._body.decode())['lines']
        list_lines = [int(x) for x in list_lines]

        context = {}
        if list_lines and pk and ticket:
            tr = SalesTicketRectification()
            tr.date = datetime.datetime.now()
            tr.ticket = ticket
            tr.billing_series = ticket.billing_series
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
    extra_context = {'menu': ['LineTicket', 'sales'], 'bread': [_('LineTicket'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
        limit['removed'] = Q(removed=False)
        return limit


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
        return super(LineTicketSubList, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(ticket__pk=pk)
        limit['removed'] = Q(removed=False)
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

        doc = filters.get('doc', None)
        if doc:
            qs = qs.filter(ticket__pk=doc)

        return qs[:settings.LIMIT_FOREIGNKEY]


# ###########################################
class GenTicketRectificationUrl(object):
    ws_entry_point = '{}/ticketrectifications'.format(settings.CDNX_INVOICING_URL_SALES)


# TicketRectification
class TicketRectificationList(GenTicketRectificationUrl, GenList):
    model = SalesTicketRectification
    show_details = True
    extra_context = {'menu': ['TicketRectification', 'sales'], 'bread': [_('TicketRectification'), _('Sales')]}
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
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_lineticketrectificationsaless_sublist', 'rows': 'base'},
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
class GenLineTicketRectificationUrl(object):
    ws_entry_point = '{}/lineticketrectifications'.format(settings.CDNX_INVOICING_URL_SALES)


# LineTicketRectification
class LineTicketRectificationList(GenLineTicketRectificationUrl, GenList):
    model = SalesLineTicketRectification
    extra_context = {'menu': ['LineTicketRectification', 'sales'], 'bread': [_('LineTicketRectification'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
        limit['removed'] = Q(removed=False)
        return limit


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
    linkadd = False
    linkedit = False

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = SalesTicketRectification.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            self.linkadd = True
            self.linkedit = True
        return super(LineTicketRectificationSubList, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(ticket_rectification__pk=pk)
        limit['removed'] = Q(removed=False)
        return limit


class LineTicketRectificationDetails(GenLineTicketRectificationUrl, GenDetail):
    model = SalesLineTicketRectification
    groups = LineTicketRectificationForm.__groups_details__()
    exclude_fields = []


class LineTicketRectificationDetailModal(GenDetailModal, LineTicketRectificationDetails):
    pass


class LineTicketRectificationForeign(GenLineTicketRectificationUrl, GenForeignKey):
    model = SalesLineTicket
    label = "{description} - {quantity}"

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(description__icontains=search)
        qs = queryset.filter(qsobject)

        doc = filters.get('doc', None)
        if doc:
            qs = qs.filter(ticket_rectification__pk=doc)

        return qs[:settings.LIMIT_FOREIGNKEY]


# ###########################################
class GenInvoiceUrl(object):
    ws_entry_point = '{}/invoices'.format(settings.CDNX_INVOICING_URL_SALES)


# Invoice
class InvoiceList(GenInvoiceUrl, GenList):
    model = SalesInvoice
    show_details = True
    template_model = "sales/invoice_list.html"
    extra_context = {'menu': ['Invoice', 'sales'], 'bread': [_('Invoice'), _('Sales')]}
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
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_lineinvoicesaless_sublist', 'rows': 'base'},
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
class GenLineInvoiceUrl(object):
    ws_entry_point = '{}/lineinvoices'.format(settings.CDNX_INVOICING_URL_SALES)


# LineInvoice
class LineInvoiceList(GenLineInvoiceUrl, GenList):
    model = SalesLineInvoice
    extra_context = {'menu': ['LineInvoice', 'sales'], 'bread': [_('LineInvoice'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
        limit['removed'] = Q(removed=False)
        return limit


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
            errors.append(_("La cantidad seleccionada es excesiva. Quedan pendiente {} unidades por facturar".format(units_pending)))
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
    linkadd = False
    linkedit = False

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        obj = SalesInvoice.objects.filter(pk=self.__pk).first()
        if obj and not obj.lock:
            self.linkadd = True
            self.linkedit = True
        return super(LineInvoiceSubList, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(invoice__pk=pk)
        limit['removed'] = Q(removed=False)
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

        doc = filters.get('doc', None)
        if doc:
            qs = qs.filter(invoice__pk=doc)
        return qs[:settings.LIMIT_FOREIGNKEY]


# ###########################################
class GenInvoiceRectificationUrl(object):
    ws_entry_point = '{}/invoicerectifications'.format(settings.CDNX_INVOICING_URL_SALES)


# InvoiceRectification
class InvoiceRectificationList(GenInvoiceRectificationUrl, GenList):
    model = SalesInvoiceRectification
    show_details = True
    extra_context = {'menu': ['InvoiceRectification', 'sales'], 'bread': [_('InvoiceRectification'), _('Sales')]}
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
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_lineinvoicerectificationsaless_sublist', 'rows': 'base'},
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


# ###########################################
class GenLineInvoiceRectificationUrl(object):
    ws_entry_point = '{}/lineinvoicerectifications'.format(settings.CDNX_INVOICING_URL_SALES)


# LineInvoiceRectification
class LineInvoiceRectificationList(GenLineInvoiceRectificationUrl, GenList):
    model = SalesLineInvoiceRectification
    extra_context = {'menu': ['LineInvoiceRectification', 'sales'], 'bread': [_('LineInvoiceRectification'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
        limit['removed'] = Q(removed=False)
        return limit


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
        return super(LineInvoiceRectificationSubList, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(invoice_rectification__pk=pk)
        limit['removed'] = Q(removed=False)
        return limit


class LineInvoiceRectificationDetails(GenLineInvoiceRectificationUrl, GenDetail):
    model = SalesLineInvoiceRectification
    groups = LineInvoiceRectificationForm.__groups_details__()
    exclude_fields = []


class LineInvoiceRectificationDetailModal(GenDetailModal, LineInvoiceRectificationDetails):
    pass


class LineInvoiceRectificationForeign(GenLineInvoiceRectificationUrl, GenForeignKey):
    model = SalesLineInvoiceRectification
    label = "{description} - {quantity}"

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(description__icontains=search)
        qs = queryset.filter(qsobject)

        doc = filters.get('doc', None)
        if doc:
            qs = qs.filter(invoice_rectification__pk=doc)
        return qs[:settings.LIMIT_FOREIGNKEY]


# ###########################################
class GenReservedProduct(object):
    ws_entry_point = '{}/reservedproducts'.format(settings.CDNX_INVOICING_URL_SALES)


# SalesReservedProduct
class ReservedProductList(GenReservedProduct, GenList):
    model = SalesReservedProduct
    extra_context = {'menu': ['SalesReservedProduct', 'sales'], 'bread': [_('SalesReservedProduct'), _('Sales')]}
    default_ordering = "-created"


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
    extra_context = {'menu': ['ReasonModification', 'sales'], 'bread': [_('ReasonModification'), _('Sales')]}


class ReasonModificationDetails(GenDetail):
    model = ReasonModification
    groups = ReasonModificationForm.__groups_details__()


class ReasonModificationDetailModal(GenDetailModal, ReasonModificationDetails):
    pass


# ###########################################
# ReasonModificationLineBasket
class ReasonModificationLineBasketList(GenList):
    model = ReasonModificationLineBasket
    extra_context = {'menu': ['sales', 'ReasonModificationLineBasket'], 'bread': [_('Sales'), _('ReasonModificationLineBasket')]}


class ReasonModificationLineBasketCreate(GenCreate):
    model = ReasonModificationLineBasket
    form_class = ReasonModificationLineBasketForm

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(ReasonModificationLineBasketCreate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ReasonModificationLineBasketCreate, self).get_form(form_class)
        obj = SalesBasket.objects.filter(pk=self.__pk).first()
        if obj:
            form.fields['doc'].initial = obj.pk
        return form

    def form_valid(self, form):
        user = get_current_user()
        form.instance.user = user
        self.request.user = user
        return super(ReasonModificationLineBasketCreate, self).form_valid(form)


class ReasonModificationLineBasketCreateModal(GenCreateModal, ReasonModificationLineBasketCreate):
    pass


class ReasonModificationLineBasketUpdate(GenUpdate):
    model = ReasonModificationLineBasket
    form_class = ReasonModificationLineBasketForm

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(ReasonModificationLineBasketUpdate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ReasonModificationLineBasketUpdate, self).get_form(form_class)
        obj = SalesBasket.objects.filter(pk=self.__pk).first()
        if obj:
            form.fields['doc'].initial = obj.pk
        return form

    def form_valid(self, form):
        user = get_current_user()
        form.instance.user = user
        self.request.user = user
        return super(ReasonModificationLineBasketUpdate, self).form_valid(form)


class ReasonModificationLineBasketUpdateModal(GenUpdateModal, ReasonModificationLineBasketUpdate):
    pass


class ReasonModificationLineBasketDelete(GenDelete):
    model = ReasonModificationLineBasket


class ReasonModificationLineBasketSubList(GenList):
    model = ReasonModificationLineBasket
    extra_context = {'menu': ['ReasonModificationLineBasket', 'sales'], 'bread': [_('ReasonModificationLineBasket'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(line__basket__pk=pk)
        return limit


class ReasonModificationLineBasketDetails(GenDetail):
    model = ReasonModificationLineBasket
    groups = ReasonModificationLineBasketForm.__groups_details__()


class ReasonModificationLineBasketDetailModal(GenDetailModal, ReasonModificationLineBasketDetails):
    pass


# ###########################################
# ReasonModificationLineOrder
class ReasonModificationLineOrderList(GenList):
    model = ReasonModificationLineOrder
    extra_context = {'menu': ['sales', 'ReasonModificationLineOrder'], 'bread': [_('Sales'), _('ReasonModificationLineOrder')]}


class ReasonModificationLineOrderCreate(GenCreate):
    model = ReasonModificationLineOrder
    form_class = ReasonModificationLineOrderForm

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(ReasonModificationLineOrderCreate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ReasonModificationLineOrderCreate, self).get_form(form_class)
        obj = SalesOrder.objects.filter(pk=self.__pk).first()
        if obj:
            form.fields['doc'].initial = obj.pk
        return form

    def form_valid(self, form):
        user = get_current_user()
        form.instance.user = user
        self.request.user = user
        return super(ReasonModificationLineOrderCreate, self).form_valid(form)


class ReasonModificationLineOrderCreateModal(GenCreateModal, ReasonModificationLineOrderCreate):
    pass


class ReasonModificationLineOrderUpdate(GenUpdate):
    model = ReasonModificationLineOrder
    form_class = ReasonModificationLineOrderForm

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(ReasonModificationLineOrderUpdate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ReasonModificationLineOrderUpdate, self).get_form(form_class)
        obj = SalesOrder.objects.filter(pk=self.__pk).first()
        if obj:
            form.fields['doc'].initial = obj.pk
        return form

    def form_valid(self, form):
        user = get_current_user()
        form.instance.user = user
        self.request.user = user
        return super(ReasonModificationLineOrderUpdate, self).form_valid(form)


class ReasonModificationLineOrderUpdateModal(GenUpdateModal, ReasonModificationLineOrderUpdate):
    pass


class ReasonModificationLineOrderDelete(GenDelete):
    model = ReasonModificationLineOrder


class ReasonModificationLineOrderSubList(GenList):
    model = ReasonModificationLineOrder
    extra_context = {'menu': ['ReasonModificationLineOrder', 'sales'], 'bread': [_('ReasonModificationLineOrder'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(line__order__pk=pk)
        return limit


class ReasonModificationLineOrderDetails(GenDetail):
    model = ReasonModificationLineOrder
    groups = ReasonModificationLineOrderForm.__groups_details__()


class ReasonModificationLineOrderDetailModal(GenDetailModal, ReasonModificationLineOrderDetails):
    pass


# ###########################################
# ReasonModificationLineAlbaran
class ReasonModificationLineAlbaranList(GenList):
    model = ReasonModificationLineAlbaran
    extra_context = {'menu': ['sales', 'ReasonModificationLineAlbaran'], 'bread': [_('Sales'), _('ReasonModificationLineAlbaran')]}


class ReasonModificationLineAlbaranCreate(GenCreate):
    model = ReasonModificationLineAlbaran
    form_class = ReasonModificationLineAlbaranForm

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(ReasonModificationLineAlbaranCreate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ReasonModificationLineAlbaranCreate, self).get_form(form_class)
        obj = SalesAlbaran.objects.filter(pk=self.__pk).first()
        if obj:
            form.fields['doc'].initial = obj.pk
        return form

    def form_valid(self, form):
        user = get_current_user()
        form.instance.user = user
        self.request.user = user
        return super(ReasonModificationLineAlbaranCreate, self).form_valid(form)


class ReasonModificationLineAlbaranCreateModal(GenCreateModal, ReasonModificationLineAlbaranCreate):
    pass


class ReasonModificationLineAlbaranUpdate(GenUpdate):
    model = ReasonModificationLineAlbaran
    form_class = ReasonModificationLineAlbaranForm

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(ReasonModificationLineAlbaranUpdate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ReasonModificationLineAlbaranUpdate, self).get_form(form_class)
        obj = SalesAlbaran.objects.filter(pk=self.__pk).first()
        if obj:
            form.fields['doc'].initial = obj.pk
        return form

    def form_valid(self, form):
        user = get_current_user()
        form.instance.user = user
        self.request.user = user
        return super(ReasonModificationLineAlbaranUpdate, self).form_valid(form)


class ReasonModificationLineAlbaranUpdateModal(GenUpdateModal, ReasonModificationLineAlbaranUpdate):
    pass


class ReasonModificationLineAlbaranDelete(GenDelete):
    model = ReasonModificationLineAlbaran


class ReasonModificationLineAlbaranSubList(GenList):
    model = ReasonModificationLineAlbaran
    extra_context = {'menu': ['ReasonModificationLineAlbaran', 'sales'], 'bread': [_('ReasonModificationLineAlbaran'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(line__albaran__pk=pk)
        return limit


class ReasonModificationLineAlbaranDetails(GenDetail):
    model = ReasonModificationLineAlbaran
    groups = ReasonModificationLineAlbaranForm.__groups_details__()


class ReasonModificationLineAlbaranDetailModal(GenDetailModal, ReasonModificationLineAlbaranDetails):
    pass


# ###########################################
# ReasonModificationLineTicket
class ReasonModificationLineTicketList(GenList):
    model = ReasonModificationLineTicket
    extra_context = {'menu': ['sales', 'ReasonModificationLineTicket'], 'bread': [_('Sales'), _('ReasonModificationLineTicket')]}


class ReasonModificationLineTicketCreate(GenCreate):
    model = ReasonModificationLineTicket
    form_class = ReasonModificationLineTicketForm

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(ReasonModificationLineTicketCreate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ReasonModificationLineTicketCreate, self).get_form(form_class)
        obj = SalesTicket.objects.filter(pk=self.__pk).first()
        if obj:
            form.fields['doc'].initial = obj.pk
        return form

    def form_valid(self, form):
        user = get_current_user()
        form.instance.user = user
        self.request.user = user
        return super(ReasonModificationLineTicketCreate, self).form_valid(form)


class ReasonModificationLineTicketCreateModal(GenCreateModal, ReasonModificationLineTicketCreate):
    pass


class ReasonModificationLineTicketUpdate(GenUpdate):
    model = ReasonModificationLineTicket
    form_class = ReasonModificationLineTicketForm

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(ReasonModificationLineTicketUpdate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ReasonModificationLineTicketUpdate, self).get_form(form_class)
        obj = SalesTicket.objects.filter(pk=self.__pk).first()
        if obj:
            form.fields['doc'].initial = obj.pk
        return form

    def form_valid(self, form):
        user = get_current_user()
        form.instance.user = user
        self.request.user = user
        return super(ReasonModificationLineTicketUpdate, self).form_valid(form)


class ReasonModificationLineTicketUpdateModal(GenUpdateModal, ReasonModificationLineTicketUpdate):
    pass


class ReasonModificationLineTicketDelete(GenDelete):
    model = ReasonModificationLineTicket


class ReasonModificationLineTicketSubList(GenList):
    model = ReasonModificationLineTicket
    extra_context = {'menu': ['ReasonModificationLineTicket', 'sales'], 'bread': [_('ReasonModificationLineTicket'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(line__ticket__pk=pk)
        return limit


class ReasonModificationLineTicketDetails(GenDetail):
    model = ReasonModificationLineTicket
    groups = ReasonModificationLineTicketForm.__groups_details__()


class ReasonModificationLineTicketDetailModal(GenDetailModal, ReasonModificationLineTicketDetails):
    pass


# ###########################################
# ReasonModificationLineTicketRectification
class ReasonModificationLineTicketRectificationList(GenList):
    model = ReasonModificationLineTicketRectification
    extra_context = {'menu': ['sales', 'ReasonModificationLineTicketRectification'], 'bread': [_('Sales'), _('ReasonModificationLineTicketRectification')]}


class ReasonModificationLineTicketRectificationCreate(GenCreate):
    model = ReasonModificationLineTicketRectification
    form_class = ReasonModificationLineTicketRectificationForm

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(ReasonModificationLineTicketRectificationCreate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ReasonModificationLineTicketRectificationCreate, self).get_form(form_class)
        obj = SalesTicketRectification.objects.filter(pk=self.__pk).first()
        if obj:
            form.fields['doc'].initial = obj.pk
        return form

    def form_valid(self, form):
        user = get_current_user()
        form.instance.user = user
        self.request.user = user
        return super(ReasonModificationLineTicketRectificationCreate, self).form_valid(form)


class ReasonModificationLineTicketRectificationCreateModal(GenCreateModal, ReasonModificationLineTicketRectificationCreate):
    pass


class ReasonModificationLineTicketRectificationUpdate(GenUpdate):
    model = ReasonModificationLineTicketRectification
    form_class = ReasonModificationLineTicketRectificationForm

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(ReasonModificationLineTicketRectificationUpdate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ReasonModificationLineTicketRectificationUpdate, self).get_form(form_class)
        obj = SalesTicketRectification.objects.filter(pk=self.__pk).first()
        if obj:
            form.fields['doc'].initial = obj.pk
        return form

    def form_valid(self, form):
        user = get_current_user()
        form.instance.user = user
        self.request.user = user
        return super(ReasonModificationLineTicketRectificationUpdate, self).form_valid(form)


class ReasonModificationLineTicketRectificationUpdateModal(GenUpdateModal, ReasonModificationLineTicketRectificationUpdate):
    pass


class ReasonModificationLineTicketRectificationDelete(GenDelete):
    model = ReasonModificationLineTicketRectification


class ReasonModificationLineTicketRectificationSubList(GenList):
    model = ReasonModificationLineTicketRectification
    extra_context = {'menu': ['ReasonModificationLineTicketRectification', 'sales'], 'bread': [_('ReasonModificationLineTicketRectification'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(line__ticket_rectification__pk=pk)
        return limit


class ReasonModificationLineTicketRectificationDetails(GenDetail):
    model = ReasonModificationLineTicketRectification
    groups = ReasonModificationLineTicketRectificationForm.__groups_details__()


class ReasonModificationLineTicketRectificationDetailModal(GenDetailModal, ReasonModificationLineTicketRectificationDetails):
    pass


# ###########################################
# ReasonModificationLineInvoice
class ReasonModificationLineInvoiceList(GenList):
    model = ReasonModificationLineInvoice
    extra_context = {'menu': ['sales', 'ReasonModificationLineInvoice'], 'bread': [_('Sales'), _('ReasonModificationLineInvoice')]}


class ReasonModificationLineInvoiceCreate(GenCreate):
    model = ReasonModificationLineInvoice
    form_class = ReasonModificationLineInvoiceForm

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(ReasonModificationLineInvoiceCreate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ReasonModificationLineInvoiceCreate, self).get_form(form_class)
        obj = SalesInvoice.objects.filter(pk=self.__pk).first()
        if obj:
            form.fields['doc'].initial = obj.pk
        return form

    def form_valid(self, form):
        user = get_current_user()
        form.instance.user = user
        self.request.user = user
        return super(ReasonModificationLineInvoiceCreate, self).form_valid(form)


class ReasonModificationLineInvoiceCreateModal(GenCreateModal, ReasonModificationLineInvoiceCreate):
    pass


class ReasonModificationLineInvoiceUpdate(GenUpdate):
    model = ReasonModificationLineInvoice
    form_class = ReasonModificationLineInvoiceForm

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(ReasonModificationLineInvoiceUpdate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ReasonModificationLineInvoiceUpdate, self).get_form(form_class)
        obj = SalesInvoice.objects.filter(pk=self.__pk).first()
        if obj:
            form.fields['doc'].initial = obj.pk
        return form

    def form_valid(self, form):
        user = get_current_user()
        form.instance.user = user
        self.request.user = user
        return super(ReasonModificationLineInvoiceUpdate, self).form_valid(form)


class ReasonModificationLineInvoiceUpdateModal(GenUpdateModal, ReasonModificationLineInvoiceUpdate):
    pass


class ReasonModificationLineInvoiceDelete(GenDelete):
    model = ReasonModificationLineInvoice


class ReasonModificationLineInvoiceSubList(GenList):
    model = ReasonModificationLineInvoice
    extra_context = {'menu': ['ReasonModificationLineInvoice', 'sales'], 'bread': [_('ReasonModificationLineInvoice'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(invoice__pk=pk)
        return limit


class ReasonModificationLineInvoiceDetails(GenDetail):
    model = ReasonModificationLineInvoice
    groups = ReasonModificationLineInvoiceForm.__groups_details__()


class ReasonModificationLineInvoiceDetailModal(GenDetailModal, ReasonModificationLineInvoiceDetails):
    pass


# ###########################################
# ReasonModificationLineInvoiceRectification
class ReasonModificationLineInvoiceRectificationList(GenList):
    model = ReasonModificationLineInvoiceRectification
    extra_context = {'menu': ['sales', 'ReasonModificationLineInvoiceRectification'], 'bread': [_('Sales'), _('ReasonModificationLineInvoiceRectification')]}


class ReasonModificationLineInvoiceRectificationCreate(GenCreate):
    model = ReasonModificationLineInvoiceRectification
    form_class = ReasonModificationLineInvoiceRectificationForm

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(ReasonModificationLineInvoiceRectificationCreate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ReasonModificationLineInvoiceRectificationCreate, self).get_form(form_class)
        obj = SalesInvoiceRectification.objects.filter(pk=self.__pk).first()
        if obj:
            form.fields['doc'].initial = obj.pk
        return form

    def form_valid(self, form):
        user = get_current_user()
        form.instance.user = user
        self.request.user = user
        return super(ReasonModificationLineInvoiceRectificationCreate, self).form_valid(form)


class ReasonModificationLineInvoiceRectificationCreateModal(GenCreateModal, ReasonModificationLineInvoiceRectificationCreate):
    pass


class ReasonModificationLineInvoiceRectificationUpdate(GenUpdate):
    model = ReasonModificationLineInvoiceRectification
    form_class = ReasonModificationLineInvoiceRectificationForm

    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(ReasonModificationLineInvoiceRectificationUpdate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ReasonModificationLineInvoiceRectificationUpdate, self).get_form(form_class)
        obj = SalesInvoiceRectification.objects.filter(pk=self.__pk).first()
        if obj:
            form.fields['doc'].initial = obj.pk
        return form

    def form_valid(self, form):
        user = get_current_user()
        form.instance.user = user
        self.request.user = user
        return super(ReasonModificationLineInvoiceRectificationUpdate, self).form_valid(form)


class ReasonModificationLineInvoiceRectificationUpdateModal(GenUpdateModal, ReasonModificationLineInvoiceRectificationUpdate):
    pass


class ReasonModificationLineInvoiceRectificationDelete(GenDelete):
    model = ReasonModificationLineInvoiceRectification


class ReasonModificationLineInvoiceRectificationSubList(GenList):
    model = ReasonModificationLineInvoiceRectification
    extra_context = {'menu': ['ReasonModificationLineInvoiceRectification', 'sales'], 'bread': [_('ReasonModificationLineInvoiceRectification'), _('Sales')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(invoice_rectification__pk=pk)
        return limit


class ReasonModificationLineInvoiceRectificationDetails(GenDetail):
    model = ReasonModificationLineInvoiceRectification
    groups = ReasonModificationLineInvoiceRectificationForm.__groups_details__()


class ReasonModificationLineInvoiceRectificationDetailModal(GenDetailModal, ReasonModificationLineInvoiceRectificationDetails):
    pass


# ###########################################
# PrintCounterDocumentBasket
class PrintCounterDocumentBasketSublist(GenList):
    model = PrintCounterDocumentBasket
    extra_context = {'menu': ['ReasonModificationLineInvoiceRectification', 'sales'], 'bread': [_('ReasonModificationLineInvoiceRectification'), _('Sales')]}
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
    extra_context = {'menu': ['PrintCounterDocumentOrder', 'sales'], 'bread': [_('PrintCounterDocumentOrder'), _('Sales')]}
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
    extra_context = {'menu': ['PrintCounterDocumentAlbaran', 'sales'], 'bread': [_('PrintCounterDocumentAlbaran'), _('Sales')]}
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
    extra_context = {'menu': ['PrintCounterDocumentTicket', 'sales'], 'bread': [_('PrintCounterDocumentTicket'), _('Sales')]}
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
    extra_context = {'menu': ['PrintCounterDocumentTicketRectification', 'sales'], 'bread': [_('PrintCounterDocumentTicketRectification'), _('Sales')]}
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
    extra_context = {'menu': ['PrintCounterDocumentInvoice', 'sales'], 'bread': [_('PrintCounterDocumentInvoice'), _('Sales')]}
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
    extra_context = {'menu': ['PrintCounterDocumentInvoiceRectification', 'sales'], 'bread': [_('PrintCounterDocumentInvoiceRectification'), _('Sales')]}
    linkadd = False
    linkedit = False
    default_ordering = "-date"

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(invoice_rectification__pk=pk)
        return limit
