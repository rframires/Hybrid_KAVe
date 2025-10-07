




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = `cat /tmp/tainted.txt`;

$tainted = (float) $tainted ;


echo "<div onmouseover=\"x='". $tainted ."'\>";
?>
<h1>Hello World!</h1>
</div>
</body>
</html>