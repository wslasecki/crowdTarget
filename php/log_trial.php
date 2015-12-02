<?php
error_reporting(E_ALL);
ini_set("display_errors", 1);

include('_db.php');

if(isset($_REQUEST['worker'])) {

  $worker = $_REQUEST['worker'];  // worker ID
  $trial = $_REQUEST['trial'];  // trial (set of targets) ID
  $session = $_REQUEST['session'];  // session ID
  $frameTime = $_REQUEST['frametime'];  // duration of single still frame
  $speed = $_REQUEST['speed'];  // movement speed of the target
  $startTime = $_REQUEST['starttime'];  // start time of the trial (set of targets) or of the previous target hit
  $duration = $_REQUEST['duration'];  // time taken to click target (since starttime)
  $avrgProx = $_REQUEST['avrgproximity'];  // how close to the center of the target the final (hit) click was
  $ttlMisses = $_REQUEST['misses'];  // number of non-target clicks in this task
  $numTargets = $_REQUEST['numtargets'];  // total number of targets in this trial
  $targetsHit = $_REQUEST['targetshit'];  // number of targets hit (clicked)
  $targetsMissed = $_REQUEST['targetsmissed'];  // number of targets missed (left screen without being clicked)

  try {
    $dbh = getDatabaseHandle();
  } catch(PDOException $e) {
    echo $e->getMessage();
  }

  if($dbh) {
    $sth = $dbh->prepare ("INSERT INTO trials (worker, trial, session, frametime, speed, starttime, duration, avrgproximity, misses, numnargets, targetshit, targetsmissed) VALUES (:worker, :trial, :session, :frameTime, :speed, :startTime, :duration, :avrgProx, :ttlMisses, :numTargets, :targetsHit, :targetsMissed)");
    $sth->execute(array(':worker'=>$worker, ':trial'=>$trial, ':session'=>$session, ':frameTime'=>$frameTime, ':speed'=>$speed, ':startTime'=>$startTime, ':duration'=>$duration, ':avrgProx'=>$avrgProx, ':ttlMisses'=>$ttlMisses, ':numTargets'=>$numTargets, ':targetsHit'=>$targetsHit, ':targetsMissed'=>$targetsMissed));
    $row = $sth->fetch(PDO::FETCH_ASSOC, PDO::FETCH_ORI_NEXT);
  }

}

?>
