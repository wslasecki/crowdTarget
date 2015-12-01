var speed = 100; //pixels per second
var numTargets = 3;

var timeBetweenRounds = 500;

$(function() {
 	startTargets();
});

function startTargets() {
	for(var i=0; i<numTargets; i++) {
		addTarget();
	}
};

var count = 0;
function addTarget() {
    //randomly create start and end positions
    var startLeft = $("#target-zone").width() * Math.random();
    var startTop = 0;
    
    var endLeft = $("#target-zone").width() * Math.random();
    var endTop = $("#target-zone").height();
    
    var distance = Math.sqrt((endLeft-startLeft)*(endLeft-startLeft) + (endTop-startTop)*(endTop-startTop));
    
    var time = (distance/speed) * 1000;
    
    //create a new target over the area
    var targetid = "target"+count;
    var targethtml = "<div class='target' id='"+targetid+"'></div>";
 	$("#target-zone").append(targethtml);
    var newTarget = $("#"+targetid);
    newTarget.css({left:startLeft, top:startTop});
    
	//animate the target
    newTarget.animate({
		top: endTop,
		left: endLeft,
    }, time, "linear", function() {
		//on end animation
        $(this).remove();
		
		//start next round if no targets remain
		if ($(".target").length == 0) {
			setTimeout(startTargets, timeBetweenRounds);
		}
  	});
	
	newTarget.click(function() {
		newTarget.hide();
	})
    
    count++;
};