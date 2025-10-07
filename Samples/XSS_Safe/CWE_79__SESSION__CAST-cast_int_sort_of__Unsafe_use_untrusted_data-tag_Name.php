




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = $_SESSION['UserData'];

$tainted += 0 ;


echo "<".  $tainted ." href= \"/bob\" />" ;
?>
<h1>Hello World!</h1>
</body>
</html>