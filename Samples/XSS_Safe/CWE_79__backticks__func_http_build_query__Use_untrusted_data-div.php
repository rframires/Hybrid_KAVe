




<!DOCTYPE html>
<html>
<head/>
<body>
<div>
<?php
$tainted = `cat /tmp/tainted.txt`;

$tainted = http_build_query($tainted);


echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>