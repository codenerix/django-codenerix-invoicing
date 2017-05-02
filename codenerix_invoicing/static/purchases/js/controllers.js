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

// Angular codenerix invoicing purchases controllers
angular.module('codenerixSalesControllers', [])
.controller('codenerixPurchasesDetailsCtrl', ['$scope', '$rootScope', '$http', '$window', '$uibModal', '$state', '$stateParams', '$templateCache', 'Register', '$location', 
    function($scope, $rootScope, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register, $location) {
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        var url = ws_entry_point+"/"+$stateParams.pk;
        $scope.list_pk = [];
        
        $scope.create_order_from_budget = function(){
            /*
            Muestra el detalle del Acta
            */
            console.log(url);
            $scope.wsbase = "/"+url+"/doorder/"+$stateParams.pk;
            // Base window
            $scope.ws_entry_point=url;
            $scope.ws=$scope.wsbase;
            
            $scope.initialws = $scope.ws_entry_point;
            // Base Window functions
            var functions = function(scope) {
                scope.gotoback = function() {
                    $scope.base_window.dismiss('cancel');
                };
            };
            var callback = function(scope) {
            };
            // Prepare for refresh
            $scope.base_reload=[$scope.details_view, $stateParams.pk];
            $scope.base_window=openmodal($scope, $uibModal, 'lg', functions, callback);
        };
        $scope.create_order = function(type){

            $scope.ws="/"+url+"/createorder";
            var lines = [];
            $("input[name=checkline]:checked").each(function (){
                lines.push($(this).val());
            });
            var datas = {
                'lines': lines
            };
            
            $http.post( $scope.ws, datas, {})
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
        };

        // lineas selecionadas
        $scope.checkline_select = function(pk){
            var pos = $scope.list_pk.indexOf(pk);
            if ($scope['checkline_'+pk] == true){
                if (pos == -1){
                    $scope.list_pk.push(pk);
                }
            }else{
                $scope.list_pk.splice(pos, 1);
            }
            
            $scope.$parent.lines = $scope.list_pk.join();
        }

        $scope.change_quantity = function(pk){
            $scope['checkline_'+pk] = true;
            $scope.checkline_select(pk);
        }

        $scope.presubmit = function(form){
            var lines = [];
            $("input[name=checkline]:checked").each(function (){
                lines.push($(this).val());
            });
            $scope.submit(form);
        }
    }
]);