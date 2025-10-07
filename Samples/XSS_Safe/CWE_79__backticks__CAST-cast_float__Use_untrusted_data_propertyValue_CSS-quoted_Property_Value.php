




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = `cat /tmp/tainted.txt`;

$tainted = (float) $tainted ;


echo "body { color :\'". $tainted ."\' ; }" ;
?>
</style> 
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>