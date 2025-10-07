




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = shell_exec('cat /tmp/tainted.txt');

$sanitized = filter_var($tainted, FILTER_SANITIZE_NUMBER_INT);
if (filter_var($sanitized, FILTER_VALIDATE_INT))
  $tainted = $sanitized ;
else
  $tainted = "" ;

//flaw
echo $tainted ;
?>
</script>
</head>
<body onload="xss()">
<h1>Hello World!</h1>
</body>
</html>