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

from django.utils.translation import ugettext as _
from django.conf import settings

from codenerix.forms import GenModelForm
from codenerix.widgets import WysiwygAngularInput

from codenerix_invoicing.models import BillingSeries, LegalNote, TypeDocument, MODELS, ProductStock, StockMovement, StockMovementProduct, Haulier


class BillingSeriesForm(GenModelForm):
    class Meta:
        model = BillingSeries
        exclude = []
        widgets = {
            'description': WysiwygAngularInput(),
            'observations': WysiwygAngularInput(),
        }
        
    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['code', 6],
                ['default', 6],
                ['description', 6],
                ['observations', 6],)
        ]
        return g


class LegalNoteForm(GenModelForm):
    class Meta:
        model = LegalNote
        exclude = []
        widgets = {
            'legal_note': WysiwygAngularInput()
        }

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['legal_note', 6],
                ['public', 6],)
        ]
        return g


class TypeDocumentForm(GenModelForm):
    class Meta:
        model = TypeDocument
        exclude = []

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['code', 6],)
        ]
        return g


# MODELS
for info in MODELS:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        exec("from codenerix_invoicing.models import {}Text{}\n".format(model, lang_code))
        query = """
class {model}TextForm{lang}(GenModelForm):\n
    class Meta:\n
        model={model}Text{lang}\n
        exclude = []\n
        widgets = {{\n
            'description': WysiwygAngularInput(),\n
        }}\n
    def __groups__(self):\n
        return [(_('Details'),12,"""
        if lang_code == settings.LANGUAGES_DATABASES[0]:
            query += """
                ['name', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('name', '{model}TextForm', [{languages}])"]],
                ['description', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('description', '{model}TextForm', [{languages}])"]],
            )]\n"""
        else:
            query += """
                ['name', 12],
                ['description', 12],
            )]\n"""

        exec(query.format(model=model, lang=lang_code, languages="'{}'".format("','".join(settings.LANGUAGES_DATABASES))))


class ProductStockForm(GenModelForm):
    class Meta:
        model = ProductStock
        exclude = []

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['batch', 6],
                ['product_final', 6],
                ['quantity', 6],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['batch', 6],
                ['product_final', 6],
                ['quantity', 6],)
        ]
        return g


class ProductStockOwnForm(GenModelForm):
    class Meta:
        model = ProductStock
        exclude = ['batch']

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['product_final', 6],
                ['quantity', 6],)
        ]
        return g


class StockMovementForm(GenModelForm):
    class Meta:
        model = StockMovement
        exclude = []

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['batch_source', 6],
                ['batch_destination', 6],
                ['status', 6],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['batch_source', 6],
                ['batch_destination', 6],
                ['status', 6],)
        ]
        return g


class StockMovementProductForm(GenModelForm):
    class Meta:
        model = StockMovementProduct
        exclude = ['stock_movement', ]

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['product_final', 6],
                ['quantity', 6],)
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['product_final', 6],
                ['quantity', 6],)
        ]
        return g


class HaulierForm(GenModelForm):
    class Meta:
        model = Haulier
        exclude = ['name_file', ]
        
    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['name', 6],
                ['image', 6],
                ['url_public', 6],
                ['url_tracking', 6],)
        ]
        return g
