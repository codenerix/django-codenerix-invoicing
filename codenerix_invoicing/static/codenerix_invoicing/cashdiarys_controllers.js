
'use strict';

// Angular codenerix invoicing sales controllers
angular.module('codenerixServicesControllers', [])
.controller('codenerixServicesDetailsCtrl', ['$scope', '$rootScope', '$timeout', '$http', '$window', '$uibModal', '$state', '$stateParams', '$templateCache', 'Register', '$location', 
    function($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register, $location) {
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        if ($stateParams.pk == undefined){
            var url = ws_entry_point;
        }else{
            var url = ws_entry_point+"/"+$stateParams.pk;
        }

        $scope.pay = function(){

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

        $scope.print_ticket = function(){
            var path = "/" + url + "/ticket";
            $http.post( path, {}, {} )
                .success(function(answer, stat) {
                    if (answer.error != null){
                        console.log(answer.error);
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

        $scope.view_doc = function(){

            var functions = function(scope) {
            };
            var callback = function(scope) {
            };
            var callback_cancel = function($scope){
            };
            if ($scope.ws_base == undefined){
                $scope.ws_base = $scope.ws;
            }
            console.log(url);
            if (url == undefined){
                $scope.ws = "/view_doc";
            }else{
                $scope.ws = "/" + url + "/view_doc";
            }
            openmodal($scope, $timeout, $uibModal, 'lg', functions, callback, undefined, callback_cancel);
        };

        $scope.change_amount = function(field_amount, field_total, field_result){
            var amount = $scope[$scope.form_name][field_amount].$viewValue;
            var total = $scope[$scope.form_name][field_total].$viewValue;
            var diff = total - amount;
            $scope[$scope.form_name][field_result].$setViewValue(diff.toFixed(2));
            $scope[$scope.form_name][field_result].$render();
        };

        $scope.disabled_field_person = function(){
            return $scope[$scope.form_name]['person_responsable'].$viewValue;
        };

        $scope.open_cash_register = function(){
            var ruta = '/services/open_cash_register/';
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
