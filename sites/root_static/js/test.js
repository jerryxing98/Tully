var settings = { 
			//nop     : 10, // The number of posts per scroll to be loaded
			pagenum : 2, // Initial offset, begins at 0 in this case
			error   : 'No More Posts!', // When the user reaches the end this is the message that is
			                            // displayed. You can change this if you want.
			delay   : 500, // When you scroll down the posts will load after a delayed amount of time.
			               // This is mainly for usability concerns. You can alter this as you see fit
			scroll  : false // The main bit, if set to false posts will not load as the user scrolls. 
			               // but will still load if the user clicks.
		}



function my_js_callback(data){
					// Change loading bar content (it may have been altered)
					// If there is no data returned, there are no more posts to be shown. Show error
					//alert($(data.message).find("div").html())
					
					try{
						$(data.message).find("div");
						settings.pagenum = settings.pagenum+1; 
						$('#content').append(data.message);
					}
					catch(err){
						$('#loading-bar').attr('disabled',"true");
						$('#loading-bar').html('加载完成');

					}
				
}


function comment_callback(data){
  $("div[@class=modal-body]/p").html(data.message);
  $("div[@class=modal hide fade]").modal.show();
  //$('#myModal').modal(options)
}

function login_get_callback(data){
	if (data.message)
	{
	 $('#modal-body').html(data.message);
	 $('#modal').modal("show");
	}	

}

function logout_callback(data){
	
	
	if(data.message){
	$('#nav-signin').empty();
	$('#nav-signin').html(data.message);
	}
}

function comment_get_callback(data){
	
	$('#modal-body').html(data.message);
	$('#modal').modal("show");

}


function comment_post_callback(data){
	switch(data.status){
	case 'Success':
		$('#modal-body').empty();
		$('#modal').modal("hide");
		$('#lk_'+data.message[0]).text('评论 '+data.message[1])
		break;
	case 'Fall':
		$('#modal-body').empty();
		$('#modal-body').html(data.message);
		break;
	case 'Error':
		$('#modal-body').empty();
		$('#modal-body').html(data.message);
		break;
	}
}


function favorite_callback(data){
	switch(data.status){
	case 'deleted':
		$('#fav_'+data.message[0]).prop('disabled', true);
		$('#fav_'+data.message[0]).children().removeClass('icon-star').addClass('icon-star-empty');
		$('#fav_'+data.message[0]).html('<i class="icon-star-empty"></i>收藏 '+data.message[1]);;
		$('#fav_'+data.message[0]).prop('disabled', false);
		break;
	case 'added':
		$('#fav_'+data.message[0]).prop('disabled', true);
		$('#fav_'+data.message[0]).children().removeClass('icon-star-empty').addClass('icon-star');		
		$('#fav_'+data.message[0]).html('<i class="icon-star"></i>收藏 '+data.message[1]);;
		$('#fav_'+data.message[0]).prop('disabled', false);
		break;
	case 'Error':
		$('#modal-body').empty();
		$('#modal-body').html(data.message);
		$('#modal').modal("show");
		break;
	}

	
}

function login_post_callback(data){
	switch(data.status){
	case 'Success':
		$('#modal-body').empty();
		$('#modal').modal("hide");
		$('#nav-signin').empty();
		$('#nav-signin').html(data.message);
		break;
	case 'Fail':
		break;
	case 'Error':
		$('#modal-body').empty();
		$('#modal-body').html(data.message);
		break;
	}
}

function screenshot_callback(data){
	switch(data.status){
	case 'Success':
		break;
	case 'Fail':
		break;
	case 'Error':
		break;
	}
}


function keep_screenshot(){
	alert($('#id_link').val());
	Dajaxice.bookmark.ajax_screenshot(screenshot_callback,{'url':$('#id_link').val()});
}

function keep_login_get(){
Dajaxice.account.ajax_login_get(login_get_callback,{'form':''});
}

function keep_login_post(){
Dajaxice.account.ajax_login_post(login_post_callback,{'form':$('#signin_form').serialize(true)});
}

function keep_logout(){
Dajaxice.account.ajax_logout(logout_callback);
}

function send_message(page){
			Dajaxice.bookmark.ajax_recommend(my_js_callback,{'page':page});
}


function keep_comment_get(pk){
	Dajaxice.bookmark.ajax_comment_get(comment_get_callback,{'form':'','pk':pk});	
}

function keep_comment_post(pk){
	Dajaxice.bookmark.ajax_comment_post(comment_post_callback,{'form':$('#comment_from').serialize(true),'pk':pk});
}

function keep_favorite(target_model,pk){
Dajaxice.favorite.add_or_remove(favorite_callback,{'target_model':target_model,'pk':pk});

}

function keep_shared(){


}

$("#loading-bar").click(function(){
	send_message(settings.pagenum);
})




