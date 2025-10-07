




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$handle = popen('/bin/cat /tmp/tainted.txt', 'r');
$tainted = fread($handle, 4096);
pclose($handle);

$tainted = mysql_real_escape_string($tainted);

//flaw
echo $tainted ;
?>
<h1>Hello World!</h1>
</body>
</html>
