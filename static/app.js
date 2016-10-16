var app = angular.module('ahunaApp', ['ui.router']);

app.controller('MainCtrl', ['$scope', '$http', function($scope, $http) {

	
	$scope.sendText = function(text) {
		$http({
			method: 'POST',
			url: '/api/chat/receive',
			data: { 'text': text, 'user': 'test'}
		});

	};


}]);