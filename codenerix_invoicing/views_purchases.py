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

import datetime
from django.db import transaction, IntegrityError
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.utils import ErrorList
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.conf import settings

from codenerix_extensions.views import GenCreateBridge, GenUpdateBridge
from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail, GenDetailModal

from codenerix_invoicing.models_purchases import Provider, \
    PurchasesBudget, PurchasesLineBudget, PurchasesOrder, PurchasesLineOrder, PurchasesAlbaran, PurchasesLineAlbaran, \
    PurchasesTicket, PurchasesLineTicket, PurchasesTicketRectification, PurchasesLineTicketRectification, PurchasesInvoice, \
    PurchasesLineInvoice, PurchasesInvoiceRectification, PurchasesLineInvoiceRectification, PurchasesBudgetDocument, \
    PurchasesOrderDocument, PurchasesAlbaranDocument, PurchasesTicketDocument, PurchasesTicketRectificationDocument, \
    PurchasesInvoiceDocument, PurchasesInvoiceRectificationDocument
from codenerix_invoicing.models import ProductStock
from codenerix_storages.models import StorageBatch

from codenerix_invoicing.forms_purchases import ProviderForm, \
    BudgetForm, LineBudgetForm, OrderForm, LineOrderForm, AlbaranForm, LineAlbaranForm, TicketForm, LineTicketForm, TicketRectificationForm, LineTicketRectificationForm, InvoiceForm, LineInvoiceForm, InvoiceRectificationForm, LineInvoiceRectificationForm, \
    BudgetDocumentForm, OrderDocumentForm, AlbaranDocumentForm, TicketDocumentForm, TicketRectificationDocumentForm, InvoiceDocumentForm, InvoiceRectificationDocumentForm, \
    OrderFromBudgetForm

from codenerix_invoicing.views import PrinterHelper

from codenerix_extensions.files.views import DocumentFileView
from codenerix_products.models import ProductFinal, ProductUnique


# ###########################################
class GenProviderUrl(object):
    ws_entry_point = '{}/providers'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# Provider
class ProviderList(GenProviderUrl, GenList):
    model = Provider
    show_details = True
    extra_context = {'menu': ['Provider', 'people'], 'bread': [_('Provider'), _('People')]}


class ProviderCreate(GenProviderUrl, GenCreate, GenCreateBridge):
    model = Provider
    show_details = True
    form_class = ProviderForm

    def form_valid(self, form):
        field = 'codenerix_external_field'
        model = Provider
        related_field = 'provider'
        error_message = [
            _("The selected entry is already a provider, select another entry!"),
            _("The selected entry is not available anymore, please, try again!")
        ]
        return self.form_valid_bridge(form, field, model, related_field, error_message)


class ProviderCreateModal(GenCreateModal, ProviderCreate):
    pass


class ProviderUpdate(GenProviderUrl, GenUpdate, GenUpdateBridge):
    model = Provider
    show_details = True
    form_class = ProviderForm

    def get_form(self, form_class=None):
        form = super(ProviderUpdate, self).get_form(form_class)
        # initial external field
        form.fields['codenerix_external_field'].initial = form.instance.external
        return form

    def form_valid(self, form):
        field = 'codenerix_external_field'
        model = Provider
        related_field = 'provider'
        error_message = [
            _("The selected entry is not available anymore, please, try again!")
        ]
        return self.form_valid_bridge(form, field, model, related_field, error_message)


class ProviderUpdateModal(GenUpdateModal, ProviderUpdate):
    pass


class ProviderDelete(GenProviderUrl, GenDelete):
    model = Provider


class ProviderDetails(GenProviderUrl, GenDetail):
    model = Provider
    groups = ProviderForm.__groups_details__()
    template_model = "purchases/provider_details.html"
    tabs = [
        {'id': 'PersonAddresses', 'name': _('Person addresses'), 'ws': 'provider_personaddress_sublist', 'rows': 'base'},
        {'id': 'Categories', 'name': _('Categories'), 'ws': 'CDNX_products_categoryrelateds_sublist', 'rows': 'base'},
    ]
    exclude_fields = ['categories']


# ###########################################
class GenBudgetUrl(object):
    ws_entry_point = '{}/budgets'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# Budget
class BudgetList(GenBudgetUrl, GenList):
    model = PurchasesBudget
    show_details = True
    extra_context = {'menu': ['Budget', 'people'], 'bread': [_('Budget'), _('People')]}
    template_model = "purchases/budget_list.html"


class BudgetCreate(GenBudgetUrl, GenCreate):
    model = PurchasesBudget
    show_details = True
    form_class = BudgetForm


class BudgetCreateModal(GenCreateModal, BudgetCreate):
    pass


class BudgetUpdate(GenBudgetUrl, GenUpdate):
    model = PurchasesBudget
    show_details = True
    form_class = BudgetForm


class BudgetUpdateModal(GenUpdateModal, BudgetUpdate):
    pass


class BudgetDelete(GenBudgetUrl, GenDelete):
    model = PurchasesBudget


class BudgetDetails(GenBudgetUrl, GenDetail):
    model = PurchasesBudget
    groups = BudgetForm.__groups_details__()
    template_model = "purchases/budget_details.html"
    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_linebudgetpurchasess_sublist', 'rows': 'base'},
        {'id': 'doc', 'name': _('Documents'), 'ws': 'CDNX_invoicing_budgetpurchasesdocuments_sublist', 'rows': 'base'},
    ]


class BudgetPrint(PrinterHelper, GenBudgetUrl, GenDetail):
    model = PurchasesBudget
    modelname = "list"
    template_model = 'purchases/pdf/budget_pdf.html'
    output_filename = '{0}{1}{2}_budget'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(BudgetPrint, self).get_context_data(**kwargs)

        budget = self.object

        # I take address for send.
        # send_address=budget.customer.external.person_address.filter(main=True).first()

        context["budget"] = budget
        lines = []
        total_budget = 0
        for line in budget.line_budget_purchases.all():
            base = (line.price * line.quantity)
            subtotal = base + (base * line.tax / 100.0)
            total_budget += subtotal
            lines.append({
                'product': line.product,
                'price': line.price,
                'quantity': line.quantity,
                'tax': line.tax,
                'total': subtotal
            })
        context['line_budget_purchases'] = lines
        context['total_budget'] = total_budget
        context['media_root'] = settings.MEDIA_ROOT + "/"
        self.output_filename = "{0}".format(budget.date)

        # bloqueo del documento
        # budget.lockit()

        budget.lock = True
        budget.save()
        
        return context


