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
  $targetIdx = $_REQUEST['targetindex'];
  $startTime = $_REQUEST['starttime'];
  $duration = $_REQUEST['duration'];
  $stLoc = $_REQUEST['startloc'];
  $endLoc = $_REQUEST['endloc'];
  $path = $_REQUEST['path'];
  $dist = $_REQUEST['distance'];
  $prox = $_REQUEST['proximity'];
  $misses = $_REQUEST['misses'];

  try {
    $dbh = getDatabaseHandle();
  } catch(PDOException $e) {
    echo $e->getMessage();
  }

if($dbh) {
    $sth = $dbh->prepare ("INSERT INTO tasks (worker, trial, session, frametime, speed, targetindex, starttime, duration, startloc, endloc, path, distance, proximity) VALUES (:worker, :trial, :session, :frameTime, :speed, :targetIdx, :startTime, :duration, :stLoc, :endLoc, :path, :dist, :prox, :misses)");
    $sth->execute(array(':worker'=>$worker, ':trial'=>$trial, ':session'=>$session, ':frameTime'=>$frameTime, ':speed'=>$speed, ':targetIdx'=>$targetIdx, ':startTime'=>$startTime, ':duration'=>$duration, ':stLoc'=>$stLoc, ':endLoc'=>$endLoc, ':path'=>$path, ':dist'=>$dist, ':prox'=>$prox, ':misses'=>$misses);
    $row = $sth->fetch(PDO::FETCH_ASSOC, PDO::FETCH_ORI_NEXT);
}

?>
