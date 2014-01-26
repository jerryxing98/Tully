/**
 * @author Chine
 */

function pageScrollTop(top) {
	$('html, body').animate({
		scrollTop: top + "px"
	}, {
		duration: 400,
		easing: "swing"
	});
}

function moveNext() {
	var beyondLast = true; // 表示下面没有可以移动到的对象
	$('article').each(function(i) {
		var top = $(this).offset().top;
		if(top > $('body').scrollTop()) {
			pageScrollTop(top);
			if(beyondLast) beyondLast = false;
			return false;
		}
	});
	if(beyondLast) {
		var $pagination = $("#Pagination");
		var pageTop = $('body').scrollTop();
		if($pagination.size() == 1) {
			var top = $pagination.offset().top;
			if(top > pageTop) {
				pageScrollTop(top);
			}
		} else {
			pageScrollTop($('body').height());
		}
	}
}

function movePrev() {
	var $articles = $('article');
	var $size = $articles.size();
	var beyondLast = true;
	$articles.each(function(i){
		var top = $(this).offset().top;
		var pageTop = $('body').scrollTop()
		if(top >= pageTop && i == 0 && pageTop > 0) {
			pageScrollTop(0);
			if(beyondLast) beyondLast = false;
			return false;
		} else if(top >= pageTop && i > 0) {
			pageScrollTop($($articles.get(i - 1)).offset().top);
			if(beyondLast) beyondLast = false;
			return false;
		}
	});
	if(beyondLast) {
		pageScrollTop($($articles.get($size - 1)).offset().top);
	}
}

function pageNext() {
	var $pages = $("div#Pagination a");
	if($pages.size() > 0) {
		var $next = $pages.last();
		var text = $next.text();
		if(isNaN(parseInt(text))) {
			window.location = $next.attr('href');
		}
	}
}

function pagePrev() {
	var $pages = $("div#Pagination a");
	if($pages.size() > 0) {
		var $first = $pages.first();
		var text = $first.text()
		if(isNaN(parseInt(text))) {
			window.location = $first.attr('href');
		}
	}
}

$(function() {
	$(window).keydown(function(event) {
		if(event.which === 74 && !event.ctrlKey) {
			// 按j键
			moveNext();
		}
		else if(event.which === 75 && !event.ctrlKey) {
			// 按k键
			movePrev();
		}
		else if(event.which === 39 && event.ctrlKey) {
			// 按ctrl + 右箭头
			pageNext();
		}
		else if(event.which === 37 && event.ctrlKey) {
			// 按ctrl + 左箭头
			pagePrev();
		}
	});
});