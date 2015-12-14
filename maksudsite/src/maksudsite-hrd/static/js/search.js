$(document).ready(function(){

	// Caching the movieName textbox:
	var movieName = $('#movieName');

	// Defining a placeholder text:
	movieName.defaultText('Search ...');

	// Using jQuery UI's autocomplete widget:
	movieName.autocomplete({
		minLength	: 5,
		source		: 'http://demo.tutorialzine.com/2010/08/simple-movie-search-app-jquery-ajax/movieInfo.php'
	});

	$('#holder .button').click(function(){
		if(movieName.val().length && movieName.data('defaultText') != movieName.val()){
			$('#holder form').submit();
		}
	});
});

// A custom jQuery method for placeholder text:

$.fn.defaultText = function(value){

	var element = this.eq(0);
	element.data('defaultText',value);

	element.focus(function(){
		if(element.val() == value){
			element.val('').removeClass('defaultText');
		}
	}).blur(function(){
		if(element.val() == '' || element.val() == value){
			element.addClass('defaultText').val(value);
		}
	});

	return element.blur();
}