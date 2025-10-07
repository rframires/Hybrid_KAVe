




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = `cat /tmp/tainted.txt`;

$tainted = floatval($tainted);


echo "<div id=\"". $tainted ."\">content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>