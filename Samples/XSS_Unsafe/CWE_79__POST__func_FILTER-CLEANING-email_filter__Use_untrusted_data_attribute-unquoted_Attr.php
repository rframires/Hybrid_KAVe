




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = $_POST['UserData'];

$sanitized = filter_var($tainted, FILTER_SANITIZE_EMAIL);
if (filter_var($sanitized, FILTER_VALIDATE_EMAIL))
  $tainted = $sanitized ;
else
  $tainted = "" ;

//flaw
echo "<div id=". $tainted .">content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>