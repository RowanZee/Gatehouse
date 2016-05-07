$(document).ready(function () {

    //Temp User
    $('.tmpuser').change(function(){
        if($(this).is(":checked")) {
            $('.date-time').addClass("visible");
    		$('.date-time').removeClass("hidden");
    		var date = new Date();

            var day = date.getDate();
            var month = date.getMonth() + 1;
            var year = date.getFullYear();

            if (month < 10) month = "0" + month;
            if (day < 10) day = "0" + day;

            var today = year + "-" + month + "-" + day;       
            $("#tempDate").attr("value", today);

        } else {
            $('.date-time').addClass("hidden");
    		$('.date-time').removeClass("visible");
        }
    });
	function validate() {

		return false;
	}
	
	$('.monallday').change(function(){
		if($(this).is(":checked")) {
			var inputs = document.getElementsByClassName('montime');
			for(var i = 0; i < inputs.length; i++) {
				inputs[i].disabled = true;
			}
        } else {
			 var inputs = document.getElementsByClassName('montime');
			 for(var i = 0; i < inputs.length; i++) {
				inputs[i].disabled = false;
			}
        }
	});
	$('.tueallday').change(function(){
		if($(this).is(":checked")) {
			var inputs = document.getElementsByClassName('tuetime');
			for(var i = 0; i < inputs.length; i++) {
				inputs[i].disabled = true;
			}
        } else {
			var inputs = document.getElementsByClassName('tuetime');
			for(var i = 0; i < inputs.length; i++) {
				inputs[i].disabled = false;
			}
        }
	});
	$('.wedallday').change(function(){
		if($(this).is(":checked")) {
			var inputs = document.getElementsByClassName('wedtime');
			for(var i = 0; i < inputs.length; i++) {
				inputs[i].disabled = true;
			}
        } else {
			var inputs = document.getElementsByClassName('wedtime');
			for(var i = 0; i < inputs.length; i++) {
				inputs[i].disabled = false;
			}
        }
	});
	$('.thuallday').change(function(){
		if($(this).is(":checked")) {
 			var inputs = document.getElementsByClassName('thutime');
			for(var i = 0; i < inputs.length; i++) {
				inputs[i].disabled = true;
			}
        } else {
			var inputs = document.getElementsByClassName('thutime');
			for(var i = 0; i < inputs.length; i++) {
				inputs[i].disabled = false;
			}
        }
	});
	$('.friallday').change(function(){
		if($(this).is(":checked")) {
			var inputs = document.getElementsByClassName('fritime');
			for(var i = 0; i < inputs.length; i++) {
				inputs[i].disabled = true;
			}
        } else {
			var inputs = document.getElementsByClassName('fritime');
			for(var i = 0; i < inputs.length; i++) {
				inputs[i].disabled = false;
			}
        }
	});
	$('.satallday').change(function(){
		if($(this).is(":checked")) {
			var inputs = document.getElementsByClassName('sattime');
			for(var i = 0; i < inputs.length; i++) {
				inputs[i].disabled = true;
			}
        } else {
 			var inputs = document.getElementsByClassName('sattime');
			for(var i = 0; i < inputs.length; i++) {
				inputs[i].disabled = false;
			}
        }
	});
	$('.sunallday').change(function(){
		if($(this).is(":checked")) {
			var inputs = document.getElementsByClassName('suntime');
			for(var i = 0; i < inputs.length; i++) {
				inputs[i].disabled = true;
			}
        } else {
			var inputs = document.getElementsByClassName('suntime');
			for(var i = 0; i < inputs.length; i++) {
				inputs[i].disabled = false;
			}
        }
	});

    //Accordian
    $(function() { $( "#accordion" ).accordion({
    	active: false,
    	collapsible: true
    });});


    //Remove User
    $('.fa-trash-o').click(function() {
        var userID = $(this).data("id");
        var data = {
            'userID' : userID
        };
        var selector = $(this);

        $.ajax({
            type : "POST",
            url : "/removeuser/",
            data: JSON.stringify(data, null, '\t'),
            contentType: 'application/json;charset=UTF-8',
            success: function(result) {
                $('.accordian_' + userID).remove();
                $('.notification').remove();
                if (result == "success") {
                    notification('success','User Removed!');
                } else {
                    notification('success','Failed To Remove User.');
                }
            }
        });
    });

    //Check Password Length
    $( ".edit-user .password, .edit-user .username" ).on("input", function() {
        var selector = $(this).attr("class");
        var username;
        var password;
        var submitButton = $(this).parent('.edit-user').find('.button');
        if (selector.indexOf('password') != -1) {
            password = $(this);
            username = $(this).parent('.edit-user').find('.username');
        } else {
            username = $(this);
            password = $(this).parent('.edit-user').find('.password');
        }
        var updateValid = true;
        if (password.val().length > 5 || password.val().length === 0) {
            password.removeClass('error');
        } else {
            updateValid = false;
            if (password.is(":focus")) {
                password.addClass('error');
            }

        }
        if (username.val().length > 2 || username.val().length === 0) {
            username.removeClass('error');
        } else {
            updateValid = false;
            if (username.is(":focus")) {
                username.addClass('error');
            }
            submitButton.addClass('disabled');
        }

        if (updateValid === true) {
            submitButton.prop('disabled', false);
            submitButton.removeClass('disabled');
        } else {
            submitButton.prop('disabled', true);
            submitButton.addClass('disabled');
        }
    });
});

//Extra Functions
//Notification Function
function notification(type, message) {
    $( "nav" ).append( '<h2 class="notification ' + type + '">' + message + '</h2>' );
}
