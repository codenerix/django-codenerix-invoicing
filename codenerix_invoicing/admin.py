# -*- coding: utf-8 -*-
#
# django-codenerix-invoicing
#
# Codenerix GNU
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

from .models_purchases import Provider, PurchasesBudget, PurchasesLineBudget, PurchasesBudgetDocument, PurchasesOrder, PurchasesLineOrder, PurchasesOrderDocument, PurchasesAlbaran, PurchasesLineAlbaran, PurchasesAlbaranDocument, PurchasesTicket, PurchasesLineTicket, PurchasesTicketDocument, PurchasesTicketRectification, PurchasesLineTicketRectification, PurchasesTicketRectificationDocument, PurchasesInvoice, PurchasesLineInvoice, PurchasesInvoiceDocument, PurchasesInvoiceRectification, PurchasesLineInvoiceRectification, PurchasesInvoiceRectificationDocument
from .models_sales import SalesAlbaran, SalesLines
from .models_cash import CashDiary, CashMovement

admin.site.register(CashDiary)
admin.site.register(CashMovement)

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

admin.site.register(SalesAlbaran)
admin.site.register(SalesLines)


"""
from .models import BillingSeries, LegalNote, TypeDocument, MODELS  # , StockMovement, StockMovementProduct
# from .models_sales import Address, Customer, CustomerDocument, SalesReservedProduct, SalesOrder, SalesLineOrder, SalesAlbaran, SalesLineAlbaran, SalesTicket, SalesLineTicket, SalesTicketRectification, SalesLineTicketRectification, SalesInvoice, SalesLineInvoice, SalesInvoiceRectification, SalesLineInvoiceRectification, SalesBasket, SalesLineBasket
# from .models_sales import SalesLineBasketOption
from .models_sales import ReasonModification, ReasonModificationLineBasket, ReasonModificationLineOrder, ReasonModificationLineAlbaran, ReasonModificationLineTicket, ReasonModificationLineTicketRectification, ReasonModificationLineInvoice, ReasonModificationLineInvoiceRectification

admin.site.register(Provider)

admin.site.register(BillingSeries)
admin.site.register(LegalNote)
admin.site.register(TypeDocument)
"""
# admin.site.register(StockMovement)
# admin.site.register(StockMovementProduct)
"""
admin.site.register(Address)
admin.site.register(Customer)
admin.site.register(CustomerDocument)
admin.site.register(SalesReservedProduct)
admin.site.register(SalesBasket)
admin.site.register(SalesLineBasket)
admin.site.register(SalesOrder)
admin.site.register(SalesLineOrder)
admin.site.register(SalesTicket)
admin.site.register(SalesLineTicket)
admin.site.register(SalesTicketRectification)
admin.site.register(SalesLineTicketRectification)
admin.site.register(SalesInvoice)
admin.site.register(SalesLineInvoice)
admin.site.register(SalesInvoiceRectification)
admin.site.register(SalesLineInvoiceRectification)

admin.site.register(SalesLineBasketOption)
admin.site.register(ReasonModification)
admin.site.register(ReasonModificationLineBasket)
admin.site.register(ReasonModificationLineOrder)
admin.site.register(ReasonModificationLineAlbaran)
admin.site.register(ReasonModificationLineTicket)
admin.site.register(ReasonModificationLineTicketRectification)
admin.site.register(ReasonModificationLineInvoice)
admin.site.register(ReasonModificationLineInvoiceRectification)
"""
"""

for info in MODELS:
    model = info[1]
    for lang in settings.LANGUAGES:
        lang_code = lang[0].upper()
        query = "from codenerix_invoicing.models import {}Text{}\n".format(model, lang_code)
        query += "admin.site.register({}Text{})\n".format(model, lang_code)
        exec(query)
"""
