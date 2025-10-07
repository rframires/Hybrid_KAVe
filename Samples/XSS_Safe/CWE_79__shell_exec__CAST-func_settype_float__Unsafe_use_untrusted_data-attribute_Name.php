




<!DOCTYPE html>
<html>
<body>
<?php
$tainted = shell_exec('cat /tmp/tainted.txt');

if(settype($tainted, "float"))
  $tainted = $tainted ;
else
  $tainted = 0.0 ;


echo "<div ". $tainted ."= bob />" ;
?>
<h1>Hello World!</h1>
</div>
</body>
</html>