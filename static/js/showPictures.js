(function() {
	var presentId = -1;
	var maxId = -1;

	init();

	function init() {
		$.ajax({
			url: "/getMaxId",
			type: "POST",
			processData: false,
			contentType: false,
			success: function (res) {
				maxId = parseInt(res["maxId"]);
			}
		});
	}

	function prev() {
		presentId = Math.max(1, presentId-1);
	}

	function next() {
		presentId = Math.min(maxId, presentId+1);
	}

	function get(id) {
		$.ajax({
			url: "/get/" + id,
			type: "POST",
			processData: false,
			contentType: false,
			success: function (res) {
				$("#pop_image").attr("src", res["image"]).load(function() {
					$("#pop_zip").text(res["zipcode"])
					$("#pop_desc").text(res["description"]);
				});
			}
		});
	}

	$("[id^='poplink']").click(function() {
		var id = parseInt(this.id.substring(7)); // "poplink" = 7
		presentId = id;
		get(id);
	});

	$("#pop_prev").click(function() {
		prev();
		get(presentId);
	});

	$("#pop_next").click(function() {
		next();
		get(presentId);
	});

	$(document).keydown(function (e) {
		var keyCode = e.keyCode || e.which,
			  arrow = {left: 37, up: 38, right: 39, down: 40 };
	
		switch (keyCode) {
		case arrow.left:
			prev();
			get(presentId);
			break;
		case arrow.right:
			next();
			get(presentId);
			break;
		}
	});

}());
