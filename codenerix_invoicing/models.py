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

from django.db import models
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text

from codenerix.models import CodenerixModel
from django.conf import settings

from codenerix_extensions.files.models import GenImageFileNull

from codenerix_products.models import ProductFinal

from codenerix_storages.models import StorageBatch

from codenerix_invoicing.models_purchases import PurchasesLineAlbaran


STATUS_MOVEMENT_REQUESTED = 'R'
STATUS_MOVEMENT_SENT = 'S'
STATUS_MOVEMENT_DELIVERED = 'D'

STATUS_MOVEMENTS = (
    (STATUS_MOVEMENT_REQUESTED, _('Requested')),
    (STATUS_MOVEMENT_SENT, _('Sent')),
    (STATUS_MOVEMENT_DELIVERED, _('Delivered')),
)


# #####################################
# ######## Series de facturacion ######
# #####################################
# Series de facturación
class BillingSeries(CodenerixModel):
    code = models.CharField(_("Code"), max_length=12, blank=False, null=False, unique=True)
    description = models.CharField(_("Description"), max_length=250, blank=True, null=True)
    default = models.BooleanField(_("Default"), blank=False, default=False)
    observations = models.TextField(_("Observations"), max_length=256, blank=True, null=True)

    def __unicode__(self):
        return u"{}".format(smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('code', _('Code')))
        fields.append(('description', _('Description')))
        fields.append(('default', _('Default')))
        return fields

    def save(self, *args, **kwards):
        with transaction.atomic():
            if self.default:
                BillingSeries.objects.exclude(pk=self.pk).update(default=False)
            else:
                if not BillingSeries.objects.exclude(pk=self.pk).filter(default=True).exists():
                    self.default = True
        return super(BillingSeries, self).save(*args, **kwards)


# #####################################
# ######## Notas Legales ##############
# se adjuntan a los documentos de Ventas (Sales)
# #####################################
# LegalNote
class LegalNote(CodenerixModel):
    legal_note = models.TextField(_("Legal_note"), blank=True, null=True)
    public = models.BooleanField(_("Public"), default=False)

    def __unicode__(self):
        return u"{}".format(smart_text(self.updated))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('updated', _('Last update')))
        fields.append(('legal_note', _('Description')))
        fields.append(('public', _('Default')))
        return fields

    def save(self, *args, **kwards):
        with transaction.atomic():
            if self.public:
                LegalNote.objects.exclude(pk=self.pk).update(public=False)
            elif not LegalNote.objects.exclude(pk=self.pk).filter(public=True).exists():
                self.public = True
        return super(LegalNote, self).save(*args, **kwards)


# #####################################
# ######## Tipos de documentos ########
# tipos de documentos, para clasificar los documentos adjuntos de los clientes
# #####################################
# TypeDocument
class TypeDocument(CodenerixModel):
    code = models.CharField(_("Code"), blank=False, null=False, max_length=128)

    def __unicode__(self):
        return u"{}".format(smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('code', _('Code')))
        return fields


class TypeDocumentText(CodenerixModel):  # META: Abstract class
    name = models.CharField(_("Name"), blank=False, null=False, max_length=128)
    description = models.TextField(_("Description"), blank=True, null=True)

    class Meta(CodenerixModel.Meta):
        abstract = True


MODELS = (('type_document', 'TypeDocument'), )
for info in MODELS:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "class {}Text{}(TypeDocumentText):\n".format(model, lang_code)
        query += "  {} = models.OneToOneField({}, on_delete=models.CASCADE, blank=False, null=False, related_name='{}')\n".format(field, model, lang_code.lower())
        exec(query)


# relación almacen-producto-cantidad
class ProductStock(CodenerixModel):
    line_albaran = models.ForeignKey(PurchasesLineAlbaran, on_delete=models.CASCADE, related_name='product_stocks', verbose_name=_("Line albaran"), null=False, blank=False)
    batch = models.ForeignKey(StorageBatch, related_name='product_stocks', verbose_name=_("Batch"), null=False, blank=False, on_delete=models.PROTECT)
    product_final = models.ForeignKey(ProductFinal, on_delete=models.CASCADE, related_name='product_stocks', verbose_name=_("Product"), null=False, blank=False)
    quantity = models.FloatField(_("Quantity"), null=False, blank=False)

    def __fields__(self, info):
        fields = []
        fields.append(('batch', _('Batch'), 100))
        fields.append(('product_final', _('Product'), 100))
        fields.append(('quantity', _('Quantity'), 100))
        return fields

    def __unicode__(self):
        return u"{}".format(self.product_final)

    def __str__(self):
        return self.__unicode__()


# movimiento de stock entre de almacenes
class StockMovement(CodenerixModel):
    batch_source = models.ForeignKey(StorageBatch, related_name='stock_movements_src', verbose_name=_("Batch source"), null=False, blank=False, on_delete=models.PROTECT)
    batch_destination = models.ForeignKey(StorageBatch, related_name='stock_movements_dst', verbose_name=_("Batch destionation"), null=False, blank=False, on_delete=models.PROTECT)
    status = models.CharField(_("Status"), max_length=1, choices=STATUS_MOVEMENTS, blank=False, null=False, default=STATUS_MOVEMENT_REQUESTED)

    def __fields__(self, info):
        fields = []
        fields.append(('batch_source', _('Batch source'), 100))
        fields.append(('batch_destination', _('Batch destination'), 100))
        fields.append(('stock_movement_products', _('Products'), 100))
        return fields

    def __unicode__(self):
        return u"{} -> {}".format(self.batch_source, self.batch_destination)

    def __str__(self):
        return self.__unicode__()


class StockMovementProduct(CodenerixModel):
    stock_movement = models.ForeignKey(StockMovement, on_delete=models.CASCADE, related_name='stock_movement_products', verbose_name=_("Stock movement"), null=False, blank=False)
    product_final = models.ForeignKey(ProductFinal, on_delete=models.CASCADE, related_name='stock_movement_products', verbose_name=_("Product"), null=False, blank=False)
    quantity = models.FloatField(_("Quantity"), null=False, blank=False)

    def __fields__(self, info):
        fields = []
        fields.append(('product_final', _('Product'), 100))
        fields.append(('quantity', _('Quantity'), 100))
        return fields

    def __unicode__(self):
        return u"{} ({})".format(self.product_final, self.quantity)

    def __str__(self):
        return self.__unicode__()


# transportista
class Haulier(CodenerixModel, GenImageFileNull):
    name = models.CharField(_("Name"), max_length=128, blank=False, null=False, unique=True)
    url_public = models.CharField(_("Url public"), max_length=250, blank=True, null=True)
    url_tracking = models.CharField(_("Url tracking"), max_length=250, blank=True, null=True)

    def __unicode__(self):
        return u"{}".format(smart_text(self.name))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('name', _('Name')))
        fields.append(('url_public', _('Url public')))
        fields.append(('url_tracking', _('Url tracking')))
        return fields
