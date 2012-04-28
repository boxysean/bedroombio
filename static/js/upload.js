(function () {
	var formdata = false; 
	var imageSource = null;
	var spinner = null;
	var first = true;
	var jcropApi = null;
	var cropped = false;

	function showUploadedItem(source) {
		// Show loading elements

		$("#picture_upload_placeholder").show();
		spinner.spin();

		// Add new image element

		$("#picture_upload_display").empty();

		var img = $("<img/>", { "src": source, "id": "picture_upload_img" });
		img.appendTo("#picture_upload_display");

		img.load(function() {
			var w = this.width;
			var h = this.height;

			var resizeRatio = 300.0 / w;
			var newh = resizeRatio * h;
			
			var minw = 300.0 * resizeRatio;
			var minh = newh * resizeRatio;

			$("#picture_upload_placeholder").hide();
			spinner.stop();

			img.css("width", 300)
			   .css("height", newh);

			jcropApi = $.Jcrop("#picture_upload_img");
			jcropApi.setOptions({
				aspectRatio: 3.0/2.0,
				minSize: [minw, minh],
				setSelect: [0, 0, minw, minh],
				allowSelected: false,
				onChange: updateCoords,
				onSelect: updateCoords });

			$("#picture_upload_display").show();
		});
	}   

	function updateCoords(c) {
		$("#picture_crop_x").val(c.x);
		$("#picture_crop_y").val(c.y);
		$("#picture_crop_x2").val(c.x2);
		$("#picture_crop_y2").val(c.y2);
	}

	function showSpinner(target) {
		var opts = {
		  lines: 15, // The number of lines to draw
		  length: 9, // The length of each line
		  width: 3, // The line thickness
		  radius: 7, // The radius of the inner circle
		  rotate: 0, // The rotation offset
		  color: '#FFF', // #rgb or #rrggbb
		  speed: 1, // Rounds per second
		  trail: 60, // Afterglow percentage
		  shadow: false, // Whether to render a shadow
		  hwaccel: false, // Whether to use hardware acceleration
		  className: 'spinner', // The CSS class to assign to the spinner
		  zIndex: 2e9, // The z-index (defaults to 2000000000)
		  top: 'auto', // Top position relative to parent in px
		  left: 'auto' // Left position relative to parent in px
		};
		var target = document.getElementById(target);
		return new Spinner(opts).spin(target);
	}

	if (window.FormData) {
  		formdata = new FormData();
	}
	
        $("#picture_upload").change(function (evt) {
 		var i = 0, len = this.files.length, img, reader, file;
	
		for ( ; i < len; i++ ) {
			file = this.files[i];
	
			if (!!file.type.match(/image.*/)) {
				if ( window.FileReader ) {
					reader = new FileReader();
					reader.onloadend = function (e) { 
						imageSource = e.target.result;
//						showUploadedItem(e.target.result, file.fileName);
					};
					reader.readAsDataURL(file);
				}
				if (formdata) {
					formdata.append("picture", file);
				}
			}	
		}
	
		if (formdata) {
			$("#picture_upload_display").hide();
			$("#picture_upload_placeholder").show();
			$("#picture_upload_error").hide();

			spinner = showSpinner("picture_upload_placeholder");

			$.ajax({
				url: "/submit/picture",
				type: "POST",
				data: formdata,
				processData: false,
				contentType: false,
				success: function (res) {
					if (res["result"] == "fail") {
						$("#picture_upload_error").text(res["error"]).show();
						spinner.stop();
					} else if (res["result"] == "success") {
						showUploadedItem(imageSource);
						$("#picture_file").val(res["file"]);
					}
				}
			});
		}
	});

	$("#picture_crop_button").click(function() {
		if (cropped) {
			jcropApi.enable();
		} else {
			jcropApi.disable();
		}
		cropped = !cropped;
	});
}());

(function() {
	updateCountdown();
	$('#description').change(updateCountdown);
	$('#description').keyup(updateCountdown);

	function updateCountdown() {
		var text = $("#description").val();
		var remaining = 250 - text.length;
		if (remaining < 0) {
			$("#description").val(text.substring(0, 250));
			remaining = 0;
		}
		$('#description_remaining').text(remaining + ' characters remaining');
	}
}());
