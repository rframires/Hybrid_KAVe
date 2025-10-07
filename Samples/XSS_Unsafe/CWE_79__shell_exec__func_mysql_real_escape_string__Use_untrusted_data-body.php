




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = shell_exec('cat /tmp/tainted.txt');

$tainted = mysql_real_escape_string($tainted);

//flaw
echo $tainted ;
?>
<h1>Hello World!</h1>
</body>
</html>
