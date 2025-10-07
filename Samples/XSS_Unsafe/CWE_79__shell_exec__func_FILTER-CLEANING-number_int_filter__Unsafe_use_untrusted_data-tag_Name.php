




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = shell_exec('cat /tmp/tainted.txt');

$sanitized = filter_var($tainted, FILTER_SANITIZE_NUMBER_INT);
if (filter_var($sanitized, FILTER_VALIDATE_INT))
  $tainted = $sanitized ;
else
  $tainted = "" ;

//flaw
echo "<".  $tainted ." href= \"/bob\" />" ;
?>
<h1>Hello World!</h1>
</body>
</html>