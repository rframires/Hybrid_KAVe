




<!DOCTYPE html>
<html>
<head/>
<body>
<div>
<?php
$handle = popen('/bin/cat /tmp/tainted.txt', 'r');
$tainted = fread($handle, 4096);
pclose($handle);

$tainted = $tainted  == 'safe1' ? 'safe1' : 'safe2';

//flaw
echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>