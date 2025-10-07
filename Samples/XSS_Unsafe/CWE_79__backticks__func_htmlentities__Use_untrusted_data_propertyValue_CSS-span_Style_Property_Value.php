




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = `cat /tmp/tainted.txt`;

$tainted = htmlentities($tainted, ENT_QUOTES);

//flaw
echo "<span style=\"color :". checked_data ."\">Hey</span>" ;
?>
<h1>Hello World!</h1>
</body>
</html>