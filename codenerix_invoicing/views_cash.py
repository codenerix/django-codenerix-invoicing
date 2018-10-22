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

from django.urls import reverse_lazy
from django.db import IntegrityError
from django.db.models import Q, Sum
from django.db.models.functions import TruncDate
from django.contrib.auth.decorators import login_required
from django.forms.utils import ErrorList
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.conf import settings

from codenerix.middleware import get_current_user
from codenerix.helpers import daterange_filter

from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail, GenDetailModal
from codenerix_pos.models import POS

from .models_cash import CashDiary, CashMovement
from .forms_cash import CashDiaryForm, CashDiaryExplainForm, CashMovementForm


# ###########################################
# CashDiary
class CashDiaryList(GenList):
    model = CashDiary
    show_details = True
    extra_context = {'menu': ['accounting', 'cashdiary'], 'bread': [_('Accounting'), _('CashDiary')]}
    client_context = {'error_margin': getattr(settings, "CASHDIARY_ERROR_MARGIN", 0.5)}
    default_ordering = "-opened_date"


class CashDiaryReport(GenList):
    model = CashDiary
    appname = 'invoicing'
    modelname = 'cashdiary'
    ws_entry_point = 'invoicing/cashdiarys/report'
    show_details = False
    extra_context = {'menu': ['accounting', 'cashdiaryreport'], 'bread': [_('Accounting'), _('CashDiary Report')]}
    linkadd = False
    linkedit = False
    annotations = {
        'date': TruncDate('opened_date')
    }
    default_ordering = "-date"

    def custom_queryset(self, queryset, info=None):
        return queryset.values('date', 'pos__name').annotate(**{
            'diff_cash': Sum('closed_cash') - Sum('opened_cash'),
            'diff_card': Sum('closed_cards') - Sum('opened_cards'),
        })

    def __searchF__(self, info):
        tf = {}
        tf['pos__name'] = (_('Point of Sales'), lambda x: Q(pos__name__icontains=x), 'input')
        tf['date'] = (_('Date'), lambda x: Q(**daterange_filter(x, 'opened_date')), 'daterange')
        return tf

    def __searchQ__(self, info, text):
        tf = {}
        tf['pos__name'] = Q(pos__name__icontains=text)
        return tf

    def __limitQ__(self, info):
        limits = {}
        limits['closed'] = Q(closed_user__isnull=False)
        return limits

    def __fields__(self, info):
        fields = []
        fields.append(('pos__name', _('Point of Sales')))
        fields.append(('date', _('Date')))
        fields.append(('diff_cash', _('Cash')))
        fields.append(('diff_card', _('Card')))
        return fields


class CashDiaryCreate(GenCreate):
    model = CashDiary
    show_details = True
    form_class = CashDiaryForm
    hide_foreignkey_button = True

    def form_valid(self, form):
        try:
            return super(CashDiaryCreate, self).form_valid(form)
        except IntegrityError as e:
            errors = form._errors.setdefault("other", ErrorList())
            errors.append(e)
            return super(CashDiaryCreate, self).form_invalid(form)


class CashDiaryCreateModal(GenCreateModal, CashDiaryCreate):
    pass


class CashDiaryUpdate(GenUpdate):
    model = CashDiary
    show_details = True
    form_class = CashDiaryForm
    hide_foreignkey_button = True

    def form_valid(self, form):
        try:
            return super(CashDiaryUpdate, self).form_valid(form)
        except IntegrityError as e:
            errors = form._errors.setdefault("other", ErrorList())
            errors.append(e)
            return super(CashDiaryUpdate, self).form_invalid(form)


class CashDiaryUpdateModal(GenUpdateModal, CashDiaryUpdate):
    pass


