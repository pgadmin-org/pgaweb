jQuery(document).ready(function($) {
	$('#pga-illustration').hover( function(){
		$(this).addClass('expand');
	}, function(){
		$(this).removeClass('expand');
	} );
});