




<!DOCTYPE html>
<html>
<head/>
<body>
<div>
<?php
$tainted = $_POST['UserData'];

$sanitized = filter_var($tainted, FILTER_SANITIZE_NUMBER_INT);
if (filter_var($sanitized, FILTER_VALIDATE_INT))
  $tainted = $sanitized ;
else
  $tainted = "" ;


echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>