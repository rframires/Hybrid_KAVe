




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = system('ls', $retval);

$tainted = $tainted + 0;


echo "<div id=". $tainted .">content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>