class CashDiaryExplain(GenUpdateModal, GenUpdate):
    template_name = 'codenerix_invoicing/cashdiary_explain.html'
    model = CashDiary
    form_class = CashDiaryExplainForm
    linkdelete = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__pk = kwargs.get('pk')
        self.__action = kwargs.get('action')
        self.__kind = kwargs.get('kind')
        return super(CashDiaryExplain, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        # Decide the field name
        if self.__action != 'opened':
            e1 = 'closed'
        else:
            e1 = 'opened'
        if self.__kind != 'cash':
            e2 = 'cards'
        else:
            e2 = 'cash'

        # Build the final kwargs
        kwargs = super(CashDiaryExplain, self).get_form_kwargs()
        kwargs.update(field_name=e1 + '_' + e2)
        return kwargs


class CashDiaryDelete(GenDelete):
    model = CashDiary


class CashDiarySubList(GenList):
    model = CashDiary
    show_details = False
    extra_context = {'menu': ['accounting', 'cashdiary'], 'bread': [_('Accounting'), _('CashDiary')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(pos__pk=pk)
        return limit


class CashDiaryDetails(GenDetail):
    model = CashDiary
    groups = CashDiaryForm.__groups_details__()
    tabs = [
        {'id': 'CashMovement', 'name': _('Cash movement'), 'ws': 'CDNX_invoicing_cashmovements_sublist', 'rows': 'base'},
    ]


class CashDiaryDetailModal(GenDetailModal, CashDiaryDetails):
    pass


# ###########################################
# CashMovement
class CashMovementList(GenList):
    model = CashMovement
    show_details = True
    extra_context = {'menu': ['accounting', 'CashMovement'], 'bread': [_('Accounting'), _('CashMovement')]}
    default_ordering = "-date_movement"


class CashMovementReport(View):
    template_name = 'accounting/CashMovement_report.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # Initialization
        context = {}
        context['menu'] = ('billing', 'CashMovementreport')
        context['bread'] = (_('Billing'), _('Cash Diary Report'))
        context['datas'] = []

        # Orders
        tickets = []
        tickets.append({
            'id': 'last7d',
            'title': _('Ultimos 7 dias'),
            # 'rows': [(x.user, x.order, x.amount) for x in CashMovement.objects.all()[:7]],
            'rows': [
                ('Hoy', 35, 498.4),
                ('Domingo', 32, 305.1),
                ('Sabado', 49, 622.3),
                ('Viernes', 45, 599.1),
                ('Jueves', 15, 115.4),
                ('Miercoles', 28, 324.3),
                ('Martes', 23, 316.7),
                ('Lunes', 15, 116.7),
            ],
        })
        tickets.append({
            'id': 'last4w',
            'title': _('Ultimas 4 semanas'),
            # 'rows': [(x.user, x.order, x.amount) for x in CashMovement.objects.all()[:4]],
            'rows': [
                ('Esta semana', 12, 125.22),
                ('Hace 1 semana', 298, 3245.88),
                ('Hace 2 semanas', 1884, 23125.43),
                ('Hace 3 semanas', 578, 6325.33),
                ('Hace 4 semanas', 778, 7145.49),
            ],
        })
        tickets.append({
            'id': 'last3m',
            'title': _('Ultimos 3 meses'),
            # 'rows': [(x.user, x.order, x.amount) for x in CashMovement.objects.all()[:3]],
            'rows': [
                ('Este mes', 139, 1842.52),
                ('Agosto', 1239, 12842.33),
                ('Julio', 439, 9842.74),
                ('Junio', 1839, 13842.14),
            ],
        })
        context['datas'].append({
            'title': _('Tickets'),
            'id': 'order',
            'columns': [_('Day'), _('Tickets'), _('Amount')],
            'graph': (0, 2),
            'lasts': tickets,
        })

        # People
        people = []
        people.append({
            'id': 'last7d',
            'title': _('Last 7 days'),
            'rows': [(x.user, x.order, x.amount) for x in CashMovement.objects.all()[:7]],
        })
        people.append({
            'id': 'last4w',
            'title': _('Last 4 weeks'),
            'rows': [(x.user, x.order, x.amount) for x in CashMovement.objects.all()[:4]],
        })
        people.append({
            'id': 'last3m',
            'title': _('Last 3 months'),
            'rows': [(x.user, x.order, x.amount) for x in CashMovement.objects.all()[:3]],
        })
        context['datas'].append({
            'title': _('People'),
            'id': 'person',
            'columns': [_('User'), _('Sales order'), _('Amount')],
            'graph': (0, 2),
            'lasts': people,
        })

        # Por hacer
        # 1: Tickets vendidos en el tiempo$
        # 2: Tickets vendidos por persona en el tiempo$
        # 3: Tickets cancelados en el tiempo$
        # 4: Tickets cancelados por persona en el tiempo$
        # --------------------
        # 5: Facturas en el tiempo
        # 6: Facturas por persona en el tiempo
        # --------------------
        # 7: Pedidos en el tiempo
        # 8: Pedidos por persona en el tiempo
        # --------------------
        # 9:  Motivos en el tiempo
        # 10: Motivos por persona en el tiempo

        # Render
        return render(request, self.template_name, context)


class CashMovementCreate(GenCreate):
    model = CashMovement
    show_details = True
    form_class = CashMovementForm
    hide_foreignkey_button = True

    def form_valid(self, form):
        user = get_current_user()
        form.instance.user = user
        self.request.user = user

        return super(CashMovementCreate, self).form_valid(form)


class CashMovementCreateModal(GenCreateModal, CashMovementCreate):
    pass


class CashMovementUpdate(GenUpdate):
    model = CashMovement
    show_details = True
    form_class = CashMovementForm
    hide_foreignkey_button = True


class CashMovementUpdateModal(GenUpdateModal, CashMovementUpdate):
    pass


class CashMovementDelete(GenDelete):
    model = CashMovement


class CashMovementSubList(GenList):
    model = CashMovement
    show_details = False
    extra_context = {'menu': ['accounting', 'CashMovement'], 'bread': [_('Accounting'), _('CashMovement')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(cash_diary__pk=pk)
        return limit


class CashMovementDetails(GenDetail):
    model = CashMovement
    groups = CashMovementForm.__groups_details__()
    """
    tabs = [
        {'id': 'CashMovementDay', 'name': _('CashMovement day'), 'ws': 'CashMovements_sublist', 'rows': 'base'},
    ]
    """


class CashMovementDetailModal(GenDetailModal, CashMovementDetails):
    pass


class CashDiaryOpenClose(View):

    def get_POS(self):
        uuid = self.request.session.get('POS_client_UUID', None)
        pos = POS.objects.filter(uuid=uuid).first()
        if pos:
            return {'uuid': str(pos.uuid), "POS": pos}
        else:
            return {'uuid': '', "POS": None}

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.template = 'codenerix_invoicing/cashdiary_openclose.html'
        action = request.GET.get('action', None)

        # Find a CashDiary
        PDV = self.get_POS()['POS']
        cashdiary = CashDiary.find(PDV, request.user)

        # Initialize context
        context = {}
        context['comma'] = '.'
        context['coin'] = '€'

        error = None
        title = None

        # Decide if we got a cashdiary or not
        if action == 'open':
            # If cashdiary exists
            if cashdiary:
                # Cashdiary exits, check if it is closed
                if cashdiary.closed_user:
                    # Cashdiary is closed and we are opening a new one, keep going
                    cash = (cashdiary.closed_cash, cashdiary.closed_cash)
                    cards = (cashdiary.closed_cards, cashdiary.closed_cards)
                    action_txt = _("Apertura de caja") + " - " + str(request.user.username)
                    title = [_('Ultimo cierre'), _('Apertura')]
                    label_btn = _('Abrir caja')
                else:
                    # Cashdiary already opened, we must stop here!
                    error = _("Cashdiary already opened")
            else:
                # No cashdiary found, create a new one, keep going!
                title = None
        elif action == 'close':
            # If cashdiary exists
            if cashdiary:
                # Cashdiary exists
                if cashdiary.closed_user:
                    # Cashdiary already closed, we must stop here!
                    error = _("Cashdiary already closed")
                else:
                    # Cashdiary is opened, we are closing this one, keep going
                    cash = (cashdiary.opened_cash, cashdiary.opened_cash + round(cashdiary.amount_cash(), 2))
                    cards = (cashdiary.opened_cards, cashdiary.opened_cards + round(cashdiary.amount_cards(), 2))
                    action_txt = _("Cierre de caja")
                    title = [_('Ultima apertura'), _('Cierre')]
                    label_btn = _('Cerrar caja')
            else:
                # No cashdiary found, we can not closed it, we must stop here!
                error = _("No Cashdiary found")
        else:
            error = "Unknown action"

        # Prepare action
        context['action'] = action
        if title:
            context['action_txt'] = action_txt
            context['info'] = {}
            context['info']['title'] = title
            context['info']['label_btn'] = label_btn
            context['info']['cash'] = ["{:.2f} €".format(cash[0]), "{:.2f} €".format(cash[1])]
            context['info']['cards'] = ["{:.2f} €".format(cards[0]), "{:.2f} €".format(cards[1])]
            context['info']['total'] = ["{:.2f} €".format(cash[0] + cards[0]), "{:.2f} €".format(cash[1] + cards[1])]
            context['values'] = [str(cash[1]), str(cards[1])]
        else:
            context['info'] = None

        context['error'] = error

        # Get template and render
        template = loader.get_template(self.template)
        return HttpResponse(template.render(context, request))

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):

        # Get data
        action = request.POST.get('action', None)
        try:
            amount_cash = float(request.POST.get('amount_cash', None))
            amount_cards = float(request.POST.get('amount_cards', None))
        except Exception:
            amount_cash = None
            amount_cards = None

        # If we got an amount
        answer = {}
        if amount_cash is not None and amount_cards is not None:
            # Get POS
            PDV = self.get_POS()['POS']
            # Find latest cashdiary
            latestCD = CashDiary.find(PDV, request.user)

            # Check action
            if action == 'open':
                # Check if we found a cash
                if latestCD:
                    closed_user = latestCD.closed_user
                    closed_cash = latestCD.closed_cash
                    closed_cards = latestCD.closed_cards
                else:
                    closed_user = True
                    closed_cash = amount_cash
                    closed_cards = amount_cards

                # Check if it is already closed
                if closed_user is not None:
                    # It is already closed, open a new one
                    cash = CashDiary()
                    cash.pos = PDV
                    cash.opened_cash = amount_cash
                    cash.opened_cash_extra = amount_cash - closed_cash
                    cash.opened_cards = amount_cards
                    cash.opened_cards_extra = amount_cards - closed_cards
                    cash.opened_user = request.user
                    cash.opened_date = timezone.now()
                    cash.save()
                    # Send the user back to vending_start
                    answer['error'] = None
                    answer['error_code'] = None
                    answer['url'] = reverse_lazy('home')
                else:
                    # Fail with opened
                    answer['error'] = _('CashDiary is already open!')
                    answer['error_code'] = 'E03'
            elif action == 'close':
                if latestCD:
                    if latestCD.closed_user is None:
                        # It is still open, close it!
                        latestCD.closed_cash = amount_cash
                        latestCD.closed_cash_extra = amount_cash - (latestCD.opened_cash + latestCD.amount_cash())
                        latestCD.closed_cards = amount_cards
                        latestCD.closed_cards_extra = amount_cards - (latestCD.opened_cards + latestCD.amount_cards())
                        latestCD.closed_user = request.user
                        latestCD.closed_date = timezone.now()
                        latestCD.save()
                        # Send the user back to vending_start
                        answer['error'] = None
                        answer['error_code'] = None
                        answer['url'] = reverse_lazy('home')
                    else:
                        # Fail with opened
                        answer['error'] = _('CashDiary is already open!')
                        answer['error_code'] = 'E02'
                else:
                    # Fail with opened
                    answer['error'] = _('You can not close a non-existant CashDiary!')
                    answer['error_code'] = 'E06'
            else:
                # Unknown action
                raise Http404("Unknown action")
        elif amount_cash is None:
            # Wrong amount
            answer['error'] = _('Wrong amount for cash!')
            answer['error_code'] = 'E04'
        elif amount_cards is not None:
            # Wrong amount
            answer['error'] = _('Wrong amount for cards!')
            answer['error_code'] = 'E05'
        else:
            # Wrong amount
            answer['error'] = _('Wrong amount!')
            answer['error_code'] = 'E01'

        # Return result
        return JsonResponse(answer)