class BudgetDoOrder(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        budget_pk = kwargs.get('pk', None)
        budget = get_object_or_404(PurchasesBudget, pk=budget_pk)

        order = PurchasesOrder()
        order.budget = budget
        order.provider = budget.provider
        order.tax = budget.tax
        order.code = budget.code
        order.date = budget.date
        order.save()

        for line in PurchasesLineBudget.objects.filter(budget__pk=budget_pk):
            lo = PurchasesLineOrder()
            lo.order = order
            lo.line_budget = line
            lo.product = line.product
            lo.quantity = line.quantity
            lo.price = line.price
            lo.tax = line.tax
            lo.description = line.description
            lo.save()

        return HttpResponseRedirect(reverse('orderpurchasess_details_js', kwargs={'pk': order.pk}))


# ###########################################
class GenLineBudgetUrl(object):
    ws_entry_point = '{}/linebudgets'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# LineBudget
class LineBudgetList(GenLineBudgetUrl, GenList):
    model = PurchasesLineBudget
    extra_context = {'menu': ['LineBudget', 'people'], 'bread': [_('LineBudget'), _('People')]}


class LineBudgetCreate(GenLineBudgetUrl, GenCreate):
    model = PurchasesLineBudget
    form_class = LineBudgetForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineBudgetCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            budget = PurchasesBudget.objects.get(pk=self.__pk)
            self.request.budget = budget
            form.instance.budget = budget

        return super(LineBudgetCreate, self).form_valid(form)


class LineBudgetCreateModal(GenCreateModal, LineBudgetCreate):
    pass


class LineBudgetUpdate(GenLineBudgetUrl, GenUpdate):
    model = PurchasesLineBudget
    form_class = LineBudgetForm


class LineBudgetUpdateModal(GenUpdateModal, LineBudgetUpdate):
    pass


class LineBudgetDelete(GenLineBudgetUrl, GenDelete):
    model = PurchasesLineBudget


class LineBudgetSubList(GenLineBudgetUrl, GenList):
    model = PurchasesLineBudget
    gentrans = {
        'CreateOrder': _("Create Order"),
    }

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(budget__pk=pk)
        return limit


class LineBudgetSubListForm(LineBudgetSubList):
    pass


class LineBudgetDetails(GenLineBudgetUrl, GenDetail):
    model = PurchasesLineBudget
    groups = LineBudgetForm.__groups_details__()
    template_model = "purchases/linebudget_details.html"


class LineBudgetDetailsModal(GenDetailModal, LineBudgetDetails):
    pass


# ###########################################
class GenOrderUrl(object):
    ws_entry_point = '{}/orders'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# Order
class OrderList(GenOrderUrl, GenList):
    model = PurchasesOrder
    show_details = True
    extra_context = {'menu': ['Order', 'people'], 'bread': [_('Order'), _('People')]}
    

class OrderCreate(GenOrderUrl, GenCreate):
    model = PurchasesOrder
    show_details = True
    form_class = OrderForm


class OrderCreateModal(GenCreateModal, OrderCreate):
    pass


class OrderCreateFromBudget(GenOrderUrl, GenUpdateModal):
    model = PurchasesBudget
    form_class = OrderFromBudgetForm
    template_model = "purchases/order_from_bugget.html"
    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_linebudgetpurchasess_sublist_form', 'rows': 'base'},
    ]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__budget_pk = kwargs.get('pk', None)
        return super(OrderCreateFromBudget, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(OrderCreateFromBudget, self).get_form(form_class)
        form.initial['code'] = ''
        form.initial['date'] = datetime.datetime.now()
        return form

    def form_valid(self, form):
        if 'lines' in form.data and form.data['lines']:
            budget_pk = format(form.data['__pk__'])
            quantity = {}
            lines_pk = [int(x) for x in form.data['lines'].split(',')]
            for pk in lines_pk:
                quantity[pk] = form.data['quantity_{}'.format(pk)]

            budget = PurchasesBudget.objects.get(pk=budget_pk)
            order = PurchasesOrder()
            order.date = form.data['date']
            order.code = form.data['code']
            order.budget = budget
            order.tax = budget.tax
            order.provider = budget.provider
            with transaction.atomic():
                order.save()

                for line in PurchasesLineBudget.objects.filter(pk__in=lines_pk):
                    lo = PurchasesLineOrder()
                    lo.order = order
                    lo.line_budget = line
                    lo.description = line.description
                    lo.product = line.product
                    lo.price = line.price
                    lo.quantity = quantity[line.pk]
                    lo.tax = line.tax
                    lo.save()
                # reset model and instance
                self.object = order
                self.model = PurchasesOrder
                form.data['__pk__'] = order.pk
                form.instance = order

                return (super(OrderCreateFromBudget, self).form_valid(form))
        else:
            errors = form._errors.setdefault("code", ErrorList())
            errors.append(_("No se han seleccionado lineas"))
            return super(OrderCreateFromBudget, self).form_invalid(form)


class OrderUpdate(GenOrderUrl, GenUpdate):
    model = PurchasesOrder
    show_details = True
    form_class = OrderForm


class OrderUpdateModal(GenUpdateModal, OrderUpdate):
    pass


class OrderDelete(GenOrderUrl, GenDelete):
    model = PurchasesOrder


class OrderDetails(GenOrderUrl, GenDetail):
    model = PurchasesOrder
    groups = OrderForm.__groups_details__()
    template_model = "purchases/order_details.html"
    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_lineorderpurchasess_sublist', 'rows': 'base'},
        {'id': 'doc', 'name': _('Documents'), 'ws': 'CDNX_invoicing_orderpurchasesdocuments_sublist', 'rows': 'base'},
    ]


class OrderDetailsModal(GenDetailModal, OrderDetails):
    pass


class OrderPrint(PrinterHelper, GenOrderUrl, GenDetail):
    model = PurchasesOrder
    modelname = "list"
    template_model = 'purchases/pdf/order_pdf.html'
    output_filename = '{0}{1}{2}_order'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(OrderPrint, self).get_context_data(**kwargs)

        order = self.object
        
        context["order"] = order
        lines = []
        total_order = 0
        for line in order.line_order_purchases.all():
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
        context['line_order_purchases'] = lines
        context['total_order'] = total_order
        context['media_root'] = settings.MEDIA_ROOT + "/"
        self.output_filename = "{0}".format(order.date)

        # bloqueo del documento
        order.lock = True
        order.save()

        return context


# ###########################################
class GenLineOrderUrl(object):
    ws_entry_point = '{}/lineorders'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# LineOrder
class LineOrderList(GenLineOrderUrl, GenList):
    model = PurchasesLineOrder
    extra_context = {'menu': ['LineOrder', 'people'], 'bread': [_('LineOrder'), _('People')]}


class LineOrderCreate(GenLineOrderUrl, GenCreate):
    model = PurchasesLineOrder
    form_class = LineOrderForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineOrderCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            obj = PurchasesOrder.objects.get(pk=self.__pk)
            self.request.order = obj
            form.instance.order = obj

        return super(LineOrderCreate, self).form_valid(form)


class LineOrderCreateModal(GenCreateModal, LineOrderCreate):
    pass


class LineOrderUpdate(GenLineOrderUrl, GenUpdate):
    model = PurchasesLineOrder
    form_class = LineOrderForm


class LineOrderUpdateModal(GenUpdateModal, LineOrderUpdate):
    pass


class LineOrderDelete(GenLineOrderUrl, GenDelete):
    model = PurchasesLineOrder


class LineOrderSubList(GenLineOrderUrl, GenList):
    model = PurchasesLineOrder

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(order__pk=pk)
        return limit


class LineOrderDetails(GenLineOrderUrl, GenDetail):
    model = PurchasesLineOrder
    groups = LineOrderForm.__groups_details__()
    template_model = "purchases/lineorder_details.html"


class LineOrderDetailsModal(GenDetailModal, LineOrderDetails):
    pass


# ###########################################
class GenAlbaranUrl(object):
    ws_entry_point = '{}/albarans'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# Albaran
class AlbaranList(GenAlbaranUrl, GenList):
    model = PurchasesAlbaran
    show_details = True
    extra_context = {'menu': ['Albaran', 'people'], 'bread': [_('Albaran'), _('People')]}
    

class AlbaranCreate(GenAlbaranUrl, GenCreate):
    model = PurchasesAlbaran
    show_details = True
    form_class = AlbaranForm


class AlbaranCreateModal(GenCreateModal, AlbaranCreate):
    pass


class AlbaranUpdate(GenAlbaranUrl, GenUpdate):
    model = PurchasesAlbaran
    show_details = True
    form_class = AlbaranForm


class AlbaranUpdateModal(GenUpdateModal, AlbaranUpdate):
    pass


class AlbaranDelete(GenAlbaranUrl, GenDelete):
    model = PurchasesAlbaran


class AlbaranDetails(GenAlbaranUrl, GenDetail):
    model = PurchasesAlbaran
    groups = AlbaranForm.__groups_details__()
    template_model = "purchases/albaran_details.html"
    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_linealbaranpurchasess_sublist', 'rows': 'base'},
        {'id': 'doc', 'name': _('Documents'), 'ws': 'CDNX_invoicing_albaranpurchasesdocuments_sublist', 'rows': 'base'},
    ]


class AlbaranPrint(PrinterHelper, GenAlbaranUrl, GenDetail):
    model = PurchasesAlbaran
    modelname = "list"
    template_model = 'purchases/pdf/albaran_pdf.html'
    output_filename = '{0}{1}{2}_albaran'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(AlbaranPrint, self).get_context_data(**kwargs)

        albaran = self.object

        # I take address for send.

        context["albaran"] = albaran

        lines = []
        total_albaran = 0
        for line in albaran.line_albaran_purchases.all():
            base = (line.price * line.quantity)
            subtotal = base + (base * line.tax / 100.0)
            total_albaran += subtotal
            lines.append({
                'product': line.product,
                'price': line.price,
                'quantity': line.quantity,
                'tax': line.tax,
                'total': subtotal
            })

        context['line_albaran_purchases'] = lines
        context['total_albaran'] = total_albaran
        context['media_root'] = settings.MEDIA_ROOT + "/"

        self.output_filename = "{0}".format(albaran.date)

        # bloqueo del documento
        albaran.lock = True
        albaran.save()

        return context


# ###########################################
class GenLineAlbaranUrl(object):
    ws_entry_point = '{}/linealbarans'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# LineAlbaran
class LineAlbaranList(GenLineAlbaranUrl, GenList):
    model = PurchasesLineAlbaran
    extra_context = {'menu': ['LineAlbaran', 'people'], 'bread': [_('LineAlbaran'), _('People')]}


