




<!DOCTYPE html>
<html>
<head/>
<body>
<div>
<?php
$tainted = $_SESSION['UserData'];

if (filter_var($sanitized, FILTER_VALIDATE_FLOAT))
  $tainted = $sanitized ;
else
  $tainted = "" ;


echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>