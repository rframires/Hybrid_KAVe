




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = `cat /tmp/tainted.txt`;

$tainted = intval($tainted);


echo $tainted ;
?>
<h1>Hello World!</h1>
</body>
</html>
