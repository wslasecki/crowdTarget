//pixels per second
var speeds = [50,100,150,200,250,300];
var numTargets = [1,2,3,4,5,6];

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
function startTargets() {
	var roundParams = combos[currentRound];
	currentRound++;
	
  console.log("Starting targets w/ mouse position (x,y): ", mouseX, mouseY);

  for(var i=0; i<roundParams.numTargets; i++) {
    addTarget(roundParams.speed);
  }
};

var count = 0;
function addTarget(speed) {
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
		tryNextRound();
  	});
	
	newTarget.click(function() {
		newTarget.remove();
		tryNextRound();
	})
    
    count++;
};

var nextRoundTimer = -1;
function tryNextRound() {
	//start next round if no targets remain
	if ($(".target").length == 0) {
		clearTimeout(nextRoundTimer);
		nextRoundTimer = setTimeout(startTargets, timeBetweenRounds);
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
  });

  $('#start').on('click', function() {
    startTargets();
    $('#start').hide();
  });

  	//handle misclicks
	$("#target-zone").click(function(e) {
		if (e.target.id == "target-zone") { 
			$("#target-zone").animate({"backgroundColor":"#000"},50,"linear",function(){
				$("#target-zone").animate({"backgroundColor":"#FFF"},50,"linear");
			});
        }
	});
});

