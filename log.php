<?php
error_reporting(E_ALL);
ini_set("display_errors", 1);

include('_db.php');

if(isset($_REQUEST['task']) && isset($_REQUEST['time']) && isset($_REQUEST['worker'])) {

  $task = $_REQUEST['task'];
  $time = $_REQUEST['time'];
  $worker = $_REQUEST['worker'];

  try {
    $dbh = getDatabaseHandle();
  } catch(PDOException $e) {
    echo $e->getMessage();
  }

if($dbh) {
    $sth = $dbh->prepare ("INSERT x INTO y");
    $sth->execute(array(':time'=>$time));
    $row = $sth->fetch(PDO::FETCH_ASSOC, PDO::FETCH_ORI_NEXT);
}

?>
