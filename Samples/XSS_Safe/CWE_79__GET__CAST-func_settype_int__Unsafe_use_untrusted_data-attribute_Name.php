




<!DOCTYPE html>
<html>
<body>
<?php
$tainted = $_GET['UserData'];

if (settype($tainted, "integer"))
  $tainted = $tainted ;
else
  $tainted = 0 ;


echo "<div ". $tainted ."= bob />" ;
?>
<h1>Hello World!</h1>
</div>
</body>
</html>