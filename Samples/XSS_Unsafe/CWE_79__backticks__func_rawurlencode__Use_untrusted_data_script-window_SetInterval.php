




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = `cat /tmp/tainted.txt`;

$tainted = rawurlencode($tainted);

//flaw
echo "window.setInterval('". $tainted ."');" ;
?>
 </script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>