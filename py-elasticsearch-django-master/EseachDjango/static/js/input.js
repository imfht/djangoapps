var res = {
	errno: 1,
	results: ['今天', '昨天', '午时已到', '有基友开我裤链', 'Hi']
}

$(function() {
	$("#input").on({
		"input propertychange": function() {
			var val = $(this).val()
			console.log(val)
			var html = ''
			if(val !== "") {
				$("#ul").css("display", "block")

				// $.ajax({
				// 	type: 'get',
				// 	dataType: 'json',
				// 	cache: false,
				// 	url: '',
				// 	async: true,
				// 	success: function(data) {
				// 		if(data.errno === 1) {
				// 			console.log('成功')
				// 		} else if (data.errno === 2) {
				// 			console.log('不能有非法字符')
				// 		} else {
				// 			console.log('Another thing')
				// 		}
				// 	}
				// })

				if(res.errno === 1) {
					$.each(res.results, function(index, str) {
						html += "<li class='item'>" + str + "</li>"
					})
					$("#ul").html(html)
				}
			} else {
				$("#ul").css("display", "none")
				$("#ul").html("")
			}
		},
		focus: function() {
			if($(this).val() === "") {
				$("#ul").css("display", "none")
			}
		}
	})

	$(document).on({
		click: function(e) {
			var e = e || window.event
			var className = e.target.className
			if(className !== "input" && className !== "item") {
				$("#ul").css("display", "none")
			}
		},
		keyup: function(e) {
			var keyNum = window.event ? e.keyCode : e.which
			console.log(keyNum)
		}
	})

	$("#ul").on({
		click: function() {
			var text = $(this).text()
			$("#input").val(text)
		},
		mouseenter: function() {
			$(this).css('background-color', '#ccc')
		},
		mouseleave: function() {
			$(this).css('background-color', '#fff')
		}
	}, ".item")

	$("#select").hover(function() {
		$(this).css("overflow", "visible")
	}, function() {
		$(this).css("overflow", "hidden")
	})

	$("#select span").click(function() {
		if($(this).text() !== $(".sel-active").text()) {
			$(".sel-active").before($(this))
			$(".sel-active").removeClass("sel-active")
			$(this).addClass("sel-active")

			if($(this).text() === 'English') {
				$("#search").text('Search')
			} else {
				$("#search").text('搜索')
			}
		}
	})
})