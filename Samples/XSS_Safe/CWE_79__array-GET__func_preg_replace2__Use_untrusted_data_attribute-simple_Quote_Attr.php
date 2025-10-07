




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

$tainted = preg_replace('/\W/si','',$tainted);


echo "<div id='".  $tainted ."'>content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>