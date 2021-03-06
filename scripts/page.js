//pixels per second
var speeds = [50,100,150,200,250,300];
var numTargets = [1,2,3,4,5,6];
var stillFrameDuration = parseInt(gup("frameDuration", 0));
var animationFunction=stillFrameAnimation;
if (stillFrameDuration == 0) {
	animationFunction=videoAnimation;
}
var backSpeedRandom = Math.random();

//initialize logging vars
var workerId = gup("workerId");
var assignmentId = gup("assignmentId");
var startTime = -1;
var avrgproximity = 0;
var misclicks = 0;
var targetssurvived = 0;
var targetshit = 0;
var mousePath = [];
var timeLastHit = startTime;
var misclicksLastHit = 0;

//create combination of every test variable
combos = [];
for(var i = 0; i < speeds.length; i++){
	for(var j = 0; j < numTargets.length; j++){
		combos.push({speed:speeds[i],numTargets:numTargets[j]});
	}
}
//shuffle combos
for(var i = combos.length - 1; i > 0; i--) {
	var j = Math.floor(Math.random() * (i + 1));
	var temp = combos[i];
	combos[i] = combos[j];
	combos[j] = temp;
}

var timeBetweenRounds = 500;

currentRound = 0;
currentSpeed = 0;
currentNumTargets = 0;
function startTargets() {
	if (currentRound < combos.length) {
		var roundParams = combos[currentRound];
		currentRound++;
		currentSpeed = roundParams.speed;
		currentNumTargets = roundParams.numTargets;

		//re-randomize how far back targets are spawned in still frame interface
		backSpeedRandom = Math.random();

		//clear logging variables
		startTime = (new Date).getTime();
		avrgproximity = 0;
		misclicks = 0;
		targetssurvived = 0;
		targetshit = 0;
		mousePath = [[mouseX,mouseY,startTime]];
		timeLastHit = startTime;
		misclicksLastHit = 0;

		console.log("Starting targets w/ mouse position (x,y): ", mouseX, mouseY);

		for(var i=0; i<roundParams.numTargets; i++) {
			addTarget(roundParams.speed);
		}
	} else {
		finished();
	}
}

function finished() {
	$('#description').hide();
	$('#buttondesc').html("Press submit to finish the task.");
	$('#buttondesc').show();

	alert("Thanks For Playing");
	$("#submitbutton").show();
}

var count = 0;
function addTarget(speed) {
    //randomly create start and end positions
	var travelDistance = $("#target-zone").height();
	var targetW2 = 25; var targetH2 = 25;
	var zonePos = $("#target-zone").position();
	var targetOffsetLeft = zonePos.left - targetW2;
	var targetOffsetTop = zonePos.top - targetH2;

    var startLeft = ($("#target-zone").width() * Math.random()) + targetOffsetLeft;
    var startTop = targetOffsetTop;

    var endLeft = ($("#target-zone").width() * Math.random()) + targetOffsetLeft;
    var endTop = $("#target-zone").height() + targetOffsetTop;

	var deltaLeft = endLeft - startLeft;
	var deltaTop = endTop - startTop;
	var deltaDist = Math.sqrt(deltaLeft*deltaLeft + deltaTop*deltaTop);
	endLeft = startLeft + ((deltaLeft/deltaDist) * travelDistance);
	endTop = startTop + ((deltaTop/deltaDist) * travelDistance);

    var time = (travelDistance/speed) * 1000;

    //create a new target over the area
    var targetid = "target"+count;
    var targethtml = "<div class='target' id='"+targetid+"'></div>";
 	$("#target-zone").append(targethtml);
    var newTarget = $("#"+targetid);
    newTarget.css({left:startLeft, top:startTop});

	//animate the target
	animationFunction(newTarget, startLeft, startTop, endLeft, endTop, time);

	//handle the click on the target
	newTarget.mousedown(function(mevent) {
		//calculate log variables
		targetshit++;

		var deltaX = mevent.offsetX - (newTarget.width()/2);
		var deltaY = mevent.offsetY - (newTarget.height()/2);

		var proximity = Math.sqrt(deltaX*deltaX + deltaY*deltaY);
		avrgproximity += proximity;

		var timeNow = (new Date).getTime();
		var duration = timeNow - timeLastHit;
		var startPos = JSON.stringify([startLeft,startTop]);
		var endPos = JSON.stringify([parseFloat(newTarget.css("left")),parseFloat(newTarget.css("top"))]);

		mousePath.push([mouseX,mouseY,timeNow]);
		var mousePathString = JSON.stringify(mousePath);

		deltaX = mousePath[0][0] - mouseX;
		deltaY = mousePath[0][1] - mouseY;
		var mouseDistance = Math.sqrt(deltaX*deltaX + deltaY*deltaY);

		//log the target clicked
		logTarget(workerId, currentRound, assignmentId, stillFrameDuration, currentSpeed, targetshit, timeLastHit, duration, startPos, endPos, mousePathString, mouseDistance, proximity, misclicksLastHit);
		mousePath = [];
		timeLastHit = timeNow;
		misclicksLastHit = 0;

		//remove the target
		newTarget.stop();
		newTarget.remove();
		tryNextRound();
	});

    count++;
}

