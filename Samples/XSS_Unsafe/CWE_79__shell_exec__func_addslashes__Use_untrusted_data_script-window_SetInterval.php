




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = shell_exec('cat /tmp/tainted.txt');

$tainted = addslashes($tainted);

//flaw
echo "window.setInterval('". $tainted ."');" ;
?>
 </script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>