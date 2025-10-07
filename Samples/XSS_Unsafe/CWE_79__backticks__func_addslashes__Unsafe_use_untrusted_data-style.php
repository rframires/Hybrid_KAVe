




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = `cat /tmp/tainted.txt`;

$tainted = addslashes($tainted);

//flaw
echo $tainted ;
?>
</style>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>