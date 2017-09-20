
'use strict';
codenerix_addlib('cashdiaryControllers');
angular.module('cashdiaryControllers', [])
.controller('CashDiaryCtrl', ['$scope', '$rootScope', '$timeout', '$location', '$uibModal', '$templateCache', '$http', '$state', 'Register', 'ListMemory',
    function($scope, $rootScope, $timeout, $location, $uibModal, $templateCache, $http, $state, Register, ListMemory) {
        var listid = 0;
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        multilist($scope, $rootScope, $timeout, $location, $uibModal, $templateCache, $http, $state, Register, ListMemory, 0, "/"+ws_entry_point);
            
        $scope.explain = function(pk, action, kind) {
            // Base window
            $scope.ws=$scope.wsbase+"explain/"+pk+"/"+action+"/"+kind;
            
            // Base Window functions
            var functions = function(scope) {}
            var callback = function(scope) { $scope.refresh(); }
            
            // Prepare for refresh
            openmodal($scope, $timeout, $uibModal, 'lg', functions, callback);
            
        };
    }
]);
