




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = system('ls', $retval);

if (filter_var($sanitized, FILTER_VALIDATE_FLOAT))
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