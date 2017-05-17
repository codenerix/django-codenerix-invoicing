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

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse

from django.template import loader
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import xhtml2pdf.pisa as pisa

from codenerix.multiforms import MultiForm
from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail, GenDetailModal

from codenerix_invoicing.models import BillingSeries, LegalNote, TypeDocument, MODELS, ProductStock
from codenerix_invoicing.forms import BillingSeriesForm, LegalNoteForm, TypeDocumentForm, ProductStockForm, ProductStockOwnForm

from codenerix_invoicing.models import StockMovement, StockMovementProduct, POS, Haulier
from codenerix_invoicing.forms import StockMovementForm, StockMovementProductForm, POSForm, HaulierForm

from codenerix_storages.models import StorageBatch
from codenerix_extensions.corporate.models import CorporateImage
from codenerix_extensions.files.views import ImageFileView


formsfull = {}
for info in MODELS:
    field = info[0]
    model = info[1]
    formsfull[model] = [(None, None, None)]
    for lang in settings.LANGUAGES:
        lang_code = lang[0]
        query = "from codenerix_invoicing.models import {}Text{}\n".format(model, lang_code.upper())
        query += "from codenerix_invoicing.forms import {}TextForm{}".format(model, lang_code.upper())
        exec(query)

        formsfull[model].append((eval("{}TextForm{}".format(model, lang_code.upper())), field, None))



# ###########################################
# Print PDF
class PrinterHelper(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PrinterHelper, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PrinterHelper, self).get_context_data(**kwargs)
        context["pdf"] = False
        # Get output
        self.__output = "pdf"
        extends = "sales/pdf/printer_pdf.html"
        # Set extends path
        context['extends_path'] = extends
        return context

    def render_to_response(self, context, **response_kwargs):
        output = self.__output
        if output is None:
            return super(PrinterHelper, self).render_to_response(context, **response_kwargs)
        elif output == "pdf":
            # Get data
            filename = "{0}.pdf".format(self.output_filename)
            html = loader.render_to_string(self.template_model, context, **response_kwargs)

            # Render the full document
            result = StringIO()

            pdf = pisa.pisaDocument(StringIO(html.encode('UTF-8')), result, encoding='UTF-8')

            # Check if we got an error
            if pdf.err:
                # Error happened
                answer = _('There was an error producing pdf')
                if settings.DEBUG:
                    answer += "\nDEBUG: {0}".format(pdf.err)
                raise IOError(answer)
            else:
                # Prepare answer
                response = HttpResponse(content_type="application/pdf")
                response['Content-Disposition'] = 'attachment; filename=%s' % (filename)
                response.write(result.getvalue())
                return response
        else:
            raise IOError("Can not render: unknown format '{0}'".format(output))


# ###########################################
class GenBillingSeriesUrl(object):
    ws_entry_point = '{}/billingseriess'.format(settings.CDNX_INVOICING_URL_COMMON)


# BillingSeries
class BillingSeriesList(GenBillingSeriesUrl, GenList):
    model = BillingSeries
    extra_context = {'menu': ['BillingSeries', 'people'], 'bread': [_('BillingSeries'), _('People')]}


class BillingSeriesCreate(GenBillingSeriesUrl, GenCreate):
    model = BillingSeries
    form_class = BillingSeriesForm


class BillingSeriesCreateModal(GenCreateModal, BillingSeriesCreate):
    pass


class BillingSeriesUpdate(GenBillingSeriesUrl, GenUpdate):
    model = BillingSeries
    form_class = BillingSeriesForm


class BillingSeriesUpdateModal(GenUpdateModal, BillingSeriesUpdate):
    pass


class BillingSeriesDelete(GenBillingSeriesUrl, GenDelete):
    model = BillingSeries


# ###########################################
# LegalNote
class LegalNoteList(GenList):
    model = LegalNote
    extra_context = {'menu': ['LegalNote', 'people'], 'bread': [_('LegalNote'), _('People')]}
    default_ordering = '-public'


