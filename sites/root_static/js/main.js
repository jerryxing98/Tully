
/***
favorite function

***/


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


function check_authentication(parsed_json)
    {
    if (parsed_json.not_authenticated)
        {
        return false;
        }
    else
        {
        return true;
        }
    }
function offer_login()
    {
    $("#signin_modal").modal('show')
    }
function send_notification(level,message)
    {
	
    $(".").html("<h4>" + level + "</h4>"+message);
    $(".alert").alert();
	setTimeout("$('.alert').show('slow').delay(5000).hide('slow');", 0);
    
	}
function submit_search()
    {
    $.ajax(
        {
        data:
            {
            query: document.search_form.query.value
            },
        datatype: 'json',
        success: function(data, textStatus, XMLHttpRequest)
            {
            if (data)
                {
                if (check_authentication(data))
                    {
                    $("#results").html("");
                    var results = data[0];
                    var length = data[1];
                    for (var index = 0; index < results.length; ++index)
                        {
                        var result = results[index];
                        $("#results").append("<p><a href='/entities/" +
                          result["id"] + "'>" + result["name"] +
                          "</a><br />" + result["description"] + "</p>");
                        }
                    }
                else
                    {
                    offer_login();
                    }
                }
            },
        type: 'POST',
        url: '/ajax/search',
        });
    }


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(function()
    {
	var csrftoken = getCookie('csrftoken');
	$.ajaxSetup({
			beforeSend:function(xhr, settings) {
				if (!csrfSafeMethod(settings.type)) {
				 xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			},
			error: function(XMLHttpRequest, textStatus, errorThrown){
				send_notification(textStatus + "</p><p>" +
				errorThrown);
			},
        });
    $("#submit").click(function(event)
        {
        submit_search();
        return false;
        });
    $("#query").width($(window).width() - 240);
	
	/**
    $("#login_form").dialog({
        autoOpen: false,
        height: 150,
        width: 350,
        modal: true,
        buttons:
            {
            'Log in': function()
                {
                $.ajax({
                    data:
                        {
                        "login": document.getElementById("login").value,
                        "password": document.getElementById("password").value,
                        },
                    datatype: 'text',
                    success: function(data, textStatus, XMLHttpRequest)
                        {
                        if (data)
                            {
                            send_notification("You have successfully logged in.");
                            $(this).dialog('close');
                            submit_search();
                            }
                        else
                            {
                            send_notification("Your login was not successful.");
                            }
                        },
                    type: 'POST',
                    url: '/ajax/login',
                    });
                },
            'Forgot password': function()
                {
                send_notification("This feature has not been implemented.");
                },
            'Create account': function()
                {
                send_notification("This feature has not been implemented.");
                },
            },
        });
	**/
	
	
	$("#signin_link").click(function(event){
		offer_login();
	});

	$('.btn.favorite').click(function() {
		var $obj = $(this);
		var target_id = $obj.attr('id').split('_')[1];
		$obj.prop('disabled', true);
		$.ajax({
		url: $obj.attr('href'),
		type: 'POST',
		data: {target_model: $obj.attr('model'),
	       target_object_id: target_id},
		success: function(response) {
			if (response.status == 'added') {
			$obj.children().removeClass('icon-star-empty').addClass('icon-star');}
			else {
			$obj.children().removeClass('icon-star').addClass('icon-star-empty');}
			$obj.parent('.favorite').children('.fav-count').text(response.fav_count);
			$obj.prop('disabled', false);
			}
		});
	});

	$("#signin_modal_link").click(function(event){
	var $obj = $(this);
	$.ajax({
		url: $obj.attr('href'),
		type: 'POST',
		data:{"identification": document.getElementById("id_identification").value,
                  "password": document.getElementById("id_password").value,
                  "remember_me":document.getElementById("id_remember_me").value,
						},
            datatype:'text',
        success: function(response){
		alert('data==============='+response);
        },

                    });
	});
	
    });



/**

**/