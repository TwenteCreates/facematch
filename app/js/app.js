var app = angular.module("FaceMatch", ["ngRoute"]);

app.config(function($routeProvider) {
	$routeProvider
	.when("/", {
		templateUrl: "/app/views/index.html",
		title: "Home",
		controller: "indexCtrl"
	})
	.when("/red", {
		templateUrl: "/app/views/red.html",
		title: "Red"
	})
	.when("/green", {
		templateUrl: "/app/views/green.html",
		title: "Green"
	})
	.when("/blue", {
		templateUrl: "/app/views/blue.html",
		title: "Blue"
	});
});

// Change page title
// https://stackoverflow.com/a/13407227/1656944
app.run(["$rootScope", function($rootScope) {
	$rootScope.$on("$routeChangeSuccess", function (event, current, previous) {
		$rootScope.title = current.$$route.title;
	});
}]);

app.controller("indexCtrl", function($scope, $interval, $timeout, $http) {
	//
});