




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$script = "/tmp/tainted.php";
exec($script, $result, $return);

$tainted = $result[0];

if (settype($tainted, "integer"))
  $tainted = $tainted ;
else
  $tainted = 0 ;


echo "<div id=\"". $tainted ."\">content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>