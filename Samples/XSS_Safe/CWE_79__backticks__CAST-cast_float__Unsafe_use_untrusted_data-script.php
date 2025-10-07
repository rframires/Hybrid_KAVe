




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = `cat /tmp/tainted.txt`;

$tainted = (float) $tainted ;


echo $tainted ;
?>
</script>
</head>
<body onload="xss()">
<h1>Hello World!</h1>
</body>
</html>