class LineAlbaranCreate(GenLineAlbaranUrl, GenCreate):
    model = PurchasesLineAlbaran
    form_class = LineAlbaranForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineAlbaranCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            obj = PurchasesAlbaran.objects.get(pk=self.__pk)
            self.request.albaran = obj
            form.instance.albaran = obj

        batch = StorageBatch.objects.filter(pk=form.data['batch']).first()
        if not batch:
            errors = form._errors.setdefault("batch", ErrorList())
            errors.append(_("Batch invalid"))
            return super(LineAlbaranCreate, self).form_invalid(form)
        
        try:
            with transaction.atomic():
                # comprueba si el producto comprado requiere un valor de atributo especial
                product_final = ProductFinal.objects.filter(pk=form.data['product']).first()
                feature_special_value = None
                if not product_final:
                    errors = form._errors.setdefault("feature_special_value", ErrorList())
                    errors.append(_("Product not selected"))
                    return super(LineAlbaranCreate, self).form_invalid(form)
                elif product_final.product.feature_special:
                    # es obligatorio la informacion de caracteristicas especiales
                    if 'feature_special_value' not in form.data or not form.data['feature_special_value']:
                        errors = form._errors.setdefault("feature_special_value", ErrorList())
                        errors.append(_("Product needs information of feature special"))
                        return super(LineAlbaranCreate, self).form_invalid(form)
                    else:
                        feature_special_value = list(set(filter(None, form.data['feature_special_value'].split('\n'))))
                        try:
                            quantity = int(float(form.data['quantity']))
                        except ValueError:
                            errors = form._errors.setdefault("quantity", ErrorList())
                            errors.append(_("Quantity is not valid"))
                            return super(LineAlbaranCreate, self).form_invalid(form)

                        if product_final.product.feature_special.unique:
                            # mismo numero de caracteristicas que de cantidades
                            # si el feature special esta marcado como 'unico'
                            if len(feature_special_value) != quantity:
                                errors = form._errors.setdefault("feature_special_value", ErrorList())
                                errors.append(_("Quantity and values of feature special not equals"))
                                return super(LineAlbaranCreate, self).form_invalid(form)
                            # no existen las caracteristicas especiales dadas de alta en el sistema
                            elif ProductUnique.objects.filter(product_final=product_final, value__in=feature_special_value).exists():
                                errors = form._errors.setdefault("feature_special_value", ErrorList())
                                errors.append(_("Some value of feature special exists"))
                                return super(LineAlbaranCreate, self).form_invalid(form)
                        elif len(feature_special_value) != 1:
                            errors = form._errors.setdefault("feature_special_value", ErrorList())
                            errors.append(_("The special feature must be unique for all products"))
                            return super(LineAlbaranCreate, self).form_invalid(form)

                # save line albaran
                result = super(LineAlbaranCreate, self).form_valid(form)

                # prepare stock
                ps = ProductStock()
                ps.product_final = product_final
                ps.line_albaran = self.object
                ps.batch = batch
                # save stock
                ps.quantity = self.object.quantity
                ps.save()

                if feature_special_value:
                    # prepare product feature special
                    if product_final.product.feature_special.unique:
                        pfs = ProductUnique()
                        pfs.product_final = product_final
                        # save product featureSpecial and stock
                        for fs in feature_special_value:
                            pfs.pk = None
                            pfs.value = fs
                            pfs.save()

                    else:
                        pfs = ProductUnique.objects.filter(
                            value=feature_special_value[0],
                            product_final=product_final
                        ).first()
                        if pfs:
                            pfs.stock_real += self.object.quantity
                        else:
                            pfs = ProductUnique()
                            pfs.product_final = product_final
                            pfs.value = feature_special_value[0]
                            pfs.stock_real = self.object.quantity
                        pfs.save()
                else:
                    # product unique by default
                    pfs = ProductUnique()
                    pfs.stock_real = self.object.quantity
                    pfs.save()

                return result
        except IntegrityError as e:
            raise Exception(e)
            errors = form._errors.setdefault("product", ErrorList())
            errors.append(_("Integrity Error"))
            return super(LineAlbaranCreate, self).form_invalid(form)


class LineAlbaranCreateModal(GenCreateModal, LineAlbaranCreate):
    pass


