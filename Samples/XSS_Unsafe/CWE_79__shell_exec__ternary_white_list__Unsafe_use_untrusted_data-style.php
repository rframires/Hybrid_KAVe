




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = shell_exec('cat /tmp/tainted.txt');

$tainted = $tainted  == 'safe1' ? 'safe1' : 'safe2';

//flaw
echo $tainted ;
?>
</style>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>