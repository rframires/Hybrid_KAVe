




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = shell_exec('cat /tmp/tainted.txt');

$sanitized = filter_var($tainted, FILTER_SANITIZE_FULL_SPECIAL_CHARS);
  $tainted = $sanitized ;
     

//flaw
echo "<".  $tainted ." href= \"/bob\" />" ;
?>
<h1>Hello World!</h1>
</body>
</html>