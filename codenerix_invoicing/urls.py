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
from codenerix_invoicing.views import BillingSeriesCreate, BillingSeriesCreateModal, BillingSeriesDelete, BillingSeriesList, BillingSeriesUpdate, BillingSeriesUpdateModal
from codenerix_invoicing.views import LegalNoteList, LegalNoteCreate, LegalNoteCreateModal, LegalNoteUpdate, LegalNoteUpdateModal, LegalNoteDelete
from codenerix_invoicing.views import ProductStockList, ProductStockCreate, ProductStockCreateModal, ProductStockUpdate, ProductStockUpdateModal, ProductStockDelete, ProductStockDetailModal
from codenerix_invoicing.views import ProductStockSubList, ProductStockOwnCreateModal, ProductStockOwnUpdateModal
from codenerix_invoicing.views import TypeDocumentList, TypeDocumentCreate, TypeDocumentCreateModal, TypeDocumentUpdate, TypeDocumentUpdateModal, TypeDocumentDelete
from codenerix_invoicing.views import StockMovementList, StockMovementCreate, StockMovementCreateModal, StockMovementUpdate, StockMovementDelete, StockMovementDetails, StockMovementPrint
from codenerix_invoicing.views import StockMovementProductCreateModal, StockMovementProductUpdateModal, StockMovementProductDelete, StockMovementProductSubList, StockMovementProductDetailModal
from codenerix_invoicing.views import HaulierList, HaulierCreate, HaulierCreateModal, HaulierUpdate, HaulierUpdateModal, HaulierDelete

from codenerix_invoicing.urls_sales import urlpatterns as url_sales
from codenerix_invoicing.urls_purchases import urlpatterns as url_purchases
from codenerix_invoicing.urls_cash import urlpatterns as url_cash


