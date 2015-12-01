<?php
function getDatabaseHandle() {
  $dbh = new PDO("mysql:host=localhost;dbname=targets", "root", "borkborkbork");
  return $dbh;
}
?>
