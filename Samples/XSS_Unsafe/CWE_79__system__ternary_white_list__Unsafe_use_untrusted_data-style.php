




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = system('ls', $retval);

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