urlpatterns = [
    url(r'^billingseriess$', BillingSeriesList.as_view(), name='CDNX_invoicing_billingseriess_list'),
    url(r'^billingseriess/add$', BillingSeriesCreate.as_view(), name='CDNX_invoicing_billingseriess_add'),
    url(r'^billingseriess/addmodal$', BillingSeriesCreateModal.as_view(), name='CDNX_invoicing_billingseriess_addmodal'),
    url(r'^billingseriess/(?P<pk>\w+)/edit$', BillingSeriesUpdate.as_view(), name='CDNX_invoicing_billingseriess_edit'),
    url(r'^billingseriess/(?P<pk>\w+)/editmodal$', BillingSeriesUpdateModal.as_view(), name='CDNX_invoicing_billingseriess_editmodal'),
    url(r'^billingseriess/(?P<pk>\w+)/delete$', BillingSeriesDelete.as_view(), name='CDNX_invoicing_billingseriess_delete'),

    url(r'^legalnotes$', LegalNoteList.as_view(), name='CDNX_invoicing_legalnotes_list'),
    url(r'^legalnotes/add$', LegalNoteCreate.as_view(), name='CDNX_invoicing_legalnotes_add'),
    url(r'^legalnotes/addmodal$', LegalNoteCreateModal.as_view(), name='CDNX_invoicing_legalnotes_addmodal'),
    url(r'^legalnotes/(?P<pk>\w+)/edit$', LegalNoteUpdate.as_view(), name='CDNX_invoicing_legalnotes_edit'),
    url(r'^legalnotes/(?P<pk>\w+)/editmodal$', LegalNoteUpdateModal.as_view(), name='CDNX_invoicing_legalnotes_editmodal'),
    url(r'^legalnotes/(?P<pk>\w+)/delete$', LegalNoteDelete.as_view(), name='CDNX_invoicing_legalnotes_delete'),

    url(r'^typedocuments$', TypeDocumentList.as_view(), name='CDNX_invoicing_typedocuments_list'),
    url(r'^typedocuments/add$', TypeDocumentCreate.as_view(), name='CDNX_invoicing_typedocuments_add'),
    url(r'^typedocuments/addmodal$', TypeDocumentCreateModal.as_view(), name='CDNX_invoicing_typedocuments_addmodal'),
    url(r'^typedocuments/(?P<pk>\w+)/edit$', TypeDocumentUpdate.as_view(), name='CDNX_invoicing_typedocuments_edit'),
    url(r'^typedocuments/(?P<pk>\w+)/editmodal$', TypeDocumentUpdateModal.as_view(), name='CDNX_invoicing_typedocuments_editmodal'),
    url(r'^typedocuments/(?P<pk>\w+)/delete$', TypeDocumentDelete.as_view(), name='CDNX_invoicing_typedocuments_delete'),

    # ProductStock
    url(r'^productstocks$', ProductStockList.as_view(), name='CDNX_invoicing_productstocks_list'),
    url(r'^productstocks/add$', ProductStockCreate.as_view(), name='CDNX_invoicing_productstocks_add'),
    url(r'^productstocks/addmodal$', ProductStockCreateModal.as_view(), name='CDNX_invoicing_productstocks_addmodal'),
    url(r'^productstocks/(?P<pk>\w+)/edit$', ProductStockUpdate.as_view(), name='CDNX_invoicing_productstocks_edit'),
    url(r'^productstocks/(?P<pk>\w+)/editmodal$', ProductStockUpdateModal.as_view(), name='CDNX_invoicing_productstocks_editmodal'),
    url(r'^productstocks/(?P<pk>\w+)/delete$', ProductStockDelete.as_view(), name='CDNX_invoicing_productstocks_delete'),

    url(r'^productstocks/(?P<pk>\w+)/sublist/add$', ProductStockCreateModal.as_view(), name='CDNX_invoicing_productstocks_sublist_add'),
    url(r'^productstocks/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ProductStockDetailModal.as_view(), name='CDNX_invoicing_productstocks_sublist_details'),
    url(r'^productstocks/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', ProductStockUpdateModal.as_view(), name='CDNX_invoicing_productstocks_sublist_details'),
    url(r'^productstocks/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', ProductStockDelete.as_view(), name='CDNX_invoicing_productstocks_sublist_delete'),

    url(r'^productstocks/(?P<pk>\w+)/own/sublist$', ProductStockSubList.as_view(), name='CDNX_invoicing_own_productstocks_sublist'),
    url(r'^productstocks/(?P<pk>\w+)/own/sublist/add$', ProductStockOwnCreateModal.as_view(), name='CDNX_invoicing_own_productstocks_sublist_add'),
    url(r'^productstocks/(?P<cpk>\w+)/own/sublist/(?P<pk>\w+)$', ProductStockDetailModal.as_view(), name='CDNX_invoicing_own_productstocks_sublist_details'),
    url(r'^productstocks/(?P<cpk>\w+)/own/sublist/(?P<pk>\w+)/edit$', ProductStockOwnUpdateModal.as_view(), name='CDNX_invoicing_own_productstocks_sublist_details'),
    url(r'^productstocks/(?P<cpk>\w+)/own/sublist/(?P<pk>\w+)/delete$', ProductStockDelete.as_view(), name='CDNX_invoicing_own_productstocks_sublist_delete'),

    url(r'^stockmovements$', StockMovementList.as_view(), name='CDNX_invoicing_stockmovements_list'),
    url(r'^stockmovements/add$', StockMovementCreate.as_view(), name='CDNX_invoicing_stockmovements_add'),
    url(r'^stockmovements/addmodal$', StockMovementCreateModal.as_view(), name='CDNX_invoicing_stockmovements_addmodal'),
    url(r'^stockmovements/(?P<pk>\w+)$', StockMovementDetails.as_view(), name='CDNX_invoicing_stockmovements_details'),
    url(r'^stockmovements/(?P<pk>\w+)/edit$', StockMovementUpdate.as_view(), name='CDNX_invoicing_stockmovements_edit'),
    url(r'^stockmovements/(?P<pk>\w+)/delete$', StockMovementDelete.as_view(), name='CDNX_invoicing_stockmovements_delete'),
    url(r'^stockmovements/(?P<pk>\w+)/print$', StockMovementPrint.as_view(), name='CDNX_invoicing_stockmovements_print'),

    url(r'^stockmovementproducts/(?P<pk>\w+)/sublist$', StockMovementProductSubList.as_view(), name='CDNX_invoicing_stockmovementproducts_sublist'),
    url(r'^stockmovementproducts/(?P<pk>\w+)/sublist/addmodal$', StockMovementProductCreateModal.as_view(), name='CDNX_invoicing_stockmovementproducts_sublist_addmodal'),
    url(r'^stockmovementproducts/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', StockMovementProductDetailModal.as_view(), name='CDNX_invoicing_stockmovementproducts_sublist_details'),
    url(r'^stockmovementproducts/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', StockMovementProductUpdateModal.as_view(), name='CDNX_invoicing_stockmovementproducts_sublist_editmodal'),
    url(r'^stockmovementproducts/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', StockMovementProductDelete.as_view(), name='CDNX_invoicing_stockmovementproducts_sublist_delete'),

    url(r'^hauliers$', HaulierList.as_view(), name='CDNX_invoicing_hauliers_list'),
    url(r'^hauliers/add$', HaulierCreate.as_view(), name='CDNX_invoicing_hauliers_add'),
    url(r'^hauliers/addmodal$', HaulierCreateModal.as_view(), name='CDNX_invoicing_hauliers_addmodal'),
    url(r'^hauliers/(?P<pk>\w+)/edit$', HaulierUpdate.as_view(), name='CDNX_invoicing_hauliers_edit'),
    url(r'^hauliers/(?P<pk>\w+)/editmodal$', HaulierUpdateModal.as_view(), name='CDNX_invoicing_hauliers_editmodal'),
    url(r'^hauliers/(?P<pk>\w+)/delete$', HaulierDelete.as_view(), name='CDNX_invoicing_hauliers_delete'),


] + url_sales + url_purchases + url_cash
