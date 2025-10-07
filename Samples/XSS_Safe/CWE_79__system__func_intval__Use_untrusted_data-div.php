




<!DOCTYPE html>
<html>
<head/>
<body>
<div>
<?php
$tainted = system('ls', $retval);

$tainted = intval($tainted);


echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>