




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$handle = popen('/bin/cat /tmp/tainted.txt', 'r');
$tainted = fread($handle, 4096);
pclose($handle);

$tainted = (float) $tainted ;


echo "<div id=". $tainted .">content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>