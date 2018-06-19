/*
 *
 * django-codenerix-storages
 *
 * Copyright 2017 Centrologic Computational Logistic Center S.L.
 *
 * Project URL : http://www.codenerix.com
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

'use strict';

// Angular codenerix Controllers
angular.module('codenerixInvoicingVendingControllers', [])

.controller('codenerixVendingCtrl', ['$scope', '$rootScope', '$timeout', '$location', '$uibModal', '$templateCache', '$http', '$state', 'Register', 'ListMemory',
    function($scope, $rootScope, $timeout, $location, $uibModal, $templateCache, $http, $state, Register, ListMemory) {
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        var ws = "/"+ws_entry_point;
        multilist($scope, $rootScope, $timeout, $location, $uibModal, $templateCache, $http, $state, Register, ListMemory, 0, ws);

        $scope.product_final = null;
        $scope.product_final_pk = null;
        $scope.product_unique = null;
        $scope.product_unique_pk = null;
        $scope.final_error = false;
        $scope.unique_new = false;
        $scope.inscope = null;

        $scope.clean_up = function () {
            // We are done here
            $scope.final_error = false;
            $scope.unique_new = false;
            $scope.inscope.product_final = "";
            $scope.inscope.product_unique = "";
            $scope.product_final = null;
            $scope.product_final_pk = null;
            $scope.product_unique = null;
            $scope.product_unique_pk = null;
            $scope.data.meta.context.final_focus = true;
            $scope.data.meta.context.unique_disabled = true;
            $scope.data.meta.context.caducity_disabled = true;
            $scope.data.meta.context.errors = {
                'zone': null,
                'quantity': null,
                'product': null,
                'unique': null,
                'caducity': null,
            };
            $scope.refresh();
        };

        $scope.product_changed = function (inscope) {
            // Save inscope
            $scope.inscope = inscope;

            // Filter product final
            $scope.product_final = $scope.inscope.product_final.split(" ")[0];
            $scope.final_error = false;
            $scope.inscope.product_final = $scope.product_final;

            if ($scope.product_final != "None" && $scope.product_final != ''){
                // Prepare URL
                var url = $scope.data.meta.context.ws.ean13_fullinfo;
                var eanurl = "/" + url.replace("/PRODUCT_FINAL_EAN13/", "/"+$scope.product_final+"/");
                // Query the product
                $http.get( eanurl, {}, {} )
                .success(function(answer, stat) {
                    if (stat==200 || stat ==202) {
                        // Decide next step
                        if (Object.keys(answer).length) {
                            // Set caducity status
                            $scope.data.meta.context.caducity_disabled = !answer.caducable;
                            $scope.data.meta.context.unique_disabled = !answer.unique;
                            $scope.product_final_pk = answer.pk
                            $scope.inscope.box = answer.box
                            $scope.product_unique_pk = answer.product_unique_pk

                            // Check for unique
                            if (answer.unique) {
                                $scope.data.meta.context.unique_focus = true;
                            } else {
                                if (answer.caducable) {
                                    $scope.data.meta.context.caducity_focus = true;
                                } else {
                                    // We are done here
                                    $scope.submit_scenario();
                                }
                            }
                        } else {
                            // No answer, invalid product
                            $scope.product_final = null;
                            $scope.product_final_pk = null;
                            $scope.data.meta.context.unique_disabled = true;
                            $scope.data.meta.context.caducity_disabled = true;
                            $scope.data.meta.context.final_focus = true;
                            $scope.final_error = true;
                        }
                    } else {
                        // Error happened, show an alert$
                        console.log("ERROR "+stat+": "+answer);
                        console.log(answer);
                        $scope.data.meta.context.unique_disabled = true;
                        $scope.data.meta.context.caducity_disabled = true;
                        $scope.data.meta.context.final_focus = true;
                        $scope.final_error = true;
                        alert("ERROR "+stat+": "+answer);
                    }
                })
                .error(function(data, status, headers, config) {
                    if (cnf_debug){
                        alert(data);
                    } else {
                        alert(cnf_debug_txt)
                    }
                });
            }else{

                $scope.product_final = null;
                $scope.product_final_pk = null;
                $scope.data.meta.context.unique_disabled = true;
                $scope.data.meta.context.caducity_disabled = true;
                $scope.data.meta.context.final_focus = true;
                $scope.final_error = true;
            }
        };

        $scope.unique_changed = function () {

            // Filter product final
            var url = $scope.data.meta.context.ws.unique_fullinfo;
            $scope.product_unique = $scope.inscope.product_unique.split(" ")[0];
            $scope.inscope.product_unique = $scope.product_unique;

            // Prepare URL
            var uniqueurl = "/" + url.replace("/PRODUCT_FINAL_UNIQUE/", "/"+$scope.product_unique+"/");

            // Query the product
            $http.get( uniqueurl, {}, {} )
            .success(function(answer, stat) {
                if (stat==200 || stat ==202) {
                    if (Object.keys(answer).length) {
                        $scope.product_unique_pk = answer.pk;
                        $scope.unique_new = false;
                    } else {
                        $scope.product_unique_pk = null;
                        $scope.unique_new = true;
                    }
                    if (!$scope.data.meta.context.caducity_disabled) {
                        $scope.data.meta.context.caducity_focus = true;
                    } else {
                        // We are done here
                        $scope.submit_scenario();
                    }
                } else {
                     // Error happened, show an alert$
                     console.log("ERROR "+stat+": "+answer);
                     console.log(answer);
                     alert("ERROR "+stat+": "+answer);
                }
            })
            .error(function(data, status, headers, config) {
                if (cnf_debug){
                    alert(data);
                } else {
                    alert(cnf_debug_txt)
                }
            });
        }

        $scope.submit_scenario = function () {
            // Prepare URL
            var url = '/'+$scope.data.meta.context.ws.submit;

            // Prepare DATA
            var data = {
                'product_final': $scope.product_final_pk,
                'product_unique': $scope.product_unique_pk,
                'product_unique_value': $scope.product_unique,
                'box': $scope.inscope.box,
                'quantity': $scope.inscope.quantity,
                'caducity': $scope.inscope.caducity,
            }

            $http.post( url, data, {} )
            .success(function(answer, stat) {
                angular.forEach($scope.data.meta.context.errors, function (value, key) {
                    $scope.data.meta.context.errors[key] = null;
                });
                if (stat==200 || stat ==202) {
                    if ((typeof(answer['head'])!='undefined') && (typeof(answer['head']['errors'])!='undefined')) {
                        angular.forEach(answer['head']['errors'], function (value, key) {
                            angular.forEach(value, function(error) {
                                if (value != null){
                                    if ($scope.data.meta.context.errors[key] == undefined){
                                        $scope.data.meta.context.errors[key] = value+".";
                                    }else{
                                        $scope.data.meta.context.errors[key] += value+".";
                                    }
                                }
                            });
                        });
                    } else {
                        // We are done here
                        $scope.clean_up();
                    }
                } else {
                     // Error happened, show an alert$
                     console.log("ERROR "+stat+": "+answer);
                     console.log(answer);
                     alert("ERROR "+stat+": "+answer);
                }
            })
            .error(function(data, status, headers, config) {
                if (cnf_debug){
                    alert(data);
                } else {
                    alert(cnf_debug_txt)
                }
            });
        };

        $scope.edit_modal_line = function(pk){
            $scope.ws=ws+"/"+pk+"/editmodal";

            // Base Window functions
            var functions = function(scope) {};
            var callback = function(scope) {
                // Close our window
                if (scope.base_window) {
                    scope.base_window.dismiss('cancel');
                }
                $state.go($state.current, {listid:scope.listid});
                refresh(scope, $timeout, Register, undefined);
            };
            
            // Start modal window
            openmodal($scope, $timeout, $uibModal, 'lg', functions, callback);
        };

        $scope.open_cash_register = function(){
            var url = '/' + $scope.data.meta.context.ws.open_cash;
            $.get(url, function(data){
                console.log(data);
            }).done(function(data){

            }).fail(function(data){
                alert(data);
            }).always(function(data){

            });
        };

        $scope.open_pay = function(budget_pk){
            // Base Window functions
            var functions = function(scope) {};
            var callback = function(scope, answer) {
                // Open cash register
                scope.open_cash_register();
                $scope.refresh();
            };


            if ($scope.ws_base == undefined){
                $scope.ws_base = $scope.ws;
            }
            
            var url = '/' + $scope.data.meta.context.ws.pay_modal;
            $scope.ws = url;
            // Start modal window
            openmodal($scope, $timeout, $uibModal, 'lg', functions, callback);
        };

        $scope.open_print = function(budget_pk){
            var url = '/' + $scope.data.meta.context.ws.print;
            $scope.ws = url;
            $http.post( url, {}, {} )
                .success(function(answer, stat) {
                    if (answer.error != null){
                        alert(answer.error);
                    }
                })
                .error(function(data, status, headers, config) {
                    if (cnf_debug){
                        alert(data);
                    }else{
                        alert(cnf_debug_txt)
                    }
                });
        };

        $scope.open_cancel = function(budget_pk){};
    }
])
.controller('codenerixVendingPaymentCtrl', ['$scope', '$rootScope', '$timeout', '$http', '$window', '$uibModal', '$state', '$stateParams', '$templateCache', 'Register', '$location', 
    function($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register, $location) {
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        if ($stateParams.pk == undefined){
            var url = ws_entry_point;
        }else{
            var url = ws_entry_point+"/"+$stateParams.pk;
        }

        $scope.pay = function(){
            alert("AA");

            var functions = function(scope) {
            };
            var callback = function(scope, answer) {
                scope.open_cash_register();
                $window.location.reload();
                // $scope.refresh();
            };
            if ($scope.ws_base == undefined){
                $scope.ws_base = $scope.ws;
            }
            $scope.ws = "/" + url + "/pay";
            openmodal($scope, $timeout, $uibModal, 'lg', functions, callback);
        };

        /*
        var signed = false;
        $scope.sign = function(){

            var functions = function(scope) {
                $timeout($scope.is_signed, 1000);
            };
            var callback = function(scope) {
                $window.location.reload();
            };
            var callback_cancel = function($scope){
                signed = true;
                var path = "/" + url + "/cancelsign";
                $http.post( path, {}, {} )
                    .success(function(answer, stat) {
                        console.log(answer);
                    })
                    .error(function(data, status, headers, config) {
                        if (cnf_debug){
                            alert(data);
                        }else{
                            alert(cnf_debug_txt)
                        }
                    });
            };
            if ($scope.ws_base == undefined){
                $scope.ws_base = $scope.ws;
            }
            $scope.ws = "/" + url + "/sign";
            openmodal($scope, $timeout, $uibModal, 'lg', functions, callback, true, callback_cancel);
        };

        $scope.is_signed = function(){
            var path = "/" + url + "/issigned";
            if (signed == false){
                $http.post( path, {}, {} )
                    .success(function(answer, stat) {
                        if (answer.error != null){
                            console.log(answer.error);
                        }
                        if (answer.error != null || answer.msg=="OK"){
                            console.log($scope);
                            $window.location.reload();
                        }else{
                            $timeout($scope.is_signed, 1000);
                        }
                    })
                    .error(function(data, status, headers, config) {
                        if (cnf_debug){
                            alert(data);
                        }else{
                            alert(cnf_debug_txt)
                        }
                    });
            }
        };
        */
        $scope.print_ticket = function(){
            var path = "/" + url + "/ticket";
            alert(path);
            /*
            */
        };

        $scope.change_amount = function(field_amount_cash, field_amount_card, check_cash, check_card, field_total, field_result){
            var in_cash = $scope[$scope.form_name][field_amount_cash].$viewValue;
            var in_card = $scope[$scope.form_name][field_amount_card].$viewValue;
            var chk_cash = $scope[$scope.form_name][check_cash].$viewValue;
            var chk_card = $scope[$scope.form_name][check_card].$viewValue;
            var total = $scope[$scope.form_name][field_total].$viewValue;
            var amount = 0;
            if (chk_cash){
                amount+= parseFloat(in_cash);
            }
            if (chk_card){
                amount+= parseFloat(in_card);
            }
            var diff = total - amount;
            $scope[$scope.form_name][field_result].$setViewValue(diff.toFixed(2));
            $scope[$scope.form_name][field_result].$render();
        };

        $scope.open_cash_register = function(){
            var ruta = '/codenerix_pos/open_cash_register';
            $.get(ruta, function(data){
                console.log(data);
            }).done(function(data){

            }).fail(function(data){
                alert(data);
            }).always(function(data){

            });
        };

    }
]);

/*
al pagar que aparezca la pantalla de pago de recepción de boingjump con dos botones (pagar e imprimir)
el botón imprimir será cliqueable si aunque no se haya pagado el POS lo admite (nuevo flag en pos)
al pagar generar el pedido, albaran, albaran de salida (inventario)
al imprimir generar el pedido si no se ha generado aun, para bloquear los posiciones del presupuestos
*/
