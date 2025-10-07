




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

$tainted = $tainted  == 'safe1' ? 'safe1' : 'safe2';

//flaw
echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>