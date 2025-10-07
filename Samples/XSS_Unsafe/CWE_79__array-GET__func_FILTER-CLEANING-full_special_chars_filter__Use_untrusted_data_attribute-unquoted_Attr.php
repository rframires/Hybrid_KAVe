




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

$sanitized = filter_var($tainted, FILTER_SANITIZE_FULL_SPECIAL_CHARS);
  $tainted = $sanitized ;
     

//flaw
echo "<div id=". $tainted .">content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>