function videoAnimation(newTarget, startLeft, startTop, endLeft, endTop, time) {
	newTarget.animate({
		left: endLeft,
		top: endTop,
    }, time, "linear", function() {
		//on end animation
		targetssurvived++;

        $(this).remove();
		tryNextRound();
  	});
}

function stillFrameAnimation(newTarget, startLeft, startTop, endLeft, endTop, time) {
	var numFrames = time / stillFrameDuration;
	var deltaLeft = endLeft - startLeft;
	var deltaTop = endTop - startTop;
	var leftInc = deltaLeft / numFrames;
	var topInc = deltaTop / numFrames;
	var distance = Math.sqrt(deltaLeft*deltaLeft + deltaTop*deltaTop);

	//move target backwards slightly so that it appears in the middle of zone
	var backSpeed = 1 - ((numFrames % 1) * backSpeedRandom);
	var newLeft = startLeft - (leftInc * backSpeed);
	var newTop = startTop - (topInc * backSpeed);
	newTarget.css({
		left: newLeft,
		top: newTop,
		display:"none"
	});

	//create a function that will animate this specific target
	var moveTarget = function() {
		//check if target still exists
		if($("#"+newTarget.attr("id")).length == 0) {
			//just quit the animation loop for this target if its been clicked on
			return;
		}

		// Begin the countdown bar animation
		startCountdown();

		//calculate and set the new position of the targets
		var newLeft = parseFloat(newTarget.css("left")) + leftInc;
		var newTop = parseFloat(newTarget.css("top")) + topInc;
		newTarget.css({
			left: newLeft,
			top: newTop,
			display:"block"
		});

		//remove if the targets have gone past its end point
		var newDeltaLeft = newLeft - startLeft;
		var newDeltaTop = newTop - startTop;
		var newDistance = Math.sqrt(newDeltaLeft*newDeltaLeft + newDeltaTop*newDeltaTop);

		if (newDistance >= distance) {
			targetssurvived++;

			newTarget.remove();
			tryNextRound();
		}else {
			setTimeout(moveTarget, stillFrameDuration);
		}
	};

	//start the animation
	var initialWaitDuration = 0;
	setTimeout(moveTarget, initialWaitDuration);
}

var nextRoundTimer = -1;
function tryNextRound() {
	//start next round if no targets remain
	if ($(".target").length == 0) {
		//stop the countdown timer
		$("#countdown-bar").stop();
		$("#countdown-bar").css({width:"0%"});

		//send the rounds logs
		var duration = (new Date).getTime() - startTime;
		if (targetshit > 0) {
			avrgproximity /= targetshit;
		}
		logTrial(workerId, currentRound, assignmentId, stillFrameDuration, currentSpeed, startTime, duration, avrgproximity, misclicks, currentNumTargets, targetshit, targetssurvived);

		//begin next round in a few milliseconds
		clearTimeout(nextRoundTimer);
		nextRoundTimer = setTimeout(startTargets, timeBetweenRounds);
	}
}

// Start the countdown bar animation
function startCountdown() {
	//we only want it to animate once per still frame
	//but this function gets called N times per still frame
	//if the bar is nearly full, then animation was likely started a few milliseconds ago.
	//instead only start the animation if it is less than half way
	var barWPercent = $("#countdown-bar").width() / $("#countdown-bar").parent().width() * 100;
	if( barWPercent < 50 ) {
		countdownRunning = true;
		$("#countdown-bar").stop();
		$("#countdown-bar").css({width:"100%"});
		$("#countdown-bar").animate({width:"0%"},stillFrameDuration, "linear");
	}
}

var mouseX = -1;
var mouseY = -1;

$(document).ready( function(e) {
  mouseX = e.pageX;
  mouseY = e.pageY;
  // Update mouse location on move
  $(document).bind('mousemove',function(e){
    //console.log("e.pageX: " + e.pageX + ", e.pageY: " + e.pageY);
    mouseX = e.pageX;
    mouseY = e.pageY;
	//log mouse location
	mousePath.push([mouseX,mouseY,(new Date).getTime()]);
  });

  $('#start').on('click', function() {
    startTargets();
    $('#start').hide();
	$('#buttondesc').hide();
  });

  	//handle misclicks
	$("#target-zone").click(function(e) {
		if (e.target.id == "target-zone") {
			misclicks++;
			misclicksLastHit++;
			$("#target-zone").animate({"backgroundColor":"#000"},50,"linear",function(){
				$("#target-zone").animate({"backgroundColor":"#FFF"},50,"linear");
			});
        }
	});
});