class LegalNoteCreate(GenCreate):
    model = LegalNote
    form_class = LegalNoteForm


class LegalNoteCreateModal(GenCreateModal, LegalNoteCreate):
    pass


class LegalNoteUpdate(GenUpdate):
    model = LegalNote
    form_class = LegalNoteForm


class LegalNoteUpdateModal(GenUpdateModal, LegalNoteUpdate):
    pass


class LegalNoteDelete(GenDelete):
    model = LegalNote


# ###########################################
# TypeDocument
class TypeDocumentList(GenList):
    model = TypeDocument
    extra_context = {'menu': ['TypeDocument', 'people'], 'bread': [_('TypeDocument'), _('People')]}


class TypeDocumentCreate(MultiForm, GenCreate):
    model = TypeDocument
    form_class = TypeDocumentForm
    forms = formsfull["TypeDocument"]


class TypeDocumentCreateModal(GenCreateModal, TypeDocumentCreate):
    pass


class TypeDocumentUpdate(MultiForm, GenUpdate):
    model = TypeDocument
    form_class = TypeDocumentForm
    forms = formsfull["TypeDocument"]


class TypeDocumentUpdateModal(GenUpdateModal, TypeDocumentUpdate):
    pass


class TypeDocumentDelete(GenDelete):
    model = TypeDocument


# ###########################################
class GenProductStockUrl(object):
    ws_entry_point = '{}/productstocks'.format(settings.CDNX_INVOICING_URL_COMMON)


# ProductStock
class ProductStockList(GenProductStockUrl, GenList):
    model = ProductStock
    extra_context = {'menu': ['ProductStock', 'people'], 'bread': [_('ProductStock'), _('People')]}


class ProductStockCreate(GenProductStockUrl, GenCreate):
    model = ProductStock
    form_class = ProductStockForm


class ProductStockCreateModal(GenCreateModal, ProductStockCreate):
    pass


