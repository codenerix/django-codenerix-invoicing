/*
 *
 * django-codenerix-invoicing
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

// Angular codenerix invoicing sales controllers
angular.module('codenerixSalesControllers', [])
.controller('codenerixSalesDetailsCtrl', ['$scope', '$rootScope', '$timeout', '$http', '$window', '$uibModal', '$state', '$stateParams', '$templateCache', 'Register', '$location', 
    function($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register, $location) {
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
                                alert(answer.url);
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
                                alert(answer.url);
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
                                alert(answer.url);
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
]);