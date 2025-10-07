




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = shell_exec('cat /tmp/tainted.txt');

$tainted = rawurlencode($tainted);

//flaw
echo $tainted ;
?>
</script>
</head>
<body onload="xss()">
<h1>Hello World!</h1>
</body>
</html>