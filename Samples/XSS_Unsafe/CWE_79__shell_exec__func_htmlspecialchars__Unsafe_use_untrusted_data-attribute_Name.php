




<!DOCTYPE html>
<html>
<body>
<?php
$tainted = shell_exec('cat /tmp/tainted.txt');

$tainted = htmlspecialchars($tainted, ENT_QUOTES);

//flaw
echo "<div ". $tainted ."= bob />" ;
?>
<h1>Hello World!</h1>
</div>
</body>
</html>