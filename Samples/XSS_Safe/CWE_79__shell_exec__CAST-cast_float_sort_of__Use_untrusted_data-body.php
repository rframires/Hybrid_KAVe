




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = shell_exec('cat /tmp/tainted.txt');

$tainted += 0.0 ;


echo $tainted ;
?>
<h1>Hello World!</h1>
</body>
</html>