class LineAlbaranUpdate(GenLineAlbaranUrl, GenUpdate):
    model = PurchasesLineAlbaran
    form_class = LineAlbaranForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineAlbaranUpdate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(LineAlbaranUpdate, self).get_form(form_class)

        ps = ProductStock.objects.filter(line_albaran=self.object).first()
        if ps:
            # initial field
            form.fields['storage'].initial = ps.batch.zone.storage
            form.fields['zone'].initial = ps.batch.zone
            form.fields['batch'].initial = ps.batch
        return form

    def form_valid(self, form):
        with transaction.atomic():
            old = PurchasesLineAlbaran.objects.get(pk=self.object.pk)

            batch = StorageBatch.objects.filter(pk=form.data['batch']).first()
            if batch is None:
                errors = form._errors.setdefault("batch", ErrorList())
                errors.append(_("Batch not selected"))
                return super(LineAlbaranUpdate, self).form_invalid(form)

            try:
                quantity = float(form.data['quantity'])
            except ValueError:
                errors = form._errors.setdefault("quantity", ErrorList())
                errors.append(_("Quantity is not valid."))
                return super(LineAlbaranUpdate, self).form_invalid(form)

            # comprueba si el producto comprado requiere un valor de atributo especial
            product_final = ProductFinal.objects.filter(pk=form.data['product']).first()
            if not product_final:
                errors = form._errors.setdefault("feature_special_value", ErrorList())
                errors.append(_("Product not selected"))
                return super(LineAlbaranUpdate, self).form_invalid(form)
            
            # FIN VALIDACION MINIMA
            if product_final != old.product:
                """
                comprobar q no se ha vendido el anterior producto
                mirando si las cantidades coinciden y las caracteristicas especiales
                """
                if product_final.product.feature_special:
                    # es obligatorio la informacion de caracteristicas especiales
                    if 'feature_special_value' not in form.data or not form.data['feature_special_value']:
                        errors = form._errors.setdefault("feature_special_value", ErrorList())
                        errors.append(_("Product needs information of feature special"))
                        return super(LineAlbaranUpdate, self).form_invalid(form)
                    
                    try:
                        quantity = int(quantity)
                    except ValueError:
                        errors = form._errors.setdefault("quantity", ErrorList())
                        errors.append(_("Quantity is not valid"))
                        return super(LineAlbaranUpdate, self).form_invalid(form)
                    
                    feature_special_value = list(set(filter(None, form.data['feature_special_value'].split('\n'))))
                    if product_final.product.feature_special.unique:
                        # mismo numero de caracteristicas que de cantidades
                        if len(feature_special_value) != quantity:
                            errors = form._errors.setdefault("feature_special_value", ErrorList())
                            errors.append(_("Quantity and values of feature special not equals"))
                            return super(LineAlbaranUpdate, self).form_invalid(form)

                    # no existen las caracteristicas especiales dadas de alta en el sistema
                    if ProductUnique.objects.filter(
                        product_final=product_final,
                        product_final__product__feature_special=product_final.product.feature_special,
                        value__in=feature_special_value
                    ).exists():
                        errors = form._errors.setdefault("feature_special_value", ErrorList())
                        errors.append(_("Some value of feature special exists"))
                        return super(LineAlbaranUpdate, self).form_invalid(form)
                    
                    if old.product.product.feature_special:
                        """
                        comprobamos que el stock sea el mismo para poder eliminarlo
                        """
                        fs_value_old = list(set(filter(None, old.feature_special_value.split('\n'))))
                        if old.product.product.feature_special.unique:
                            if ProductUnique.objects.filter(
                                product_final=old.product,
                                product_final__product__feature_special=old.product.product.feature_special,
                                value__in=fs_value_old
                            ).aggregate(
                                q=Sum('stock_real')
                            )['q'] != old.quantity:
                                errors = form._errors.setdefault("product", ErrorList())
                                errors.append(_("Products were bought, you can not change product"))
                                return super(LineAlbaranUpdate, self).form_invalid(form)
                        else:
                            if ProductUnique.objects.filter(
                                product_final=old.product,
                                product_final__product__feature_special=old.product.product.feature_special,
                                value=fs_value_old[0]
                            ).values('stock_real').first()['stock_real'] < old.quantity:
                                errors = form._errors.setdefault("product", ErrorList())
                                errors.append(_("Products were bought, you can not change product"))
                                return super(LineAlbaranUpdate, self).form_invalid(form)
                        # guardar, borrar antiguo y dar de alta los nuevos
                        result = super(LineAlbaranUpdate, self).form_valid(form)
                        ProductStock.objects.filter(
                            line_albaran=self.object,
                            product_final=old.product,
                            product_final__product__feature_special=old.product.product.feature_special,
                        ).delete()

                        # prepare stock
                        ps = ProductStock()
                        ps.line_albaran = self.object
                        ps.product_final = product_final
                        ps.batch = batch
                        ps.quantity = self.object.quantity
                        ps.save()
                        # prepare product feature special
                        pu = ProductUnique()
                        pu.product_final = product_final

                        if product_final.product.feature_special.unique:
                            # borra lo antiguo y crea lo nuevo
                            ProductUnique.objects.filter(
                                product_final=old.product,
                                product_final__product__feature_special=old.product.product.feature_special,
                                value__in=fs_value_old
                            ).delete()
                            # save product featureSpecial and stock
                            for fs in feature_special_value:
                                pu.pk = None
                                pu.value = fs
                                pu.stock_real = 1
                                pu.save()
                        else:
                            # creamos o actualizamos el producto unico
                            product_unique = ProductUnique.objects.filter(
                                product_final=product_final,
                                value=feature_special_value[0]
                            ).first()
                            if product_unique is None:
                                product_unique = pu
                                product_unique.stock_real = 0
                            product_unique.stock_real += self.object.quantity
                            product_unique.save()
                            # actualizo el producto unico del registro anterior
                            product_unique_old = old.products_unique.filter(
                                value=fs_value_old[0]
                            ).first()
                            product_unique_old.stock_real -= old.quantity
                            product_unique_old.save()
                    else:
                        # cuando el producto final anterior no tiene una caracteristica especial
                        """
                        comprobamos que las cantidades que fueron introducidas en el albaran son las mismas que hay disponible
                        """
                        product_unique = ProductUnique.objects.filter(
                            product_final=product_final,
                            value=None
                        ).first()
                        if old.quantity > product_unique.stock_real:
                            # error porque la cantidad a descontar es menor que la cantidad en stock
                            errors = form._errors.setdefault("product", ErrorList())
                            errors.append(_("Product were bought, you can not change product"))
                            return super(LineAlbaranUpdate, self).form_invalid(form)
                        else:
                            # guardar, borrar antiguo y dar de alta los nuevos
                            result = super(LineAlbaranUpdate, self).form_valid(form)
                            ProductStock.objects.filter(
                                Q(line_albaran=self.object, product_final=old.product)
                            ).delete()
                            # prepare stock
                            ps = ProductStock()
                            ps.line_albaran = self.object
                            ps.product_final = product_final
                            ps.batch = batch
                            ps.quantity = self.object.quantity
                            ps.save()
                            # actualizamos el stock quitandole al producto unico
                            # la cantidad del anterior registro
                            product_unique.stock_real -= old.quantity
                            product_unique.save()
                            # prepare product unique
                            pu = ProductUnique.objects.filter(
                                product_final=product_final,
                                value__in=feature_special_value
                            ).first()
                            if pu is None:
                                pu = ProductUnique()
                                pu.product_final = product_final
                            if product_final.product.feature_special.unique:
                                # save product unique
                                for fs in feature_special_value:
                                    pu.pk = None
                                    pu.value = fs
                                    pu.stock_real = 1
                                    pu.save()
                            else:
                                pu.value = feature_special_value[0]
                                pu.stock_real += self.object.quantity
                                pu.save()
                # FIN if product_final.product.feature_special

                if old.product.product.feature_special:
                    """
                    si el nuevo producto no necesita de una caracteristicas especial y el antiguo si
                    comprobamos que el stock sea el mismo para poder eliminarlo
                    """
                    if ProductStock.objects.filter(
                        line_albaran=self.object,
                        product_final=old.product,
                        feature_special=old.product.product.feature_special,
                        value__in=list(set(filter(None, old.feature_special_value.split('\n'))))
                    ).aggregate(
                        q=Sum('quantity')
                    )['q'] != old.quantity:
                        errors = form._errors.setdefault("product", ErrorList())
                        errors.append(_("Products were bought, you can not change product"))
                        return super(LineAlbaranUpdate, self).form_invalid(form)
                    else:
                        # guardar y actualizar
                        result = super(LineAlbaranUpdate, self).form_valid(form)
                        # borra stock antiguo
                        ProductStock.objects.filter(
                            line_albaran=self.object,
                            product_final=old.product,
                            feature_special=old.product.product.feature_special,
                            value__in=list(set(filter(None, old.feature_special_value.split('\n'))))
                        ).delete()
                        # guarda nuevo stock
                        ps = ProductStock()
                        ps.product_final = product_final
                        ps.line_albaran = self.object
                        ps.batch = batch
                        ps.quantity = quantity
                        ps.save()
                        # borra las caracteristicas especiales
                        ProductUnique.objects.filter(
                            product_final=self.object.product,
                            feature_special=old.product.product.feature_special,
                            value__in=list(set(filter(None, old.feature_special_value.split('\n'))))
                        ).delete()

                if product_final.product.feature_special is None and old.product.product.feature_special is None:
                    """
                    comprobamos que las cantidades que fueron introducidas en el albaran son las mismas que hay disponible
                    """
                    if ProductUnique.objects.filter(
                        product_final=old.product,
                        stock_real__lte=old.quantity
                    ).exists():
                        errors = form._errors.setdefault("product", ErrorList())
                        errors.append(_("Product were bought, you can not change product"))
                        return super(LineInvoiceUpdate, self).form_invalid(form)
                    
                    # guardar y actualizar
                    result = super(LineAlbaranUpdate, self).form_valid(form)
                    ProductStock.objects.filter(
                        Q(line_albaran=self.objects, product_final=old.product)
                    ).update(
                        batch=batch,
                        product=product_final,
                        quantity=quantity
                    )
                    # actualizamos/creamos el nuevo registro
                    product_unique = ProductUnique.objects.filter(
                        product_final=product_final, value=None
                    ).first()
                    if product_unique is None:
                        product_unique = ProductUnique()
                        product_unique.product_final = product_final
                        product_unique.value = None
                        product_unique.stock_real = 0
                    product_unique.stock_real += self.object.quantity
                    product_unique.save()
                    # actualizamos el registro anterior
                    product_unique_old = old.products_unique.get()
                    product_unique_old.stock_real -= old.quantity
                    product_unique_old.save()
            elif product_final.product.feature_special:
                """
                modificamos el mismo producto
                """
                # es obligatorio la informacion de caracteristicas especiales
                if 'feature_special_value' not in form.data or not form.data['feature_special_value']:
                    errors = form._errors.setdefault("feature_special_value", ErrorList())
                    errors.append(_("Product needs information of feature special"))
                    return super(LineAlbaranUpdate, self).form_invalid(form)

                items_remove = None
                items_new = None
                feature_special_value = list(set(filter(None, form.data['feature_special_value'].split('\n'))))
                fs_value_old = list(set(filter(None, old.feature_special_value.split('\n'))))
                product_unique = None
                
                if product_final.product.feature_special.unique:
                    # mismo numero de caracteristicas que de cantidades
                    if len(feature_special_value) != quantity:
                        errors = form._errors.setdefault("feature_special_value", ErrorList())
                        errors.append(_("Quantity and values of feature special not equals"))
                        return super(LineAlbaranUpdate, self).form_invalid(form)
                    else:
                        # no existen las caracteristicas especiales dadas de alta en el sistema
                        if ProductUnique.objects.filter(
                            product_final=product_final,
                            product_final__product__feature_special=product_final.product.feature_special,
                            value__in=feature_special_value
                        ).exists():
                            errors = form._errors.setdefault("feature_special_value", ErrorList())
                            errors.append(_("Some value of feature special exists"))
                            return super(LineAlbaranUpdate, self).form_invalid(form)
                    
                    # se han modificado las caracteristicas especiales
                    if fs_value_old != feature_special_value:
                        items_new = []
                        # elementos eliminados
                        for x in feature_special_value:
                            if x not in fs_value_old:
                                items_new.append(x)
                        items_remove = []
                        # elementos nuevos
                        for x in fs_value_old:
                            if x not in feature_special_value:
                                items_remove.append(x)

                        if items_remove:
                            """
                            comprobar que no se ha vendido el producto con la caracteristica que falta
                            para eso la cantidad del ProductUnique asociado debe ser mayor a 0
                            mostrar error
                            """
                            if ProductUnique.objects.filter(
                                product_final=self.object.product,
                                value__in=items_remove,
                                stock_real__lte=0
                            ).exists():
                                errors = form._errors.setdefault("feature_special_value", ErrorList())
                                errors.append(_("Some features special can not be delete because it were bought"))
                                return super(LineAlbaranUpdate, self).form_invalid(form)
                else:
                    """
                    busco el producto unico
                    y actualizo la cantidad y el valor de la caracteristicas especial
                    """
                    product_unique = ProductUnique.objects.filter(
                        product_final=old.product,
                        value__in=fs_value_old
                    ).first()
                    if product_unique:
                        # compruebo que el stock sea positivo
                        if product_unique.stock_real + self.object.quantity - old.quantity <= 0:
                            errors = form._errors.setdefault("feature_special_value", ErrorList())
                            errors.append(_("Some features special can not be delete because it were bought"))
                            return super(LineAlbaranUpdate, self).form_invalid(form)
                    else:
                        errors = form._errors.setdefault("product", ErrorList())
                        errors.append(_("Product is not valid."))
                        return super(LineAlbaranUpdate, self).form_invalid(form)

                result = super(LineAlbaranUpdate, self).form_valid(form)

                # solo entrara si la caracteristica es NO unica
                if product_unique:
                    if self.object.quantity != old.quantity:
                        product_unique.stock_real += self.object.quantity - old.quantity
                        product_unique.save()
                    if fs_value_old == feature_special_value:
                        product_unique.value = feature_special_value[0]
                        product_unique.save()

                # solo entrara si la caracteristica es unica
                if items_remove:
                    """
                    una vez que se guarde, eliminar o poner a 0 el ProductStock asociado y el ProductUnique
                    """
                    ProductStock.objects.filter(
                        line_albaran=self.object,
                        product_final=self.object.product,
                        product_final__product__feature_special=self.object.product.product.feature_special,
                        value__in=items_remove).delete()

                    ProductUnique.objects.filter(
                        product_final=self.object.product,
                        value__in=items_remove).delete()

                # solo entrara si la caracteristica es unica
                if items_new:
                    """
                    buscar si hay elementos nuevos y darlos de alta en ProductStock y ProductUnique
                    """
                    # prepare stock
                    ps = ProductStock()
                    ps.product_final = product_final
                    ps.line_albaran = self.object
                    ps.batch = batch
                    # prepare product feature special
                    pu = ProductUnique()
                    pu.product_final = product_final
                    # save product featureSpecial and stock
                    for fs in items_new:
                        pu.pk = None
                        pu.value = fs
                        pu.save()

                        ps.pk = None
                        ps.value = fs
                        ps.quantity = 1
                        ps.save()

            else:
                """
                comprobamos que las nuevas cantidades esten aun en stock
                """
                if quantity < old.quantity:
                    if ProductStock.objects.filter(
                        line_albaran=self.object,
                        product_final=self.object.product,
                        quantity__lt=quantity
                    ).exists():
                        errors = form._errors.setdefault("quantity", ErrorList())
                        errors.append(_("Quantity invalid, no stock"))
                        return super(LineAlbaranUpdate, self).form_invalid(form)

                result = super(LineAlbaranUpdate, self).form_valid(form)
                ProductStock.objects.filter(
                    batch=batch,
                    line_albaran=self.object,
                    product_final=self.object.product).update(quantity=quantity)

            return result


