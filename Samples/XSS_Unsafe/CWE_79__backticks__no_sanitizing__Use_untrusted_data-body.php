




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = `cat /tmp/tainted.txt`;

//no_sanitizing

//flaw
echo $tainted ;
?>
<h1>Hello World!</h1>
</body>
</html>
