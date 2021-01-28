$(function() {
	if ($(".page-active").text() === '1') {
		$(".page-pro").css("display", "none")
	} else if ($(".active").text() === $(".page-divide a").length) {
		$(".page-next").css("display", "none")
	}
})