function chooseImageType(type) {
	//handles which image type the user selects, pano or 2d
	if (type == "panorama") {
		console.log("panorama");

		//confirm the user's choice
		$('#select-pano').removeClass("form-hidden");
		$('#select-pano').addClass("form-visible");

		$('#select-2d').removeClass("form-visible");
		$('#select-2d').addClass("form-hidden");

		//update the form's type to 3d (True, False is 2d)
		$('#image-type').val("True");

		$('#btn-next').removeClass("btn-disabled");
		$('#btn-next').addClass("btn-primary");


	}
	else if (type == "2d") {
		console.log("2d");
		//confirm user's choice by displaying appropriate feedback to user, same as above
		$('#select-2d').removeClass("form-hidden");
		$('#select-2d').addClass("form-visible");

		$('#select-pano').removeClass("form-visible");
		$('#select-pano').addClass("form-hidden");

		//update the form's type to 2d
		$('#image-type').val("False");

		$('#btn-next').removeClass("btn-disabled");
		$('#btn-next').addClass("btn-primary");

		//show user 'next stage option'
		//return triggerNextStage();
	}
	else {
		//pass
	}
}

function showStage(stage) {
	//used to switch between each section of the card-based form. works by toggling a 'stage'
	//on or off.
	console.log("showing stage: " + stage);

	switch (stage) {
		case 1:
		console.log("case 1 fired");
			//stage one: user selects which type of image they're uploading
			$('#form-stage-1').removeClass("form-hidden");				//show
			$('#form-stage-1').addClass("form-visible");

			$('#form-stage-2').removeClass("form-visible");			 //hide
			$('#form-stage-2').addClass("form-hidden");

			$('#form-stage-3').removeClass("form-visible");				//hide
			$('#form-stage-3').addClass("form-hidden");
			$('#form-stage-4').removeClass("form-visible");				//hide
			$('#form-stage-4').addClass("form-hidden");

			console.log("btn-next-stage is 2");

			//disable the previous button here, or change label to cancel
			$('#btn-previous').data('prev-stage', 0);
			$('#btn-next').data('next-stage', 2);

			$('#btn-next').removeClass("form-hidden");
			break;
		case 2:
			console.log("case 2 fired");
			//2: user selects an image, describes the image too
			//load second layout
			$('#form-stage-1').removeClass("form-visible");				//hide
			$('#form-stage-1').addClass("form-hidden");

			$('#form-stage-2').removeClass("form-hidden");			 //show
			$('#form-stage-2').addClass("form-visible");

			$('#form-stage-3').removeClass("form-visible");				//hide
			$('#form-stage-3').addClass("form-hidden");
			$('#form-stage-4').removeClass("form-visible");				//hide
			$('#form-stage-4').addClass("form-hidden");


			console.log("btn-next-stage is 3");
			$('#btn-previous').data('prev-stage', 1);
			$('#btn-next').data('next-stage', 3);

			if ($('#btn-submit').hasClass("form-visible")){
				$('#btn-submit').removeClass("form-visible");
				$('#btn-submit').addClass("form-hidden");
			}

			$('#btn-next').removeClass("form-hidden");
			break;
		case 3:
			//3: user drops a map pin to show where they took the photo
			$('#form-stage-1').removeClass("form-visible");				//hide
			$('#form-stage-1').addClass("form-hidden");
			$('#form-stage-2').removeClass("form-visible");			 //hide
			$('#form-stage-2').addClass("form-hidden");

			$('#form-stage-3').removeClass("form-hidden");				//show
			$('#form-stage-3').addClass("form-visible");


			console.log("btn-next-stage is 4");
			$('#btn-previous').data('prev-stage', 2);
			$('#btn-next').data('next-stage', 4);

			$('#btn-submit').removeClass("form-hidden");
			$('#btn-submit').addClass("form-visible");

			$('#btn-next').addClass("form-hidden");
			break;
		default:
			console.log("default has been triggered");
			break;
	}
}

function triggerPrevStage() {
	//grabs the next stage to show, regardless of previous or next
	var stage = $('#btn-previous').data('prev-stage');

	console.log("triggerPrevStage()");
	console.log("current stage read at:" + stage);

	return showStage(stage);
}


function triggerNextStage() {
	//grabs the next stage to show, regardless of previous or next
	var stage = $('#btn-next').data('next-stage');

	if ($('#btn-next').hasClass('btn-disabled')){
		//stay disabled
		console.log('next is disabled!');
	}
	else{
		console.log("triggerNextStage");
		console.log("current stage read at:" + stage);

		return showStage(stage);
	}
}
