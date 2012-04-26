(function () {
	var formdata = false; 
	var imageSource = null;
	var spinner = null;
	var first = true;

	function showUploadedItem(source) {
		// Show loading elements

		$("#picture_upload_placeholder").show();
		$("#picture_upload_crop_dialog").hide();
		spinner.spin();

		// Add new image element

		$("#picture_upload_display").empty();

		var img = $("<img/>", { "src": source });
		img.appendTo("#picture_upload_display");

		img.load(function() {
			var w = this.width;
			var h = this.height;

			var resizeRatio = 600.0 / w;
			var newh = resizeRatio * h;
			
			var minw = 600.0 * resizeRatio;
			var minh = newh * resizeRatio

			$("#picture_upload_placeholder").hide();
			spinner.stop();

			img.Jcrop({
				aspectRatio: 4.0/3.0,
				minSize: [minw, minh],
				setSelect: [0, 0, minw, minh],
				allowSelected: false,
				onChange: updateCoords,
				onSelect: updateCoords })
			   .css("width", 600)
			   .css("height", newh);

			$("#picture_upload_crop_dialog").show();
			$("#picture_upload_display").show();
		});
	}   

	function updateCoords(c) {
		$("#picture_crop_x").val(c.x);
		$("#picture_crop_y").val(c.y);
		$("#picture_crop_w").val(c.w);
		$("#picture_crop_h").val(c.h);
	}

	function showSpinner(target) {
		var opts = {
		  lines: 13, // The number of lines to draw
		  length: 7, // The length of each line
		  width: 2, // The line thickness
		  radius: 5, // The radius of the inner circle
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
		spinner = new Spinner(opts).spin(target);
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
	                $("#picture_upload_crop_dialog").hide();
			$("#picture_upload_placeholder").show();

			showSpinner("picture_upload_placeholder");

			$.ajax({
				url: "/submit/picture",
				type: "POST",
				data: formdata,
				processData: false,
				contentType: false,
				success: function (res) {
					$("#picture_upload_info").text(res["result"]); 
					// TODO gracefully handle erorrs
					if ("file" in res) {
						showUploadedItem(imageSource);
						$("#picture_file").val(res["file"]);
					}
				}
			});
		}
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
