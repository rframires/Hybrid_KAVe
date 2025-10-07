




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = $_SESSION['UserData'];

if (settype($tainted, "integer"))
  $tainted = $tainted ;
else
  $tainted = 0 ;


echo "x='". $tainted ."'" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>