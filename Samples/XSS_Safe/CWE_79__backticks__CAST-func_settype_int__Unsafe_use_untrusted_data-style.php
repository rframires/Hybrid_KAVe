




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = `cat /tmp/tainted.txt`;

if (settype($tainted, "integer"))
  $tainted = $tainted ;
else
  $tainted = 0 ;


echo $tainted ;
?>
</style>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>