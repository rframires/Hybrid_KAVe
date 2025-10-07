




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = system('ls', $retval);

if (settype($tainted, "integer"))
  $tainted = $tainted ;
else
  $tainted = 0 ;


echo "<div id='".  $tainted ."'>content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>