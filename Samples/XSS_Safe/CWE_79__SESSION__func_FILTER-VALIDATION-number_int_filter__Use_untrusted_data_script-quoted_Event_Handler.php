




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = $_SESSION['UserData'];

if (filter_var($sanitized, FILTER_VALIDATE_INT))
  $tainted = $sanitized ;
else
  $tainted = "" ;


echo "<div onmouseover=\"x='". $tainted ."'\>";
?>
<h1>Hello World!</h1>
</div>
</body>
</html>