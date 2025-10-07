




<!DOCTYPE html>
<html>
<body>
<?php
$tainted = `cat /tmp/tainted.txt`;

$tainted = addslashes($tainted);

//flaw
echo "<div ". $tainted ."= bob />" ;
?>
<h1>Hello World!</h1>
</div>
</body>
</html>