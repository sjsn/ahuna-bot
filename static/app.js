var app = angular.module('ahunaApp', ['ui.router']);

app.controller('MainCtrl', ['$scope', '$http', function($scope, $http) {

	$scope.conversation = []
	$scope.newIn = false;
	$scope.newOut = false;

	$scope.handleInput = function(text) {
		$scope.newIn = true;
		$scope.conversation.push({text: text, author: 'user'});
		// Uses a GET request for now. Fix later for security.
		$http({
			method: 'GET',
			url: '/api/chat/receive?text=' + text,
		}).then(function(res) {
			console.log(res.data);
			if (res.data.text != null) {
				$scope.conversation.push({text: res.data.text, author: 'bot'});
			} else {
				$scope.conversation.push({text: "I wasn't able to process that. Please try again.", author: 'bot'})
			}
		});
	};

}]);