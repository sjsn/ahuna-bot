var app = angular.module('ahunaApp', ['ui.router']);

app.controller('MainCtrl', ['$scope', '$http', function($scope, $http) {

	// Temporary client-side version of conversation
	$scope.conversation = []
	$scope.newOut = false;

	var convo = document.getElementById('convo');

	$scope.handleInput = function(text) {
		$scope.text = "";
		$scope.conversation.push({text: text, author: 'user'});
		$scope.newOut = true;
		// Uses a GET request for now. Fix later for security.
		$http({
			method: 'GET',
			url: '/api/chat/receive?text=' + text,
		}).then(function(res) {
			if (res.data.text != null) {
				$scope.conversation.push({text: res.data.text, author: 'bot'});
			} else {
				$scope.conversation.push({text: "I wasn't able to process that. Please try again.", author: 'bot'})
			}
			$scope.newOut = false;
			convo.scrollTop = convo.scrollHeight;
		});
		convo.scrollTop = convo.scrollHeight;
	};

}]);

app.controller('LoginCtrl', ['$scope', function($scope) {

	$scope.login = function(username, pass)	{
		if (username == 'test' && pass == 'test') {
			console.log("login");
		}
	};
	
}]);