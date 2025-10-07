




<!DOCTYPE html>
<html>
<body>
<?php
$tainted = shell_exec('cat /tmp/tainted.txt');

//no_sanitizing

//flaw
echo "<div ". $tainted ."= bob />" ;
?>
<h1>Hello World!</h1>
</div>
</body>
</html>