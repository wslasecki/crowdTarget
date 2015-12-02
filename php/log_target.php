<?php
error_reporting(E_ALL);
ini_set("display_errors", 1);

include('_db.php');

if(isset($_REQUEST['time']) && isset($_REQUEST['worker'])) {

  $worker = $_REQUEST['worker'];  // worker ID
  $trial = $_REQUEST['trial'];  // trial (set of targets) ID
  $session = $_REQUEST['session'];  // session ID
  $frameTime = $_REQUEST['frametime'];  // duration of single still frame
  $speed = $_REQUEST['speed'];  // movement speed of the target
  $targetIdx = $_REQUEST['targetindex'];  // target ID (numeric index of the current target clicked)
  $startTime = $_REQUEST['starttime'];  // start time of the trial (set of targets) or of the previous target hit
  $duration = $_REQUEST['duration'];  // time taken to click target (since starttime)
  $stLoc = $_REQUEST['startloc'];  // location of mouse pointer [x,y] at start of task (target appears, or prior target hit)
  $endLoc = $_REQUEST['endloc'];  // location of the mouse pointer [x,y] at the end of the task (target hit)
  $path = $_REQUEST['path'];  // string containing the all of the locations the mouse was in between the start and the end of this task (JSON list)
  $dist = $_REQUEST['distance'];  // distance between starting mouse location and ending mouse location
  $prox = $_REQUEST['proximity'];  // how close to the center of the target the final (hit) click was
  $misses = $_REQUEST['misses'];  // number of non-target clicks in this task

  try {
    $dbh = getDatabaseHandle();
  } catch(PDOException $e) {
    echo $e->getMessage();
  }

if($dbh) {
    $sth = $dbh->prepare ("INSERT INTO targethits(worker, trial, session, frametime, speed, targetindex, starttime, duration, startloc, endloc, path, distance, proximity, misses) VALUES (:worker, :trial, :session, :frameTime, :speed, :targetIdx, :startTime, :duration, :stLoc, :endLoc, :path, :dist, :prox, :misses)");
    $sth->execute(array(':worker'=>$worker, ':trial'=>$trial, ':session'=>$session, ':frameTime'=>$frameTime, ':speed'=>$speed, ':targetIdx'=>$targetIdx, ':startTime'=>$startTime, ':duration'=>$duration, ':stLoc'=>$stLoc, ':endLoc'=>$endLoc, ':path'=>$path, ':dist'=>$dist, ':prox'=>$prox, ':misses'=>$misses);
    $row = $sth->fetch(PDO::FETCH_ASSOC, PDO::FETCH_ORI_NEXT);
}

?>
