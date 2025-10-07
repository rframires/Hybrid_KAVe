




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = shell_exec('cat /tmp/tainted.txt');

$sanitized = filter_var($tainted, FILTER_SANITIZE_NUMBER_FLOAT);
if (filter_var($sanitized, FILTER_VALIDATE_FLOAT))
  $tainted = $sanitized ;
else
  $tainted = "" ;


echo "<div id='".  $tainted ."'>content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>