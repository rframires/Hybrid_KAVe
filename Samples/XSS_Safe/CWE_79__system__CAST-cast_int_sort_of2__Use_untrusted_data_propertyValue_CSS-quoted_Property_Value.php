




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = system('ls', $retval);

$tainted = $tainted + 0;


echo "body { color :\'". $tainted ."\' ; }" ;
?>
</style> 
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>