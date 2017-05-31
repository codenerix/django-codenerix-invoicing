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

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import F, Sum

from codenerix_invoicing.models import POS, Haulier
from codenerix_invoicing.models_sales import SalesBasket, SalesLineBasket, ROLE_BASKET_SHOPPINGCART
from codenerix_products.models import ProductFinal


class ShoppingCartProxy(object):
    __slots__ = ['_lang', '_cart', '_session', '_apply_surcharge', '_lines', '_quantities', '_products', '_totals', '__price_base', '__price_tax', '__ws_line', '__wos_line', ]
    SESSION_KEY = 'cdnx-shopping-cart'

    def __init__(self, request):
        self._lang = None
        for x in settings.LANGUAGES:
            if x[0] == request.LANGUAGE_CODE:
                self._lang = request.LANGUAGE_CODE.lower()
                break
        else:
            self._lang = settings.LANGUAGES[0][0].lower()

        self._cart = None
        self._session = None
        self._apply_surcharge = False

        self.__price_base = None
        self.__price_tax = None
        self.__ws_line = None
        self.__wos_line = None

        if request.user.is_authenticated():
            customer = request.user.person.customer
            self._apply_surcharge = customer.apply_equivalence_surcharge

            try:
                self._cart = SalesBasket.objects.get(customer=customer, role=ROLE_BASKET_SHOPPINGCART)
            except ObjectDoesNotExist:
                pos = POS.objects.filter(default=True).first()
                self._cart = SalesBasket(customer=customer, role=ROLE_BASKET_SHOPPINGCART, point_sales=pos)
                self._cart.save()

            if hasattr(request.body, 'transport'):
                transport = Haulier.objects.filter(name=request.body.transport).first()
                if transport is None:
                    transport = Haulier()
                    transport.name = request.body.transport
                    transport.save()

                self._cart.haulier = transport
                self._cart.save()

            # Merge anonymous to user cart
            if ShoppingCartProxy.SESSION_KEY in request.session:
                for product_dict in request.session[ShoppingCartProxy.SESSION_KEY]:
                    try:
                        product = ProductFinal.objects.get(pk=product_dict['pk'])
                    except ObjectDoesNotExist:
                        product = None
                    if product:
                        try:
                            line = SalesLineBasket.objects.get(basket=self._cart, product=product)
                            line.quantity += product_dict['quantity']
                            line.save()
                        except ObjectDoesNotExist:
                            line = SalesLineBasket(basket=self._cart, product=product, quantity=product_dict['quantity'], price=product.price)
                            line.save()
                del request.session[ShoppingCartProxy.SESSION_KEY]
                request.session.modified = True
        else:
            if ShoppingCartProxy.SESSION_KEY not in request.session:
                request.session[ShoppingCartProxy.SESSION_KEY] = []
                request.session.modified = True

            self._session = request.session

        self._lines = None
        self._quantities = None
        self._products = None
        self._totals = None

    @property
    def lines(self):
        if self._lines is None:
            self._quantities = {}
            if self._cart is not None:
                self._lines = self._cart.line_basket_sales.all().values(
                    'product__pk',
                    'quantity'
                ).annotate(
                    pk=F('product__pk')
                )

                for line in self._lines:
                    line.pop('product__pk')
                    self._quantities[line['pk']] = line['quantity']

            elif self._session is not None:
                self._lines = self._session[ShoppingCartProxy.SESSION_KEY]
                self._quantities = {line['pk']: line['quantity'] for line in self._lines}

        return self._lines

    @property
    def products(self):
        if self._products is None:
            products = ProductFinal.objects.filter(
                pk__in=[int(line['pk']) for line in self.lines]
            ).select_related(
                'product',
            ).only(
                'pk',
                'price',
                'stock_real',
                '{}__name'.format(self._lang),
                '{}__slug'.format(self._lang),
                '{}__description_short'.format(self._lang),
                'product__id',
                'product__code',
                'product__force_stock',
            ).annotate(
                product_pk=F('product__id'),
                name=F('{}__name'.format(self._lang)),
                slug=F('{}__slug'.format(self._lang)),
                description=F('{}__description_short'.format(self._lang)),
                code=F('product__code'),
                force_stock=F('product__force_stock')
            )

            self._products = {
                'count': 0,
                'subtotal': 0.0,
                'total': 0.0,
                'tax': 0.0,
                'products': [],
            }

            for final_product in products:

                features = final_product.product.product_features.all().values(
                    'feature__{}__description'.format(self._lang),
                    'value'
                ).annotate(
                    name=F('feature__{}__description'.format(self._lang))
                )

                attributes = final_product.products_final_attr.all().values(
                    'attribute__{}__description'.format(self._lang),
                    'value'
                ).annotate(
                    name=F('attribute__{}__description'.format(self._lang))
                )
                price = final_product.calculate_price(self._apply_surcharge)

                stock_locked = final_product.line_basket_sales.filter(
                    basket__expiration_date__isnull=False
                ).aggregate(
                    quantity=Sum('quantity')
                )['quantity'] or 0

                self._products['products'].append({
                    'pk': final_product.pk,
                    'name': final_product.name,
                    'code': final_product.code,
                    'description': final_product.description,
                    'url': reverse('sluglevel_get', args=(final_product.slug,)),
                    'thumbnail': final_product.product.products_image.filter(principal=True).first().image.url,
                    'quantity': self._quantities[final_product.pk],
                    'stock_real': final_product.stock_real - stock_locked,
                    'force_stock': int(final_product.force_stock),
                    'tax': self._quantities[final_product.pk] * price['tax'],
                    'base_price': price['price_base'],
                    'unit_price': price['price_total'],
                    'overcharge': price['overcharge'],
                    'total_price': self._quantities[final_product.pk] * price['price_total'],
                    'features': [{
                        'name': feature['name'],
                        'value': feature['value']
                    } for feature in features],
                    'attributes': [{
                        'name': attribute['name'],
                        'value': attribute['value'],
                    } for attribute in attributes]
                })

                self._products['count'] += 1
                self._products['subtotal'] += self._quantities[final_product.pk] * price['price_base']
                self._products['total'] += (price['price_base'] + self._products['products'][-1]['tax'])
                self._products['tax'] += self._products['products'][-1]['tax']

        return self._products

    @property
    def totals(self):
        if self._totals is None:
            products = ProductFinal.objects.filter(
                pk__in=[int(line['pk']) for line in self.lines]
            ).select_related(
                'product',
            ).only(
                'pk',
                'price',
                'product__tax__tax'
            )

            self._totals = {
                'count': 0,
                'subtotal': 0.0,
                'total': 0.0,
                'tax': 0.0,
            }

            for final_product in products:
                price = final_product.calculate_price(self._apply_surcharge)
                self._totals['count'] += 1
                self._totals['subtotal'] += self._quantities[final_product.pk] * price['price_base']
                self._totals['total'] += self._quantities[final_product.pk] * price['price_total']
                self._totals['tax'] += self._quantities[final_product.pk] * price['tax']

        return self._totals

    @property
    def user_cart(self):
        return self._cart

    def set_address(self, address_invoice, address_delivery):
        self._cart.address_invoice = address_invoice.address_invoice
        self._cart.address_delivery = address_delivery.address_delivery
        self._cart.save()

    def product(self, product_pk):
        product = ProductFinal.objects.get(pk=product_pk)
        price = product.calculate_price(self._apply_surcharge)

        result = self.totals.copy()
        result['total_price'] = self._quantities[product_pk] * price['price_total']

        return result

    def get_info_prices(self):
        if not self.__price_tax or not self.__price_base:

            with_stock = []
            without_stock = []

            price_base = 0
            price_tax = 0
            ws_line = {}
            wos_line = None

            for line in self.products['products']:
                ws_line = {
                    'description': line['name'],
                    'price': float("{0:.2f}".format(line['unit_price'] * line['quantity'])),
                    'quantity': line['quantity'],
                }
                wos_line = {
                    'description': line['name'],
                    'price': float("{0:.2f}".format(line['base_price'])),
                    'quantity': 0
                }

                if line['force_stock']:
                    if line['stock_real'] >= line['quantity']:
                        wos_line = None
                    else:
                        if line['stock_real'] == 0:
                            ws_line = None
                        wos_line['quantity'] = line['quantity'] - line['stock_real']
                else:
                    wos_line = None

                if ws_line:
                    with_stock.append(ws_line)
                    price_base += float("{0:.2f}".format(line['base_price'] * line['quantity']))
                    price_tax += float("{0:.2f}".format((line['tax'] - line['overcharge'])))
                if wos_line:
                    without_stock.append(wos_line)

            if without_stock:
                without_stock += with_stock
                with_stock = []

            prices = {
                'price_base': round(float("{0:.2f}".format(price_base)) * 100, 2) / 100,
                'price_tax': round(float("{0:.2f}".format(price_tax)) * 100, 2) / 100,
                'price_total': round(float("{0:.2f}".format(price_tax + price_base)) * 100, 2) / 100,
                'products_with_stock': with_stock,
                'products_without_stock': without_stock,
            }
        else:
            prices = {
                'price_base': round(float("{0:.2f}".format(self.__price_base)) * 100, 2) / 100,
                'price_tax': round(float("{0:.2f}".format(self.__price_tax)) * 100, 2) / 100,
                'price_total': round(float("{0:.2f}".format(self.__price_tax + self.__price_base)) * 100, 2) / 100,
                'ws_line': self.__ws_line,
                'wos_line': self.__wos_line,
            }
        return prices

    def _reset_data(self):
        self._lines = None
        self._quantities = None
        self._products = None
        self._totals = None
        # info prices
        self.__price_base = None
        self.__price_tax = None
        self.__ws_line = None
        self.__wos_line = None

    def _set_product(self, product_pk, quantity, add=False):
        product = ProductFinal.objects.get(pk=product_pk)
        if self._cart is not None:
            try:
                line = SalesLineBasket.objects.get(basket=self._cart, product=product)
                line.quantity = line.quantity + quantity if add else quantity
            except ObjectDoesNotExist:
                line = SalesLineBasket(basket=self._cart, product=product)
                line.quantity = quantity
            finally:
                line.price = product.calculate_price()['price_total']
                line.save()
        elif self._session is not None:
            for product_dict in self._session[ShoppingCartProxy.SESSION_KEY]:
                if product_dict['pk'] == product.pk:
                    product_dict['quantity'] = product_dict['quantity'] + quantity if add else quantity
                    break
            else:
                self._session[ShoppingCartProxy.SESSION_KEY].append({
                    'pk': product_pk,
                    'quantity': quantity
                })
            self._session.modified = True

    def add(self, product_pk, quantity):
        self._set_product(product_pk, quantity, add=True)
        self._reset_data()

    def edit(self, product_pk, quantity):
        self._set_product(product_pk, quantity)
        self._reset_data()

    def remove(self, product_pk):
        product = ProductFinal.objects.get(pk=product_pk)
        if self._cart is not None:
            line = SalesLineBasket.objects.get(basket=self._cart, product=product)
            line.delete()
        elif self._session is not None:
            if ShoppingCartProxy.SESSION_KEY in self._session:
                for product in self._session[ShoppingCartProxy.SESSION_KEY]:
                    if product['pk'] == product_pk:
                        self._session[ShoppingCartProxy.SESSION_KEY].remove(product)
                        self._session.modified = True
        self._reset_data()
