<?php
error_reporting(E_ALL);
ini_set("display_errors", 1);

include('_db.php');

if(isset($_REQUEST['task']) && isset($_REQUEST['time']) && isset($_REQUEST['worker'])) {

  $worker = $_REQUEST['worker'];
  $trial = $_REQUEST['trial'];
  $session = $_REQUEST['session'];
  $speed = $_REQUEST['speed'];
  $startTime = $_REQUEST['starttime'];
  $duration = $_REQUEST['duration'];
  $avrgProx = $_REQUEST['proximity'];
  $ttlMisses = $_REQUEST['misses'];
  $targetsMissed = $_REQUEST['targetsmissed'];

  try {
    $dbh = getDatabaseHandle();
  } catch(PDOException $e) {
    echo $e->getMessage();
  }

if($dbh) {
    $sth = $dbh->prepare ("INSERT INTO tasks (worker, trial, session, speed, starttime, duration, avrgproximity, misses, targetsmissed) VALUES ()");
    $sth->execute(array(':time'=>$time));
    $row = $sth->fetch(PDO::FETCH_ASSOC, PDO::FETCH_ORI_NEXT);
}

?>
