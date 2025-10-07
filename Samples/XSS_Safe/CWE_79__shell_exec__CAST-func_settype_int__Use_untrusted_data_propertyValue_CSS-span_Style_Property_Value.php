




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = shell_exec('cat /tmp/tainted.txt');

if (settype($tainted, "integer"))
  $tainted = $tainted ;
else
  $tainted = 0 ;


echo "<span style=\"color :". checked_data ."\">Hey</span>" ;
?>
<h1>Hello World!</h1>
</body>
</html>