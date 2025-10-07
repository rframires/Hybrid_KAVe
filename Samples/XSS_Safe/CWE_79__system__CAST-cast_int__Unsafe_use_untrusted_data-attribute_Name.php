




<!DOCTYPE html>
<html>
<body>
<?php
$tainted = system('ls', $retval);

$tainted = (int) $tainted ;


echo "<div ". $tainted ."= bob />" ;
?>
<h1>Hello World!</h1>
</div>
</body>
</html>