class ProductStockOwnCreateModal(GenCreateModal, ProductStockCreate):
    form_class = ProductStockOwnForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__storage_batch_pk = kwargs.get('pk', None)
        return super(ProductStockOwnCreateModal, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__storage_batch_pk:
            batch = StorageBatch.objects.get(pk=self.__storage_batch_pk)
            self.request.batch = batch
            form.instance.batch = batch

        return super(ProductStockOwnCreateModal, self).form_valid(form)
"""
"""


class ProductStockUpdate(GenProductStockUrl, GenUpdate):
    model = ProductStock
    form_class = ProductStockForm


class ProductStockUpdateModal(GenUpdateModal, ProductStockUpdate):
    pass


class ProductStockOwnUpdateModal(GenUpdateModal, ProductStockUpdate):
    form_class = ProductStockOwnForm


class ProductStockDelete(GenProductStockUrl, GenDelete):
    model = ProductStock


class ProductStockSubList(GenProductStockUrl, GenList):
    model = ProductStock
    show_details = False
    json = True
    template_model = "storages/productstock_sublist.html"
    extra_context = {'menu': ['ProductStock', 'people'], 'bread': [_('ProductStock'), _('People')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(batch__pk=pk)
        return limit


class ProductStockDetail(GenProductStockUrl, GenDetail):
    model = ProductStock
    groups = ProductStockForm.__groups_details__()
    template_model = "storages/productstock_details.html"


class ProductStockDetailModal(GenDetailModal, ProductStockDetail):
    pass


# ###########################################
# StockMovement
class StockMovementList(GenList):
    model = StockMovement
    show_details = True
    extra_context = {'menu': ['StockMovement', 'people'], 'bread': [_('StockMovement'), _('People')]}


class StockMovementCreate(GenCreate):
    model = StockMovement
    form_class = StockMovementForm


class StockMovementCreateModal(GenCreateModal, StockMovementCreate):
    pass


class StockMovementUpdate(GenUpdate):
    model = StockMovement
    form_class = StockMovementForm


class StockMovementUpdateModal(GenUpdateModal, StockMovementUpdate):
    pass


class StockMovementDelete(GenDelete):
    model = StockMovement


class StockMovementDetails(GenDetail):
    model = StockMovement
    groups = StockMovementForm.__groups_details__()
    template_model = 'codenerix_invoicing/stockmovement_details.html'

    tabs = [
        {'id': 'Products', 'name': _('Products'), 'ws': 'CDNX_invoicing_stockmovementproducts_sublist', 'wsbase': 'CDNX_invoicing_stockmovements_list', 'rows': 'base'},
    ]


class StockMovementPrint(PrinterHelper, GenDetail):
    model = StockMovement
    modelname = 'list'
    template_model = 'codenerix_invoicing/pdf/stockmovement_pdf.html'
    output_filename = '{0}{1}{2}_stockmovement'.format(datetime.now().year, datetime.now().month, datetime.now().day)

    def get_context_data(self, **kwargs):
        context = super(StockMovementPrint, self).get_context_data(**kwargs)

        movements = self.object

        context['media_root'] = settings.MEDIA_ROOT + '/'
        context['movement'] = movements
        context['line_stockmovements'] = movements.stock_movement_products.all()
        context['corporate_image'] = CorporateImage.objects.filter(public=True).first()

        return context


# ###########################################
# StockMovementProduct
class StockMovementProductList(GenList):
    model = StockMovementProduct
    extra_context = {'menu': ['StockMovementProduct', 'people'], 'bread': [_('StockMovementProduct'), _('People')]}


class StockMovementProductCreate(GenCreate):
    model = StockMovementProduct
    form_class = StockMovementProductForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__stock_movement_pk = kwargs.get('pk', None)
        return super(StockMovementProductCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__stock_movement_pk:
            stock_movement = StockMovement.objects.get(pk=self.__stock_movement_pk)
            self.request.stock_movement = stock_movement
            form.instance.stock_movement = stock_movement

        return super(StockMovementProductCreate, self).form_valid(form)


class StockMovementProductCreateModal(GenCreateModal, StockMovementProductCreate):
    pass


class StockMovementProductUpdate(GenUpdate):
    model = StockMovementProduct
    form_class = StockMovementProductForm


class StockMovementProductUpdateModal(GenUpdateModal, StockMovementProductUpdate):
    pass


class StockMovementProductDelete(GenDelete):
    model = StockMovementProduct


class StockMovementProductSubList(GenList):
    model = StockMovementProduct

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(stock_movement__pk=pk)
        return limit


class StockMovementProductDetails(GenDetail):
    model = StockMovementProduct
    groups = StockMovementProductForm.__groups_details__()


class StockMovementProductDetailModal(GenDetailModal, StockMovementProductDetails):
    pass


class POSList(GenList):
    model = POS


class POSCreate(GenCreate):
    model = POS
    form_class = POSForm


class POSCreateModal(GenCreateModal, POSCreate):
    pass


class POSUpdate(GenUpdate):
    model = POS
    form_class = POSForm


class POSUpdateModal(GenUpdateModal, POSUpdate):
    pass


class POSDelete(GenDelete):
    model = POS


# ###########################################
class GenHaulierUrl(object):
    ws_entry_point = '{}/hauliers'.format(settings.CDNX_INVOICING_URL_COMMON)


# Haulier
class HaulierList(GenHaulierUrl, GenList):
    model = Haulier
    extra_context = {'menu': ['Haulier', 'people'], 'bread': [_('Haulier'), _('People')]}


class HaulierCreate(GenHaulierUrl, ImageFileView, GenCreate):
    model = Haulier
    form_class = HaulierForm


class HaulierCreateModal(GenCreateModal, HaulierCreate):
    pass


class HaulierUpdate(GenHaulierUrl, GenUpdate):
    model = Haulier
    form_class = HaulierForm


class HaulierUpdateModal(GenUpdateModal, ImageFileView, HaulierUpdate):
    pass


class HaulierDelete(GenHaulierUrl, GenDelete):
    model = Haulier