class LineAlbaranUpdateModal(GenUpdateModal, LineAlbaranUpdate):
    pass


class LineAlbaranDelete(GenLineAlbaranUrl, GenDelete):
    model = PurchasesLineAlbaran


class LineAlbaranSubList(GenLineAlbaranUrl, GenList):
    model = PurchasesLineAlbaran

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(albaran__pk=pk)
        return limit


class LineAlbaranDetails(GenLineAlbaranUrl, GenDetail):
    model = PurchasesLineAlbaran
    groups = LineAlbaranForm.__groups_details__()
    template_model = "purchases/linealbaran_details.html"


class LineAlbaranDetailsModal(GenDetailModal, LineAlbaranDetails):
    pass


# ###########################################
class GenTicketUrl(object):
    ws_entry_point = '{}/tickets'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# Ticket
class TicketList(GenTicketUrl, GenList):
    model = PurchasesTicket
    show_details = True
    extra_context = {'menu': ['Ticket', 'people'], 'bread': [_('Ticket'), _('People')]}


class TicketCreate(GenTicketUrl, GenCreate):
    model = PurchasesTicket
    show_details = True
    form_class = TicketForm


class TicketCreateModal(GenCreateModal, TicketCreate):
    pass


class TicketUpdate(GenTicketUrl, GenUpdate):
    model = PurchasesTicket
    show_details = True
    form_class = TicketForm


class TicketUpdateModal(GenUpdateModal, TicketUpdate):
    pass


class TicketDelete(GenTicketUrl, GenDelete):
    model = PurchasesTicket


class TicketDetails(GenTicketUrl, GenDetail):
    model = PurchasesTicket
    groups = TicketForm.__groups_details__()
    template_model = "purchases/ticket_details.html"
    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_lineticketpurchasess_sublist', 'rows': 'base'},
        {'id': 'doc', 'name': _('Documents'), 'ws': 'CDNX_invoicing_ticketpurchasesdocuments_sublist', 'rows': 'base'},
    ]


class TicketPrint(PrinterHelper, GenTicketUrl, GenDetail):
    model = PurchasesTicket
    modelname = "list"
    template_model = 'purchases/pdf/ticket_pdf.html'
    output_filename = '{0}{1}{2}_ticket'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(TicketPrint, self).get_context_data(**kwargs)

        ticket = self.object

        context["ticket"] = ticket
        lines = []
        total_ticket = 0
        for line in ticket.line_ticket_purchases.all():
            base = (line.price * line.quantity)
            subtotal = base + (base * line.tax / 100.0)
            total_ticket += subtotal
            lines.append({
                'product': line.product,
                'price': line.price,
                'quantity': line.quantity,
                'tax': line.tax,
                'total': subtotal
            })
        context['line_ticket_purchases'] = lines
        context['total_ticket'] = total_ticket
        context['media_root'] = settings.MEDIA_ROOT + "/"
        self.output_filename = "{0}".format(ticket.date)

        # bloqueo del documento
        ticket.lock = True
        ticket.save()

        return context


# ###########################################
class GenLineTicketUrl(object):
    ws_entry_point = '{}/linetickets'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# LineTicket
class LineTicketList(GenLineTicketUrl, GenList):
    model = PurchasesLineTicket
    extra_context = {'menu': ['LineTicket', 'people'], 'bread': [_('LineTicket'), _('People')]}


class LineTicketCreate(GenLineTicketUrl, GenCreate):
    model = PurchasesLineTicket
    form_class = LineTicketForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineTicketCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            obj = PurchasesTicket.objects.get(pk=self.__pk)
            self.request.ticket = obj
            form.instance.ticket = obj

        return super(LineTicketCreate, self).form_valid(form)


class LineTicketCreateModal(GenCreateModal, LineTicketCreate):
    pass


class LineTicketUpdate(GenLineTicketUrl, GenUpdate):
    model = PurchasesLineTicket
    form_class = LineTicketForm


class LineTicketUpdateModal(GenUpdateModal, LineTicketUpdate):
    pass


class LineTicketDelete(GenLineTicketUrl, GenDelete):
    model = PurchasesLineTicket


class LineTicketSubList(GenLineTicketUrl, GenList):
    model = PurchasesLineTicket

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(ticket__pk=pk)
        return limit


class LineTicketDetails(GenLineTicketUrl, GenDetail):
    model = PurchasesLineTicket
    groups = LineTicketForm.__groups_details__()
    template_model = "purchases/lineticket_details.html"


class LineTicketDetailsModal(GenDetailModal, LineTicketDetails):
    pass


# ###########################################
class GenTicketRectificationUrl(object):
    ws_entry_point = '{}/ticketrectifications'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# TicketRectification
class TicketRectificationList(GenTicketRectificationUrl, GenList):
    model = PurchasesTicketRectification
    show_details = True
    extra_context = {'menu': ['TicketRectification', 'people'], 'bread': [_('TicketRectification'), _('People')]}


class TicketRectificationCreate(GenTicketRectificationUrl, GenCreate):
    model = PurchasesTicketRectification
    show_details = True
    form_class = TicketRectificationForm


class TicketRectificationCreateModal(GenCreateModal, TicketRectificationCreate):
    pass


class TicketRectificationUpdate(GenTicketRectificationUrl, GenUpdate):
    model = PurchasesTicketRectification
    show_details = True
    form_class = TicketRectificationForm


class TicketRectificationUpdateModal(GenUpdateModal, TicketRectificationUpdate):
    pass


class TicketRectificationDelete(GenTicketRectificationUrl, GenDelete):
    model = PurchasesTicketRectification


class TicketRectificationDetails(GenTicketRectificationUrl, GenDetail):
    model = PurchasesTicketRectification
    groups = TicketRectificationForm.__groups_details__()
    template_model = "purchases/ticketrectification_details.html"
    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_lineticketrectificationpurchasess_sublist', 'rows': 'base'},
        {'id': 'doc', 'name': _('Documents'), 'ws': 'CDNX_invoicing_ticketrectificationpurchasesdocuments_sublist', 'rows': 'base'},
    ]


