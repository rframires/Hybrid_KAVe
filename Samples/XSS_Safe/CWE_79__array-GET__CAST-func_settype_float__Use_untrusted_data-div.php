




<!DOCTYPE html>
<html>
<head/>
<body>
<div>
<?php
$array = array();
$array[] = 'safe' ;
$array[] = $_GET['userData'] ;
$array[] = 'safe' ;
$tainted = $array[1] ;

if(settype($tainted, "float"))
  $tainted = $tainted ;
else
  $tainted = 0.0 ;


echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>