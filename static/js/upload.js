(function () {
	var formdata = false; 
	var imageSource = null;

	function showUploadedItem(source) {
  		var list = document.getElementById("image-list"),
	  		li = document.createElement("li"),
	  		img = document.createElement("img");
  		img.src = source;
  		li.appendChild(img);
		list.appendChild(li);
	}   

	if (window.FormData) {
  		formdata = new FormData();
//  		document.getElementById("btn").style.display = "none";
	}
	
        $("#picture_upload").change(function (evt) {
 		$("#picture_upload_info").text("Uploading . . .");
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
			$.ajax({
				url: "/submit/picture",
				type: "POST",
				data: formdata,
				processData: false,
				contentType: false,
				success: function (res) {
					console.log(res);
					$("#picture_upload_info").text(res); 
					showUploadedItem(imageSource);
				}
			});
		}
	});
}());
