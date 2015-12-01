
function startTargets() {
    addTarget();
    console.log("Mouse location (X,Y): ", mouseX, mouseY);
};

var count = 0;
function addTarget() {
    //randomly create start and end positions
    var startLeft = $("#target-zone").width() * Math.random();
    var startTop = 0;
    
    var endLeft = $("#target-zone").width() * Math.random();
    var endTop = $("#target-zone").height();
    
    var distance = Math.sqrt((endLeft-startLeft)*(endLeft-startLeft) + (endTop-startTop)*(endTop-startTop));
    var speed = 100; //pixels per second
    var time = (distance/speed) * 1000;
    
    //create a new target over the area
    var targetid = "target"+count;
    var targethtml = "<div class='target' id='"+targetid+"'></div>";
 	$("#target-zone").append(targethtml);
    var newTarget = $("#"+targetid);
    newTarget.css({left:startLeft, top:startTop});
    
    newTarget.animate({
		top: endTop,
		left: endLeft,
    }, time, "linear", function() {
        $(this).remove();
        alert("done");
  	});
    
    count++;
};


var mouseX = -1;
var mouseY = -1;

$(document).ready( function(e) {
console.log("loaded", e);
  mouseX = e.pageX;
  mouseY = e.pageY;
  // Update mouse location on move
  $(document).bind('mousemove',function(e){ 
    //console.log("e.pageX: " + e.pageX + ", e.pageY: " + e.pageY); 
    mouseX = e.pageX;
    mouseY = e.pageY;
  });

  $(document).on('click', function() {
 	startTargets();
  });
});

