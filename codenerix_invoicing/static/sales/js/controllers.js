/*
 *
 * django-codenerix-invoicing
 *
 * Codenerix GNU
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

// Angular codenerix invoicing sales controllers
angular.module('codenerixSalesControllers', [])
.controller('codenerixSalesDetailsCtrl', ['$scope', '$rootScope', '$timeout', '$http', '$window', '$uibModal', '$uibModalStack', '$state', '$stateParams', '$templateCache', 'Register', '$location', 
    function($scope, $rootScope, $timeout, $http, $window, $uibModal, $uibModalStack, $state, $stateParams, $templateCache, Register, $location) {
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        var url = ws_entry_point+"/"+$stateParams.pk;

        function create_doc($scope, url, msg_line){
            var lines = [];
            $("input[name=checkline]:checked").each(function (){
                lines.push($(this).val());
            });
            if (lines.length != 0){
                var datas = {
                    'lines': lines
                };
                
                $http.post( url, datas, {})
                    .success(function(answer, stat) {
                        // Check the answer
                        if (stat==200 || stat ==202) {
                            // Reload details window
                            if ($scope.base_window != undefined){
                                $scope.base_window.dismiss('cancel');
                            }
                            if (answer.url == undefined){
                                alert(answer.error);
                            }else{
                                $window.location.href = answer.url;
                            }
                        } else {
                            // Error happened, show an alert
                            console.log("ERROR "+stat+": "+answer)
                            console.log(answer);
                            alert("ERROR "+stat+": "+answer)
                        }
                    })
                    .error(function(data, status, headers, config) {
                        if (cnf_debug){
                            alert(data);
                        }else{
                            alert(cnf_debug_txt);
                        }
                    });
            }else{
                if (typeof(msg_line) != 'undefined'){
                    alert(msg_line);
                }
            }
        }

        $scope.order_status_next = function(pk){
            var modalInstance = $uibModal.open({ templateUrl: 'executingModal.html', size: 'sm' });
            $http.post( "/"+ws_entry_point+"/"+pk+"/status/next" )
            .success(function(answer, stat) {
                if (answer['error']) {
                    $("#executingModal").html(answer['errortxt']);
                } else {
                    $uibModalStack.dismissAll();
                    $scope.$parent.$parent.refresh();
                }
            })
            .error(function(data) {
                alert("Some error happened while executing: "+data)
            });
        }
        $scope.create_budget = function(msg_line){
            create_doc($scope, "/"+url+"/createbudget", msg_line);
        };
        $scope.create_order = function(msg_line){
            create_doc($scope, "/"+url+"/createorder");
        };
        $scope.create_albaran = function(){
            create_doc($scope, "/"+url+"/createalbaran");
        };
        $scope.create_ticket = function(){
            create_doc($scope, "/"+url+"/createticket");
        };
        $scope.create_invoice = function(){
            create_doc($scope, "/"+url+"/createinvoice");
        };
        $scope.create_ticket_from_albaran = function(){
            create_doc($scope, "/"+url+"/createticket");
        };
        $scope.create_invoice_from_albaran = function(){
            create_doc($scope, "/"+url+"/createinvoice");
        };
        $scope.create_invoice_from_ticket = function(){
            create_doc($scope, "/"+url+"/createinvoice");
        };

        $scope.invoice_rectification = function(){
            var lines = [];
            var url = "/" + ws_entry_point+"/"+$stateParams.pk + "/createinvoicerectification"

            $("input[name=checkline]:checked").each(function (){
                lines.push($(this).val());
            });
            if (lines.length != 0){
                var datas = {
                    'lines': lines
                };
                
                $http.post( url, datas, {})
                    .success(function(answer, stat) {
                        // Check the answer
                        if (stat==200 || stat ==202) {
                            // Reload details window
                            if ($scope.base_window != undefined){
                                $scope.base_window.dismiss('cancel');
                            }
                            if (answer.url == undefined){
                                alert(answer.error);
                            }else{
                                $window.location.href = answer.url;
                            }
                        } else {
                            // Error happened, show an alert
                            console.log("ERROR "+stat+": "+answer)
                            console.log(answer);
                            alert("ERROR "+stat+": "+answer)
                        }
                    })
                    .error(function(data, status, headers, config) {
                        if (cnf_debug){
                            alert(data);
                        }else{
                            alert(cnf_debug_txt);
                        }
                    });
            }
        };

        $scope.ticket_rectification = function(){
            var lines = [];
            var url = "/" + ws_entry_point+"/"+$stateParams.pk + "/createticketrectification"

            $("input[name=checkline]:checked").each(function (){
                lines.push($(this).val());
            });
            if (lines.length != 0){
                var datas = {
                    'lines': lines
                };
                
                $http.post( url, datas, {})
                    .success(function(answer, stat) {
                        // Check the answer
                        if (stat==200 || stat ==202) {
                            // Reload details window
                            if ($scope.base_window != undefined){
                                $scope.base_window.dismiss('cancel');
                            }
                            if (answer.url == undefined){
                                alert(answer.error);
                            }else{
                                $window.location.href = answer.url;
                            }
                        } else {
                            // Error happened, show an alert
                            console.log("ERROR "+stat+": "+answer)
                            console.log(answer);
                            alert("ERROR "+stat+": "+answer)
                        }
                    })
                    .error(function(data, status, headers, config) {
                        if (cnf_debug){
                            alert(data);
                        }else{
                            alert(cnf_debug_txt);
                        }
                    });
            }
        };

        $scope.create_order_from_budget = function(){

            var functions = function(scope) {
            };
            var callback = function(scope) {
                $scope.refresh();
            };
            if ($scope.ws_base == undefined){
                $scope.ws_base = $scope.ws;
            }
            $scope.ws = $scope.ws_base + "/addfrombudget";
            openmodal($scope, $timeout, $uibModal, 'lg', functions, callback);
        };

        $scope.create_order_from_shopping_cart = function(){

            var functions = function(scope) {
            };
            var callback = function(scope) {
                $scope.refresh();
            };
            if ($scope.ws_base == undefined){
                $scope.ws_base = $scope.ws;
            }
            $scope.ws = $scope.ws_base + "/addfromshoppingcart";
            openmodal($scope, $timeout, $uibModal, 'lg', functions, callback);
        };
    }
])
.controller('SalesAlbaranDetailsCtrl', ['$scope', '$rootScope', '$timeout', '$http', '$window', '$uibModal', '$state', '$stateParams', '$templateCache', 'Register', 'hotkeys',
   function($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register, hotkeys) {
       if (ws_entry_point==undefined) { ws_entry_point=""; }
       multidetails($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register, 0, "/"+ws_entry_point, hotkeys);

        $scope.send_albaran = function(gobackurl, url) {

            var functions = function(scope) {};
            var callback = function(scope, answer) {
                $window.location.href = gobackurl;
            };
            var callback_cancel = function(scope, answer) {};

            function action(quickmodal_ok, quickmodal_error) {
                $http.get( url, {}, {} )
                .success(function(answer, stat) {
                    if (answer.return != 'OK'){
                        quickmodal_error(answer.return);
                    } else {
                        quickmodal_ok(answer);
                    }
                })
                .error(function(data, status, headers, config) {
                    if (cnf_debug){
                        if (data) {
                            quickmodal_error(data);
                        } else {
                            quickmodal_error(cnf_debug_txt);
                        }
                    } else {
                        quickmodal_error(cnf_debug_txt);
                    }
                });
            }

            quickmodal($scope, $timeout, $uibModal, 'sm', action, functions, callback, callback_cancel);
        };

    }
])
.controller('codenerixSalesListPackCtrl', ['$scope', '$rootScope', '$timeout', '$location', '$uibModal', '$templateCache', '$http', '$state', 'Register', 'ListMemory', 'hotkeys',
    function($scope, $rootScope, $timeout, $location, $uibModal, $templateCache, $http, $state, Register, ListMemory, hotkeys) {
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        multilist($scope, $rootScope, $timeout, $location, $uibModal, $templateCache, $http, $state, Register, ListMemory, 0, "/"+ws_entry_point, undefined, undefined, hotkeys);
    }
])
.controller('codenerixSalesSubListPackCtrl', ['$scope', '$rootScope', '$timeout', '$location', '$uibModal', '$templateCache', '$http', '$state', 'Register', 'ListMemory','hotkeys',
    function($scope, $rootScope, $timeout, $location, $uibModal, $templateCache, $http, $state, Register, ListMemory, hotkeys) {
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        var listid=$state.params.listid;
        if (listid!='') {
            if (CDNX_tabsref==undefined) {
                angular.forEach($scope.tabs_autorender, function(value,key) {
                    $scope.tabs_autorender['t'+key]=false;
                });
                $scope.tabs_autorender['t'+$scope.tabsref[listid]]=true;
                CDNX_tabsref=$scope.tabsref;
            }
            $state.go('details0.sublist'+listid+'.rows',{'listid':listid});
            var register = angular.injector(['codenerixInlineServices']).get('Register'+listid);
            hotkeys = undefined; // Don't use it rignt now on sublist
            var ws = subws_entry_point[listid];
            multilist($scope, $rootScope, $timeout, $location, $uibModal, $templateCache, $http, $state, register, ListMemory, listid, ws, undefined, true, hotkeys);
            
            $scope.addnewpack = function () {
                if ($scope.data.meta.linkadd) {
                    // Base window
                    $scope.ws=ws+"/addpackmodal";
                    
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
                }
            };

        } else {
            // Activate autorender tabs
            angular.forEach(tabs_js, function(tab, i){
                if (tab.auto_open) {
                    $state.go('details0.sublist'+i+'.rows',{'listid':i});
                    return;
                }
            });
        }

    }
])
.controller('codenerixSalesLineBasketCtrl', ['$scope', '$rootScope', '$timeout', '$location', '$uibModal', '$templateCache', '$http', '$state', 'Register', 'ListMemory','hotkeys',
    function($scope){
        $scope.update_price = function(){
            var tax = $scope.tax;
            var price_base = $scope.price_base_basket;
            if (isNaN(price_base)){
                price_base = $scope.price_base_order;
            }

            if (isNaN(price_base)){
                price_base = 0;
            }
            if (isNaN(tax)){
                tax = 0;
            }else{
                tax = tax * price_base / 100;
            }
            var price = parseFloat(price_base) + parseFloat(tax);
            if ($scope[$scope.form_name]['price'] != undefined){
                $scope[$scope.form_name]['price'].$setViewValue(price.toFixed(2));
                $scope[$scope.form_name]['price'].$render();
            }
        }
    }
])
.controller('codenerixSalesReturnLineCtrl', ['$scope', '$rootScope', '$timeout', '$http', '$window', '$uibModal', '$state', '$stateParams', '$templateCache', 'Register',
    function($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register) {
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        var url = ws_entry_point+"/"+$stateParams.pk;

        modal_manager($scope, $timeout, $uibModal, $templateCache, $http, $scope);

        multidetails($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register, 0, "/"+ws_entry_point);

        $scope.return_product = function(path, apk){
            var functions = function(){};
            var callback = function(){
                //var reload = $("li.ng-isolate-scope.active").attr("ng-click").split("(")[1].split(")")[0].replace(/'/g, "");
                // $scope.$parent.refreshTab(reload);
            };
            $scope.ws = "/" + url + "/" + path + "/" + apk;
            openmodal($scope, $timeout, $uibModal, 'lg', functions, callback);
        };

        $scope.return_product_ticket = function(apk){
            $scope.return_product('ticket_rectification', apk);
        };

        $scope.return_product_invoice = function(apk){
            $scope.return_product('invoice_rectification', apk);
        };
    }
]);
