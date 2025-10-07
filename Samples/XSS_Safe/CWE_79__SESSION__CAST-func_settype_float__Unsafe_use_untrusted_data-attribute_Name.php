




<!DOCTYPE html>
<html>
<body>
<?php
$tainted = $_SESSION['UserData'];

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