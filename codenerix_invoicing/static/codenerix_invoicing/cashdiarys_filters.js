codenerix_addlib('cashdiaryFilters');
angular.module('cashdiaryFilters', [])

.filter('cashdiary', function() {
  return function(value, error_margin) {
        if (Math.abs(value) >= error_margin) {
            if (value>0) {
                var color = 'success';
            } else {
                var color = 'danger';
            }
            return '<b class="text-'+color+' small"> ('+parseFloat(value).toFixed(2)+' €)</b>';
        } else {
            return '';
        }
    }
})
.filter('cashdiarytxt', function() {
  return function(value, error_margin) {
        if (Math.abs(value) >= error_margin) {
            return parseFloat(value).toFixed(2)+' €';
        } else {
            return '';
        }
    }
});
