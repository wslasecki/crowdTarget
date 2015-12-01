<?php
error_reporting(E_ALL);
ini_set("display_errors", 1);

include('_db.php');

if(isset($_REQUEST['task']) && isset($_REQUEST['time']) && isset($_REQUEST['worker'])) {

  $worker = $_REQUEST['worker'];
  $trial = $_REQUEST['trial'];
  $session = $_REQUEST['session'];
  $frameTime = $_REQUEST['frametime'];
  $speed = $_REQUEST['speed'];
  $startTime = $_REQUEST['starttime'];
  $duration = $_REQUEST['duration'];
  $avrgProx = $_REQUEST['proximity'];
  $ttlMisses = $_REQUEST['misses'];
  $numTargets = $_REQUEST['numtargets'];
  $targetsHit = $_REQUEST['targetshit'];
  $targetsMissed = $_REQUEST['targetsmissed'];

  try {
    $dbh = getDatabaseHandle();
  } catch(PDOException $e) {
    echo $e->getMessage();
  }

if($dbh) {
    $sth = $dbh->prepare ("INSERT INTO tasks (worker, trial, session, frametime, speed, starttime, duration, avrgproximity, misses, numnargets, targetshit, targetsmissed) VALUES (:worker, :trial, :session, :frameTime, :speed, :startTime, :duration, :avrgProx, :misses, :numTargets, :targetsHit, :targetsMissed)");
    $sth->execute(array(':worker'=>$worker, ':trial'=>$trial, ':session'=>$session, ':frameTime'=>$frameTime, ':speed'=>$speed, ':startTime'=>$startTime, ':duration'=>$duration, ':avrgProx'=>$avrgProx, ':misses'=>$misses, ':numTargets'=>$numTargets, ':targetsHit'=>$targetsHit, ':targetsMissed'=>$targetsMissed);
    $row = $sth->fetch(PDO::FETCH_ASSOC, PDO::FETCH_ORI_NEXT);
}

?>
