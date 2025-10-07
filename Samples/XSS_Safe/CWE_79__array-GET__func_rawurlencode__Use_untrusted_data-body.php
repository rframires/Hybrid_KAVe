




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$array = array();
$array[] = 'safe' ;
$array[] = $_GET['userData'] ;
$array[] = 'safe' ;
$tainted = $array[1] ;

$tainted = rawurlencode($tainted);


echo $tainted ;
?>
<h1>Hello World!</h1>
</body>
</html>
