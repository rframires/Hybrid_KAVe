




<!DOCTYPE html>
<html>
<head/>
<body>
<div>
<?php
$tainted = shell_exec('cat /tmp/tainted.txt');

$sanitized = filter_var($tainted, FILTER_SANITIZE_SPECIAL_CHARS);
  $tainted = $sanitized ;
      


echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>