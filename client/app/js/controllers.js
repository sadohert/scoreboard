'use strict';

/* Controllers */

angular.module('myApp.controllers', []).
  controller('MyCtrl1', [function() {

  }])
  .controller('MyCtrl2', [function() {

  }])
  .controller('NewGame', [function() {


  }])
  .controller('GetGames', ['$scope', 'Games', function($scope, Games) {
	  $scope.games = Games.query();

  }]);