var app = angular.module('ahunaApp', ['ui.router']);

app.controller('MainCtrl', ['$scope', '$http', function($scope, $http) {

	$scope.test = [];

	$scope.addText = function(text) {
		$scope.test.push(text);
	};

}]);