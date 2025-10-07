




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = shell_exec('cat /tmp/tainted.txt');

$tainted = floatval($tainted);


echo $tainted ;
?>
<h1>Hello World!</h1>
</body>
</html>
