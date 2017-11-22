# -*- coding: utf-8 -*-
#
# django-codenerix-pos
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

from .views_cash import CashDiaryList, CashDiaryExplain, CashDiaryCreate, CashDiaryCreateModal, CashDiaryUpdate, CashDiaryUpdateModal, CashDiaryDelete, CashDiarySubList, CashDiaryDetails, CashDiaryDetailModal, CashDiaryReport
from .views_cash import CashMovementList, CashMovementReport, CashMovementCreate, CashMovementCreateModal, CashMovementUpdate, CashMovementUpdateModal, CashMovementDelete, CashMovementSubList, CashMovementDetails, CashMovementDetailModal
from .views_cash import CashDiaryOpenClose


urlpatterns = [
    url(r'^cashdiarys$', CashDiaryList.as_view(), name='CDNX_invoicing_cashdiarys_list'),
    url(r'^cashdiarys/report$', CashDiaryReport.as_view(), name='CDNX_invoicing_cashdiarys_report'),
    url(r'^cashdiarys/add$', CashDiaryCreate.as_view(), name='CDNX_invoicing_cashdiarys_add'),
    url(r'^cashdiarys/addmodal$', CashDiaryCreateModal.as_view(), name='CDNX_invoicing_cashdiarys_addmodal'),
    url(r'^cashdiarys/explain/(?P<pk>\w+)/(?P<action>\w+)/(?P<kind>\w+)$', CashDiaryExplain.as_view(), name='CDNX_invoicing_cashdiarys_explain'),
    url(r'^cashdiarys/(?P<pk>\w+)$', CashDiaryDetails.as_view(), name='CDNX_invoicing_cashdiarys_details'),
    url(r'^cashdiarys/(?P<pk>\w+)/edit$', CashDiaryUpdate.as_view(), name='CDNX_invoicing_cashdiarys_edit'),
    url(r'^cashdiarys/(?P<pk>\w+)/editmodal$', CashDiaryUpdateModal.as_view(), name='CDNX_invoicing_cashdiarys_editmodal'),
    url(r'^cashdiarys/(?P<pk>\w+)/delete$', CashDiaryDelete.as_view(), name='CDNX_invoicing_cashdiarys_delete'),
    url(r'^cashdiarys/(?P<pk>\w+)/sublist$', CashDiarySubList.as_view(), name='CDNX_invoicing_cashdiarys_sublist'),
    url(r'^cashdiarys/(?P<cpk>\w+)/sublist/add$', CashDiaryCreateModal.as_view(), name='CDNX_invoicing_cashdiarys_sublist_add'),
    url(r'^cashdiarys/(?P<cpk>\w+)/sublist/addmodal$', CashDiaryCreateModal.as_view(), name='CDNX_invoicing_cashdiarys_sublist_addmodal'),
    url(r'^cashdiarys/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', CashDiaryDetailModal.as_view(), name='CDNX_invoicing_cashdiarys_sublist_details'),
    url(r'^cashdiarys/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', CashDiaryUpdateModal.as_view(), name='CDNX_invoicing_cashdiarys_sublist_details'),
    url(r'^cashdiarys/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', CashDiaryDelete.as_view(), name='CDNX_invoicing_cashdiarys_sublist_delete'),

    url(r'^cashmovements$', CashMovementList.as_view(), name='CDNX_invoicing_cashmovements_list'),
    url(r'^cashmovements/report$', CashMovementReport.as_view(), name='CDNX_invoicing_cashmovements_report'),
    url(r'^cashmovements/add$', CashMovementCreate.as_view(), name='CDNX_invoicing_cashmovements_add'),
    url(r'^cashmovements/addmodal$', CashMovementCreateModal.as_view(), name='CDNX_invoicing_cashmovements_addmodal'),
    url(r'^cashmovements/(?P<pk>\w+)$', CashMovementDetails.as_view(), name='CDNX_invoicing_cashmovements_details'),
    url(r'^cashmovements/(?P<pk>\w+)/edit$', CashMovementUpdate.as_view(), name='CDNX_invoicing_cashmovements_edit'),
    url(r'^cashmovements/(?P<pk>\w+)/editmodal$', CashMovementUpdateModal.as_view(), name='CDNX_invoicing_cashmovements_editmodal'),
    url(r'^cashmovements/(?P<pk>\w+)/delete$', CashMovementDelete.as_view(), name='CDNX_invoicing_cashmovements_delete'),
    url(r'^cashmovements/(?P<pk>\w+)/sublist$', CashMovementSubList.as_view(), name='CDNX_invoicing_cashmovements_sublist'),
    url(r'^cashmovements/(?P<cpk>\w+)/sublist/add$', CashMovementCreateModal.as_view(), name='CDNX_invoicing_cashmovements_sublist_add'),
    url(r'^cashmovements/(?P<cpk>\w+)/sublist/addmodal$', CashMovementCreateModal.as_view(), name='CDNX_invoicing_cashmovements_sublist_addmodal'),
    url(r'^cashmovements/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', CashMovementDetailModal.as_view(), name='CDNX_invoicing_cashmovements_sublist_details'),
    url(r'^cashmovements/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', CashMovementUpdateModal.as_view(), name='CDNX_invoicing_cashmovements_sublist_details'),
    url(r'^cashmovements/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', CashMovementDelete.as_view(), name='CDNX_invoicing_cashmovements_sublist_delete'),

    url(r'^cashdiary$', CashDiaryOpenClose.as_view(), name='cashdiarys_cashdiary'),
]
