




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = system('ls', $retval);

$tainted = (float) $tainted ;


echo $tainted ;
?>
</style>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>