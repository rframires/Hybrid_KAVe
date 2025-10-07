




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = system('ls', $retval);

$tainted = rawurlencode($tainted);


echo $tainted ;
?>
<h1>Hello World!</h1>
</body>
</html>
