




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = `cat /tmp/tainted.txt`;

$tainted = preg_replace('/\'/', '', $tainted);

//flaw
echo $tainted ;
?>
</style>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>