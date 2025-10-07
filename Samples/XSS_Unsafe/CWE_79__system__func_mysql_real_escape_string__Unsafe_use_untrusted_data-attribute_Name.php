




<!DOCTYPE html>
<html>
<body>
<?php
$tainted = system('ls', $retval);

$tainted = mysql_real_escape_string($tainted);

//flaw
echo "<div ". $tainted ."= bob />" ;
?>
<h1>Hello World!</h1>
</div>
</body>
</html>