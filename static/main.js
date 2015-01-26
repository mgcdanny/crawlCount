(function () {

  'use strict';

  angular.module('WordcountApp', [])

  .controller('WordcountController', ['$scope', '$log', '$http', '$timeout', function($scope, $log, $http, $timeout) {
    $scope.getResults = function() {

      $scope.wordcounts = []

      // get the URL from the input
      var userInput = $scope.input_url

      // fire the request
      $http.post('/api/crawl', {"url": userInput}).
        success(function(results) {
          angular.forEach(results.freq, function(val,key){
            $scope.wordcounts.push({word:key, count:val})
          })
        }).
        error(function(error) {
          $log.log(error)
        });
    }
  }

  ]);

}());
