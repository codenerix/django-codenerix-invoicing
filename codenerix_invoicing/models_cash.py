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

from django.db import models, IntegrityError
from django.db.models import Sum
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone, dateparse

from codenerix.models import CodenerixModel
from codenerix_invoicing.models_sales import SalesOrder
from codenerix_invoicing.models_purchases import PAYMENT_DETAILS, KIND_CARD, PAYMENT_DETAILS_CASH, PAYMENT_DETAILS_CARD
from codenerix_pos.models import POS, POSSlot


class CashDiary(CodenerixModel):
    pos = models.ForeignKey(POS, related_name='cash_movements', verbose_name=_("Point of Sales"), null=True)
    opened_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='opened_cash_diarys', verbose_name=_("User"))
    opened_date = models.DateTimeField(_("Opened Date"), blank=False, null=False)
    opened_cash = models.FloatField(_("Opened Cash"), blank=False, null=False)
    opened_cards = models.FloatField(_("Opened Cards"), blank=False, null=False)
    closed_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='closed_cash_diarys', verbose_name=_("User"), blank=True, null=True)
    closed_date = models.DateTimeField(_("Closed Date"), blank=True, null=True)
    closed_cash = models.FloatField(_("Closed Cash"), blank=True, null=True)
    closed_cards = models.FloatField(_("Closed Cards"), blank=True, null=True)

    def amount_cash(self):
        total = self.cash_movements.filter(kind=PAYMENT_DETAILS_CASH).annotate(total=Sum('amount')).values('total').first()
        if total:
            return total['total']
        else:
            return 0.0

    def amount_cards(self):
        total = self.cash_movements.filter(kind=PAYMENT_DETAILS_CARD).annotate(total=Sum('amount')).values('total').first()
        if total:
            return total['total']
        else:
            return 0.0

    @staticmethod
    def find(pos, user):
        '''
        Get a valid CashDiary for today from the given POS, it will return:
            - None: if no CashDiary is available today and older one was already closed
            - New CashDiary: if no CashDiary is available today but there is an older one which it was opened
            - Existing CashDiary: if a CashDiary is available today (open or close)
        '''

        # Get checkpoint
        ck = dateparse.parse_time(settings.get("CASHDIARY_CLOSES_AT", '03:00'))
        year = timezone.now().year
        month = timezone.now().month
        day = timezone.now().day
        hour = ck.hour
        minute = ck.minute
        second = ck.second
        checkpoint = timezone.datetime(year, month, day, hour, minute, second)

        # Get
        cashdiary = CashDiary.objects.filters(pos=pos, opened_date__gte=checkpoint).order_by("-opened_date").first()
        if not cashdiary:
            # No cashdiary found for today, check older one
            oldercashdiary = CashDiary.objects.filters(pos=pos, opened_date__lt=checkpoint).order_by("-opened_date").first()
            if oldercashdiary:
                if oldercashdiary.closed_user:
                    cashdiary = None
                else:
                    # Older cashdiary is not closed, we have to close it and open a new one
                    amount_cash = oldercashdiary.amount_cash()
                    amount_cards = oldercashdiary.amount_cards()
                    # The older cashdiary is still opened, we have to close it and create a new one
                    oldercashdiary.closed_cash = amount_cash
                    oldercashdiary.closed_cards = amount_cards
                    oldercashdiary.closed_user = user
                    oldercashdiary.closed_date = timezone.now()
                    oldercashdiary.save()
                    # Open new cashdiary
                    cashdiary = CashDiary()
                    cashdiary.pos = pos
                    cashdiary.opened_cash = amount_cash
                    cashdiary.opened_cards = amount_cards
                    cashdiary.opened_user = user
                    cashdiary.opened_date = timezone.now()
                    cashdiary.save()

        # Return the found CashDiary
        return cashdiary

    def __str__(self):
        return u"({}) {}: {}".format(smart_text(self.pos), smart_text(self.opened_user), smart_text(self.opened_date))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('pos', _('Point of Sales')))
        fields.append(('opened_user', _('Opened user')))
        fields.append(('opened_date', _('Opened date')))
        fields.append(('opened_cash', _('Opened cash')))
        fields.append(('opened_cards', _('Opened cards')))
        fields.append(('closed_user', _('Closed user')))
        fields.append(('closed_date', _('Closed date')))
        fields.append(('closed_cash', _('Closed cash')))
        fields.append(('closed_cards', _('Closed cards')))
        return fields

    def save(self, *args, **kwargs):
        if CashDiary.objects.filter(pos=self.pos, closed_date__isnull=True).exclude(pk=self.pk).exists():
            raise IntegrityError(_('Can not open a POS already open'))
        else:
            return super(CashDiary, self).save(*args, **kwargs)


class CashMovement(CodenerixModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cash_movements', verbose_name=_("User"))

    order = models.ManyToManyField(SalesOrder, related_name='cash_movements', verbose_name=_("Order"), symmetrical=False, blank=False, null=False)
    cash_diary = models.ForeignKey(CashDiary, related_name='cash_movements', verbose_name=_("Cash diary"), null=True)
    pos_slot = models.ForeignKey(POSSlot, related_name='cash_movements', verbose_name=_("Slot"), null=True)
    kind = models.CharField(_("Kind"), max_length=3, choices=PAYMENT_DETAILS, blank=False, null=False)
    kind_card = models.CharField(_("Kind Card"), max_length=3, choices=KIND_CARD, blank=True, null=True)
    date_movement = models.DateTimeField(_("Date of movement"), blank=False, null=False)
    amount = models.FloatField(_("Amount"), blank=False, null=False)

    def __str__(self):
        return u"{}".format(smart_text(self.order), smart_text(self.pos_slot), smart_text(self.amount))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('user', _('User')))
        fields.append(('order', _('Order')))
        fields.append(('cash_diary', _('Cash diary')))
        fields.append(('pos_slot', _('Slot')))
        fields.append(('get_kind_display', _('Kind')))
        fields.append(('get_kind_card_display', _('Kind Card')))
        fields.append(('date_movement', _('Date movement')))
        fields.append(('amount', _('Amount'), None, 'right'))
        return fields
