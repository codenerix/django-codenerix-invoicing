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

from django.contrib import admin
from django.conf import settings

from codenerix_invoicing.models import BillingSeries, LegalNote, TypeDocument, ProductStock, StockMovement, StockMovementProduct, POS, MODELS
from codenerix_invoicing.models_purchases import Provider, PurchasesBudget, PurchasesLineBudget, PurchasesBudgetDocument, PurchasesOrder, PurchasesLineOrder, PurchasesOrderDocument, PurchasesAlbaran, PurchasesLineAlbaran, PurchasesAlbaranDocument, PurchasesTicket, PurchasesLineTicket, PurchasesTicketDocument, PurchasesTicketRectification, PurchasesLineTicketRectification, PurchasesTicketRectificationDocument, PurchasesInvoice, PurchasesLineInvoice, PurchasesInvoiceDocument, PurchasesInvoiceRectification, PurchasesLineInvoiceRectification, PurchasesInvoiceRectificationDocument
from codenerix_invoicing.models_sales import Address, Customer, CustomerDocument, SalesReservedProduct, SalesOrder, SalesLineOrder, SalesAlbaran, SalesLineAlbaran, SalesTicket, SalesLineTicket, SalesTicketRectification, SalesLineTicketRectification, SalesInvoice, SalesLineInvoice, SalesInvoiceRectification, SalesLineInvoiceRectification, SalesBasket, SalesLineBasket

admin.site.register(Provider)
admin.site.register(PurchasesBudget)
admin.site.register(PurchasesLineBudget)
admin.site.register(PurchasesBudgetDocument)
admin.site.register(PurchasesOrder)
admin.site.register(PurchasesLineOrder)
admin.site.register(PurchasesOrderDocument)
admin.site.register(PurchasesAlbaran)
admin.site.register(PurchasesLineAlbaran)
admin.site.register(PurchasesAlbaranDocument)
admin.site.register(PurchasesTicket)
admin.site.register(PurchasesLineTicket)
admin.site.register(PurchasesTicketDocument)
admin.site.register(PurchasesTicketRectification)
admin.site.register(PurchasesLineTicketRectification)
admin.site.register(PurchasesTicketRectificationDocument)
admin.site.register(PurchasesInvoice)
admin.site.register(PurchasesLineInvoice)
admin.site.register(PurchasesInvoiceDocument)
admin.site.register(PurchasesInvoiceRectification)
admin.site.register(PurchasesLineInvoiceRectification)
admin.site.register(PurchasesInvoiceRectificationDocument)

admin.site.register(BillingSeries)
admin.site.register(LegalNote)
admin.site.register(TypeDocument)
admin.site.register(ProductStock)
admin.site.register(StockMovement)
admin.site.register(StockMovementProduct)
admin.site.register(POS)

admin.site.register(Address)
admin.site.register(Customer)
admin.site.register(CustomerDocument)
admin.site.register(SalesReservedProduct)
admin.site.register(SalesBasket)
admin.site.register(SalesLineBasket)
admin.site.register(SalesOrder)
admin.site.register(SalesLineOrder)
admin.site.register(SalesAlbaran)
admin.site.register(SalesLineAlbaran)
admin.site.register(SalesTicket)
admin.site.register(SalesLineTicket)
admin.site.register(SalesTicketRectification)
admin.site.register(SalesLineTicketRectification)
admin.site.register(SalesInvoice)
admin.site.register(SalesLineInvoice)
admin.site.register(SalesInvoiceRectification)
admin.site.register(SalesLineInvoiceRectification)


for info in MODELS:
    model = info[1]
    for lang in settings.LANGUAGES:
        lang_code = lang[0].upper()
        query = "from codenerix_invoicing.models import {}Text{}\n".format(model, lang_code)
        query += "admin.site.register({}Text{})\n".format(model, lang_code)
        exec(query)
