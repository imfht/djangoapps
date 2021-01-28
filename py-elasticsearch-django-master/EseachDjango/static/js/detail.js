$(function() {
	// console.log($(".item-summary").text().length)
	$(".show-summary").click(function() {
		if ($(this).text() === "展开全部") {
			$(this).text("收起展开")
			$(".item-summary").css("height", "auto")
		} else {
			$(this).text("展开全部")
			$(".item-summary").css("height", "240px")
		}
	})
})