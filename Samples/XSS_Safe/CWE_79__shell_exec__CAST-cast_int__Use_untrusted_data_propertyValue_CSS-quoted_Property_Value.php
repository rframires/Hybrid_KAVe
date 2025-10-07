




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = shell_exec('cat /tmp/tainted.txt');

$tainted = (int) $tainted ;


echo "body { color :\'". $tainted ."\' ; }" ;
?>
</style> 
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>