'use strict';

/* Controllers */

angular.module('myApp.controllers', []).
  controller('MyCtrl1', [function() {

  }])
  .controller('MyCtrl2', [function() {

  }])
  .controller('NewGame', ['$scope', function($scope) {
	  $scope.colours = [{name:'red'},{name:'blue'}, {name:'black'}]
	  
	  $scope.start_times = ['17:00', '17:30', '18:00', '18:30']
	  
	  $scope.ages = [0, 1, 2, 3]
	  $scope.genders = [
	                    {name: 'unspecified', value: 0}, 
	                    {name: 'mixed', value: 1},
	                    {name: 'female', value: 2},
	                    {name: 'male', value: 3}
	                    ]
  }])
  .controller('GetGames', ['$scope', 'Games', function($scope, Games) {
	  $scope.games = Games.query();

  }]);