class TicketRectificationPrint(PrinterHelper, GenTicketRectificationUrl, GenDetail):
    model = PurchasesTicketRectification
    modelname = "list"
    template_model = 'purchases/pdf/ticketrectification_pdf.html'
    output_filename = '{0}{1}{2}_ticketrectification'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(TicketRectificationPrint, self).get_context_data(**kwargs)

        ticketrectification = self.object

        context["ticketrectification"] = ticketrectification
        lines = []
        total_ticketrectification = 0
        for line in ticketrectification.line_ticketrectification_purchases.all():
            base = (line.line_ticket.price * line.line_ticket.quantity)
            subtotal = base + (base * line.line_ticket.tax / 100.0)
            total_ticketrectification += subtotal
            lines.append({
                'product': line.line_ticket.product,
                'price': line.line_ticket.price,
                'quantity': line.line_ticket.quantity,
                'tax': line.line_ticket.tax,
                'total': subtotal
            })

        context['line_ticketrectification_purchases'] = lines
        context['total_ticketrectification'] = total_ticketrectification
        context['media_root'] = settings.MEDIA_ROOT + "/"

        # bloqueo del documento
        ticketrectification.lock = True
        ticketrectification.save()

        return context


# ###########################################
class GenLineTicketRectificationUrl(object):
    ws_entry_point = '{}/lineticketrectifications'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# LineTicketRectification
class LineTicketRectificationList(GenLineTicketRectificationUrl, GenList):
    model = PurchasesLineTicketRectification
    extra_context = {'menu': ['LineTicketRectification', 'people'], 'bread': [_('LineTicketRectification'), _('People')]}


class LineTicketRectificationCreate(GenLineTicketRectificationUrl, GenCreate):
    model = PurchasesLineTicketRectification
    form_class = LineTicketRectificationForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineTicketRectificationCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            obj = PurchasesTicketRectification.objects.get(pk=self.__pk)
            self.request.ticket_rectification = obj
            form.instance.ticket_rectification = obj

        return super(LineTicketRectificationCreate, self).form_valid(form)


class LineTicketRectificationCreateModal(GenCreateModal, LineTicketRectificationCreate):
    pass


class LineTicketRectificationUpdate(GenLineTicketRectificationUrl, GenUpdate):
    model = PurchasesLineTicketRectification
    form_class = LineTicketRectificationForm


class LineTicketRectificationUpdateModal(GenUpdateModal, LineTicketRectificationUpdate):
    pass


class LineTicketRectificationDelete(GenLineTicketRectificationUrl, GenDelete):
    model = PurchasesLineTicketRectification


class LineTicketRectificationSubList(GenLineTicketRectificationUrl, GenList):
    model = PurchasesLineTicketRectification

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(ticket_rectification__pk=pk)
        return limit


class LineTicketRectificationDetails(GenLineTicketRectificationUrl, GenDetail):
    model = PurchasesLineTicketRectification
    groups = LineTicketRectificationForm.__groups_details__()
    template_model = "purchases/lineticketrectification_details.html"


class LineTicketRectificationDetailsModal(GenDetailModal, LineTicketRectificationDetails):
    pass


# ###########################################
class GenInvoiceUrl(object):
    ws_entry_point = '{}/invoices'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# Invoice
class InvoiceList(GenInvoiceUrl, GenList):
    model = PurchasesInvoice
    show_details = True
    extra_context = {'menu': ['Invoice', 'people'], 'bread': [_('Invoice'), _('People')]}


class InvoiceCreate(GenInvoiceUrl, GenCreate):
    model = PurchasesInvoice
    show_details = True
    form_class = InvoiceForm


class InvoiceCreateModal(GenCreateModal, InvoiceCreate):
    pass


class InvoiceUpdate(GenInvoiceUrl, GenUpdate):
    model = PurchasesInvoice
    show_details = True
    form_class = InvoiceForm


class InvoiceUpdateModal(GenUpdateModal, InvoiceUpdate):
    pass


class InvoiceDelete(GenInvoiceUrl, GenDelete):
    model = PurchasesInvoice


class InvoiceDetails(GenInvoiceUrl, GenDetail):
    model = PurchasesInvoice
    groups = InvoiceForm.__groups_details__()
    template_model = "purchases/invoice_details.html"
    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_lineinvoicepurchasess_sublist', 'rows': 'base'},
        {'id': 'doc', 'name': _('Documents'), 'ws': 'CDNX_invoicing_invoicepurchasesdocuments_sublist', 'rows': 'base'},
    ]


class InvoicePrint(PrinterHelper, GenInvoiceUrl, GenDetail):
    model = PurchasesInvoice
    modelname = "list"
    template_model = 'purchases/pdf/invoice_pdf.html'
    output_filename = '{0}{1}{2}_invoice'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(InvoicePrint, self).get_context_data(**kwargs)

        invoice = self.object

        context["invoice"] = invoice
        lines = []
        total_invoice = 0
        for line in invoice.line_invoice_purchases.all():
            base = (line.price * line.quantity)
            subtotal = base + (base * line.tax / 100.0)
            total_invoice += subtotal
            lines.append({
                'product': line.product,
                'price': line.price,
                'quantity': line.quantity,
                'tax': line.tax,
                'total': subtotal
            })
        context['line_invoice_purchases'] = lines
        context['total_invoice'] = total_invoice
        context['media_root'] = settings.MEDIA_ROOT + "/"

        self.output_filename = "{0}".format(invoice.date)

        # bloqueo del documento
        invoice.lock = True
        invoice.save()

        return context


# ###########################################
class GenLineInvoiceUrl(object):
    ws_entry_point = '{}/lineinvoices'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# LineInvoice
class LineInvoiceList(GenLineInvoiceUrl, GenList):
    model = PurchasesLineInvoice
    extra_context = {'menu': ['LineInvoice', 'people'], 'bread': [_('LineInvoice'), _('People')]}


class LineInvoiceCreate(GenLineInvoiceUrl, GenCreate):
    model = PurchasesLineInvoice
    form_class = LineInvoiceForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineInvoiceCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            obj = PurchasesInvoice.objects.get(pk=self.__pk)
            self.request.invoice = obj
            form.instance.invoice = obj

        # comprueba si el producto comprado requiere un valor de atributo especial
        product_final = ProductFinal.objects.filter(pk=form.data['product']).first()
        if not product_final:
            errors = form._errors.setdefault("feature_special_value", ErrorList())
            errors.append(_("Product not selected"))
            return super(LineInvoiceCreate, self).form_invalid(form)
        elif product_final.product.feature_special:
            if 'feature_special_value' not in form.data or not form.data['feature_special_value']:
                errors = form._errors.setdefault("feature_special_value", ErrorList())
                errors.append(_("Product needs information of feature special"))
                return super(LineInvoiceCreate, self).form_invalid(form)

        return super(LineInvoiceCreate, self).form_valid(form)


class LineInvoiceCreateModal(GenCreateModal, LineInvoiceCreate):
    pass


class LineInvoiceUpdate(GenLineInvoiceUrl, GenUpdate):
    model = PurchasesLineInvoice
    form_class = LineInvoiceForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineInvoiceUpdate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        # comprueba si el producto comprado requiere un valor de atributo especial
        product_final = ProductFinal.objects.filter(pk=form.data['product']).first()
        if not product_final:
            errors = form._errors.setdefault("feature_special_value", ErrorList())
            errors.append(_("Product not selected"))
            return super(LineInvoiceUpdate, self).form_invalid(form)
        elif product_final.product.feature_special:
            if 'feature_special_value' not in form.data or not form.data['feature_special_value']:
                errors = form._errors.setdefault("feature_special_value", ErrorList())
                errors.append(_("Product needs information of feature special"))
                return super(LineInvoiceUpdate, self).form_invalid(form)

        return super(LineInvoiceUpdate, self).form_valid(form)


class LineInvoiceUpdateModal(GenUpdateModal, LineInvoiceUpdate):
    pass


class LineInvoiceDelete(GenLineInvoiceUrl, GenDelete):
    model = PurchasesLineInvoice


class LineInvoiceSubList(GenLineInvoiceUrl, GenList):
    model = PurchasesLineInvoice

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(invoice__pk=pk)
        return limit


class LineInvoiceDetails(GenLineInvoiceUrl, GenDetail):
    model = PurchasesLineInvoice
    groups = LineInvoiceForm.__groups_details__()


class LineInvoiceDetailsModal(GenDetailModal, LineInvoiceDetails):
    pass


# ###########################################
class GenInvoiceRectificationUrl(object):
    ws_entry_point = '{}/invoicerectifications'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# InvoiceRectification
class InvoiceRectificationList(GenInvoiceRectificationUrl, GenList):
    model = PurchasesInvoiceRectification
    show_details = True
    extra_context = {'menu': ['InvoiceRectification', 'people'], 'bread': [_('InvoiceRectification'), _('People')]}


class InvoiceRectificationCreate(GenInvoiceRectificationUrl, GenCreate):
    model = PurchasesInvoiceRectification
    show_details = True
    form_class = InvoiceRectificationForm


class InvoiceRectificationCreateModal(GenCreateModal, InvoiceRectificationCreate):
    pass


class InvoiceRectificationUpdate(GenInvoiceRectificationUrl, GenUpdate):
    model = PurchasesInvoiceRectification
    show_details = True
    form_class = InvoiceRectificationForm


