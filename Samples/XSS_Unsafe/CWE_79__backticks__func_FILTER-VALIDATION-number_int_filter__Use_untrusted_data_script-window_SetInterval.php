




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = `cat /tmp/tainted.txt`;

if (filter_var($sanitized, FILTER_VALIDATE_INT))
  $tainted = $sanitized ;
else
  $tainted = "" ;

//flaw
echo "window.setInterval('". $tainted ."');" ;
?>
 </script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>