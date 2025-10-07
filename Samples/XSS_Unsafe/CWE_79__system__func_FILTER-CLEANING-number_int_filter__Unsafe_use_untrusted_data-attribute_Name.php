




<!DOCTYPE html>
<html>
<body>
<?php
$tainted = system('ls', $retval);

$sanitized = filter_var($tainted, FILTER_SANITIZE_NUMBER_INT);
if (filter_var($sanitized, FILTER_VALIDATE_INT))
  $tainted = $sanitized ;
else
  $tainted = "" ;

//flaw
echo "<div ". $tainted ."= bob />" ;
?>
<h1>Hello World!</h1>
</div>
</body>
</html>