class InvoiceRectificationUpdateModal(GenUpdateModal, InvoiceRectificationUpdate):
    pass


class InvoiceRectificationDelete(GenInvoiceRectificationUrl, GenDelete):
    model = PurchasesInvoiceRectification


class InvoiceRectificationDetails(GenInvoiceRectificationUrl, GenDetail):
    model = PurchasesInvoiceRectification
    groups = InvoiceRectificationForm.__groups_details__()
    template_model = "purchases/invoicerectification_details.html"
    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_lineinvoicerectificationpurchasess_sublist', 'rows': 'base'},
        {'id': 'doc', 'name': _('Documents'), 'ws': 'CDNX_invoicing_invoicerectificationpurchasesdocuments_sublist', 'rows': 'base'},
    ]


class InvoiceRectificationPrint(PrinterHelper, GenInvoiceRectificationUrl, GenDetail):
    model = PurchasesInvoiceRectification
    modelname = "list"
    template_model = 'sales/pdf/invoicerectification_pdf.html'
    output_filename = '{0}{1}{2}_invoicerectification'.format(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

    def get_context_data(self, **kwargs):
        # Get context
        context = super(InvoiceRectificationPrint, self).get_context_data(**kwargs)

        invoicerectification = self.object

        context["invoicerectification"] = invoicerectification
        lines = []
        total_invoicerectification = 0
        for line in invoicerectification.line_invoicerectification_purchases.all():
            base = (line.line_invoice.price * line.line_invoice.quantity)
            subtotal = base + (base * line.line_invoice.tax / 100.0)
            total_invoicerectification += subtotal
            lines.append({
                'product': line.line_invoice.product,
                'price': line.line_invoice.price,
                'quantity': line.line_invoice.quantity,
                'tax': line.line_invoice.tax,
                'total': subtotal
            })
        # I take address for send.

        context['line_invoicerectification_purchases'] = lines
        context['total_invoicerectification'] = total_invoicerectification
        context['media_root'] = settings.MEDIA_ROOT + "/"
        self.output_filename = "{0}".format(invoicerectification.date)

        # bloqueo del documento
        invoicerectification.lock = True
        invoicerectification.save()

        return context


# ###########################################
class GenLineInvoiceRectificationUrl(object):
    ws_entry_point = '{}/lineinvoicerectifications'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# LineInvoiceRectification
class LineInvoiceRectificationList(GenLineInvoiceRectificationUrl, GenList):
    model = PurchasesLineInvoiceRectification
    extra_context = {'menu': ['LineInvoiceRectification', 'people'], 'bread': [_('LineInvoiceRectification'), _('People')]}


class LineInvoiceRectificationCreate(GenLineInvoiceRectificationUrl, GenCreate):
    model = PurchasesLineInvoiceRectification
    form_class = LineInvoiceRectificationForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(LineInvoiceRectificationCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            obj = PurchasesInvoiceRectification.objects.get(pk=self.__pk)
            self.request.invoice_rectification = obj
            form.instance.invoice_rectification = obj

        return super(LineInvoiceRectificationCreate, self).form_valid(form)


class LineInvoiceRectificationCreateModal(GenCreateModal, LineInvoiceRectificationCreate):
    pass


class LineInvoiceRectificationUpdate(GenLineInvoiceRectificationUrl, GenUpdate):
    model = PurchasesLineInvoiceRectification
    form_class = LineInvoiceRectificationForm


class LineInvoiceRectificationUpdateModal(GenUpdateModal, LineInvoiceRectificationUpdate):
    pass


class LineInvoiceRectificationDelete(GenLineInvoiceRectificationUrl, GenDelete):
    model = PurchasesLineInvoiceRectification


class LineInvoiceRectificationSubList(GenLineInvoiceRectificationUrl, GenList):
    model = PurchasesLineInvoiceRectification

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(invoice_rectification__pk=pk)
        return limit


class LineInvoiceRectificationDetails(GenLineInvoiceRectificationUrl, GenDetail):
    model = PurchasesLineInvoiceRectification
    groups = LineInvoiceRectificationForm.__groups_details__()
    template_model = "purchases/lineinvoice_details.html"


class LineInvoiceRectificationDetailsModal(GenDetailModal, LineInvoiceRectificationDetails):
    pass


# ###########################################
# #### DOCUMENTOS RELACIONADOS ##############
# ############################################
# ###########################################
class GenBudgetDocumentUrl(object):
    ws_entry_point = '{}/budgetdocuments'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# BudgetDocument
class BudgetDocumentList(GenBudgetDocumentUrl, GenList):
    model = PurchasesBudgetDocument
    extra_context = {'menu': ['BudgetDocument', 'people'], 'bread': [_('BudgetDocument'), _('People')]}


class BudgetDocumentCreate(GenBudgetDocumentUrl, DocumentFileView, GenCreate):
    model = PurchasesBudgetDocument
    form_class = BudgetDocumentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(BudgetDocumentCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            budget = PurchasesBudget.objects.get(pk=self.__pk)
            self.request.budget = budget
            form.instance.budget = budget

        return super(BudgetDocumentCreate, self).form_valid(form)


class BudgetDocumentCreateModal(GenCreateModal, BudgetDocumentCreate):
    pass


class BudgetDocumentUpdate(GenBudgetDocumentUrl, DocumentFileView, GenUpdate):
    model = PurchasesBudgetDocument
    form_class = BudgetDocumentForm


class BudgetDocumentUpdateModal(GenUpdateModal, BudgetDocumentUpdate):
    pass


class BudgetDocumentDelete(GenBudgetDocumentUrl, GenDelete):
    model = PurchasesBudgetDocument


class BudgetDocumentSubList(GenBudgetDocumentUrl, GenList):
    model = PurchasesBudgetDocument

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(budget__pk=pk)
        return limit


class BudgetDocumentDetails(GenBudgetDocumentUrl, GenDetail):
    model = PurchasesBudgetDocument
    groups = BudgetDocumentForm.__groups_details__()
    template_model = "purchases/budgetdocument_details.html"


class BudgetDocumentDetailsModal(GenDetailModal, BudgetDocumentDetails):
    pass


# ###########################################
class GenOrderDocumentUrl(object):
    ws_entry_point = '{}/orderdocuments'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# OrderDocument
class OrderDocumentList(GenOrderDocumentUrl, GenList):
    model = PurchasesOrderDocument
    extra_context = {'menu': ['OrderDocument', 'people'], 'bread': [_('OrderDocument'), _('People')]}


class OrderDocumentCreate(GenOrderDocumentUrl, DocumentFileView, GenCreate):
    model = PurchasesOrderDocument
    form_class = OrderDocumentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(OrderDocumentCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            obj = PurchasesOrder.objects.get(pk=self.__pk)
            self.request.order = obj
            form.instance.order = obj

        return super(OrderDocumentCreate, self).form_valid(form)


class OrderDocumentCreateModal(GenCreateModal, OrderDocumentCreate):
    pass


class OrderDocumentUpdate(GenOrderDocumentUrl, DocumentFileView, GenUpdate):
    model = PurchasesOrderDocument
    form_class = OrderDocumentForm


class OrderDocumentUpdateModal(GenUpdateModal, OrderDocumentUpdate):
    pass


class OrderDocumentDelete(GenOrderDocumentUrl, GenDelete):
    model = PurchasesOrderDocument


class OrderDocumentSubList(GenOrderDocumentUrl, GenList):
    model = PurchasesOrderDocument

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(order__pk=pk)
        return limit


class OrderDocumentDetails(GenOrderDocumentUrl, GenDetail):
    model = PurchasesOrderDocument
    groups = OrderDocumentForm.__groups_details__()
    template_model = "purchases/orderdocument_details.html"


class OrderDocumentDetailsModal(GenDetailModal, OrderDocumentDetails):
    pass


# ###########################################
class GenAlbaranDocumentUrl(object):
    ws_entry_point = '{}/albarandocuments'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# AlbaranDocument
class AlbaranDocumentList(GenAlbaranDocumentUrl, GenList):
    model = PurchasesAlbaranDocument
    extra_context = {'menu': ['AlbaranDocument', 'people'], 'bread': [_('AlbaranDocument'), _('People')]}


class AlbaranDocumentCreate(GenAlbaranDocumentUrl, DocumentFileView, GenCreate):
    model = PurchasesAlbaranDocument
    form_class = AlbaranDocumentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(AlbaranDocumentCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            obj = PurchasesAlbaran.objects.get(pk=self.__pk)
            self.request.albaran = obj
            form.instance.albaran = obj

        return super(AlbaranDocumentCreate, self).form_valid(form)


class AlbaranDocumentCreateModal(GenCreateModal, AlbaranDocumentCreate):
    pass


class AlbaranDocumentUpdate(GenAlbaranDocumentUrl, DocumentFileView, GenUpdate):
    model = PurchasesAlbaranDocument
    form_class = AlbaranDocumentForm


class AlbaranDocumentUpdateModal(GenUpdateModal, AlbaranDocumentUpdate):
    pass


class AlbaranDocumentDelete(GenAlbaranDocumentUrl, GenDelete):
    model = PurchasesAlbaranDocument


class AlbaranDocumentSubList(GenAlbaranDocumentUrl, GenList):
    model = PurchasesAlbaranDocument

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(albaran__pk=pk)
        return limit


class AlbaranDocumentDetails(GenAlbaranDocumentUrl, GenDetail):
    model = PurchasesAlbaranDocument
    groups = AlbaranDocumentForm.__groups_details__()
    template_model = "purchases/albarandocument_details.html"


class AlbaranDocumentDetailsModal(GenDetailModal, AlbaranDocumentDetails):
    pass


# ###########################################
class GenTicketDocumentUrl(object):
    ws_entry_point = '{}/ticketdocuments'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# TicketDocument
class TicketDocumentList(GenTicketDocumentUrl, GenList):
    model = PurchasesTicketDocument
    extra_context = {'menu': ['TicketDocument', 'people'], 'bread': [_('TicketDocument'), _('People')]}


class TicketDocumentCreate(GenTicketDocumentUrl, DocumentFileView, GenCreate):
    model = PurchasesTicketDocument
    form_class = TicketDocumentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(TicketDocumentCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            obj = PurchasesTicket.objects.get(pk=self.__pk)
            self.request.ticket = obj
            form.instance.ticket = obj

        return super(TicketDocumentCreate, self).form_valid(form)


class TicketDocumentCreateModal(GenCreateModal, TicketDocumentCreate):
    pass


class TicketDocumentUpdate(GenTicketDocumentUrl, DocumentFileView, GenUpdate):
    model = PurchasesTicketDocument
    form_class = TicketDocumentForm


class TicketDocumentUpdateModal(GenUpdateModal, TicketDocumentUpdate):
    pass


class TicketDocumentDelete(GenTicketDocumentUrl, GenDelete):
    model = PurchasesTicketDocument


class TicketDocumentSubList(GenTicketDocumentUrl, GenList):
    model = PurchasesTicketDocument

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(ticket__pk=pk)
        return limit


class TicketDocumentDetails(GenTicketDocumentUrl, GenDetail):
    model = PurchasesTicketDocument
    groups = TicketDocumentForm.__groups_details__()
    template_model = "purchases/ticketdocument_details.html"


class TicketDocumentDetailsModal(GenDetailModal, TicketDocumentDetails):
    pass


# ###########################################
class GenTicketRectificationDocumentUrl(object):
    ws_entry_point = '{}/ticketrectificationdocuments'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# TicketRectificationDocument
class TicketRectificationDocumentList(GenTicketRectificationDocumentUrl, GenList):
    model = PurchasesTicketRectificationDocument
    extra_context = {'menu': ['TicketRectificationDocument', 'people'], 'bread': [_('TicketRectificationDocument'), _('People')]}


class TicketRectificationDocumentCreate(GenTicketRectificationDocumentUrl, DocumentFileView, GenCreate):
    model = PurchasesTicketRectificationDocument
    form_class = TicketRectificationDocumentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(TicketRectificationDocumentCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            obj = PurchasesTicketRectification.objects.get(pk=self.__pk)
            self.request.ticket_rectification = obj
            form.instance.ticket_rectification = obj

        return super(TicketRectificationDocumentCreate, self).form_valid(form)


class TicketRectificationDocumentCreateModal(GenCreateModal, TicketRectificationDocumentCreate):
    pass


class TicketRectificationDocumentUpdate(GenTicketRectificationDocumentUrl, DocumentFileView, GenUpdate):
    model = PurchasesTicketRectificationDocument
    form_class = TicketRectificationDocumentForm


class TicketRectificationDocumentUpdateModal(GenUpdateModal, TicketRectificationDocumentUpdate):
    pass


class TicketRectificationDocumentDelete(GenTicketRectificationDocumentUrl, GenDelete):
    model = PurchasesTicketRectificationDocument


class TicketRectificationDocumentSubList(GenTicketRectificationDocumentUrl, GenList):
    model = PurchasesTicketRectificationDocument

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(ticket_rectification__pk=pk)
        return limit


class TicketRectificationDocumentDetails(GenTicketRectificationDocumentUrl, GenDetail):
    model = PurchasesTicketRectificationDocument
    groups = TicketRectificationDocumentForm.__groups_details__()
    template_model = "purchases/ticketrectificationdocument_details.html"


class TicketRectificationDocumentDetailsModal(GenDetailModal, TicketRectificationDocumentDetails):
    pass


# ###########################################
class GenInvoiceDocumentUrl(object):
    ws_entry_point = '{}/invoicedocuments'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# InvoiceDocument
class InvoiceDocumentList(GenInvoiceDocumentUrl, GenList):
    model = PurchasesInvoiceDocument
    extra_context = {'menu': ['InvoiceDocument', 'people'], 'bread': [_('InvoiceDocument'), _('People')]}


class InvoiceDocumentCreate(GenInvoiceDocumentUrl, DocumentFileView, GenCreate):
    model = PurchasesInvoiceDocument
    form_class = InvoiceDocumentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(InvoiceDocumentCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            obj = PurchasesInvoice.objects.get(pk=self.__pk)
            self.request.invoice = obj
            form.instance.invoice = obj

        return super(InvoiceDocumentCreate, self).form_valid(form)


class InvoiceDocumentCreateModal(GenCreateModal, InvoiceDocumentCreate):
    pass


class InvoiceDocumentUpdate(GenInvoiceDocumentUrl, DocumentFileView, GenUpdate):
    model = PurchasesInvoiceDocument
    form_class = InvoiceDocumentForm


class InvoiceDocumentUpdateModal(GenUpdateModal, InvoiceDocumentUpdate):
    pass


class InvoiceDocumentDelete(GenInvoiceDocumentUrl, GenDelete):
    model = PurchasesInvoiceDocument


class InvoiceDocumentSubList(GenInvoiceDocumentUrl, GenList):
    model = PurchasesInvoiceDocument

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(invoice__pk=pk)
        return limit


class InvoiceDocumentDetails(GenInvoiceDocumentUrl, GenDetail):
    model = PurchasesInvoiceDocument
    groups = InvoiceDocumentForm.__groups_details__()
    template_model = "purchases/invoicedocument_details.html"


class InvoiceDocumentDetailsModal(GenDetailModal, InvoiceDocumentDetails):
    pass


# ###########################################
class GenInvoiceRectificationDocumentUrl(object):
    ws_entry_point = '{}/invoicerectificationdocuments'.format(settings.CDNX_INVOICING_URL_PURCHASES)


# InvoiceRectificationDocument
class InvoiceRectificationDocumentList(GenInvoiceRectificationDocumentUrl, GenList):
    model = PurchasesInvoiceRectificationDocument
    extra_context = {'menu': ['InvoiceRectificationDocument', 'people'], 'bread': [_('InvoiceRectificationDocument'), _('People')]}


class InvoiceRectificationDocumentCreate(GenInvoiceRectificationDocumentUrl, DocumentFileView, GenCreate):
    model = PurchasesInvoiceRectificationDocument
    form_class = InvoiceRectificationDocumentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk', None)
        return super(InvoiceRectificationDocumentCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__pk:
            obj = PurchasesInvoiceRectification.objects.get(pk=self.__pk)
            self.request.invoice_rectification = obj
            form.instance.invoice_rectification = obj

        return super(InvoiceRectificationDocumentCreate, self).form_valid(form)


class InvoiceRectificationDocumentCreateModal(GenCreateModal, InvoiceRectificationDocumentCreate):
    pass


class InvoiceRectificationDocumentUpdate(GenInvoiceRectificationDocumentUrl, DocumentFileView, GenUpdate):
    model = PurchasesInvoiceRectificationDocument
    form_class = InvoiceRectificationDocumentForm


class InvoiceRectificationDocumentUpdateModal(GenUpdateModal, InvoiceRectificationDocumentUpdate):
    pass


class InvoiceRectificationDocumentDelete(GenInvoiceRectificationDocumentUrl, GenDelete):
    model = PurchasesInvoiceRectificationDocument


class InvoiceRectificationDocumentSubList(GenInvoiceRectificationDocumentUrl, GenList):
    model = PurchasesInvoiceRectificationDocument

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(invoice_rectification__pk=pk)
        return limit


class InvoiceRectificationDocumentDetails(GenInvoiceRectificationDocumentUrl, GenDetail):
    model = PurchasesInvoiceRectificationDocument
    groups = InvoiceRectificationDocumentForm.__groups_details__()
    template_model = "purchases/invoicerectificationdocument_details.html"


class InvoiceRectificationDocumentDetailsModal(GenDetailModal, InvoiceRectificationDocumentDetails):
    pass
