




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = `cat /tmp/tainted.txt`;

//no_sanitizing

//flaw
echo "x='". $tainted ."'" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>