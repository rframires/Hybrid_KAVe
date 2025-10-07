




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$script = "/tmp/tainted.php";
exec($script, $result, $return);

$tainted = $result[0];

$tainted = htmlspecialchars($tainted, ENT_QUOTES);


echo $tainted ;
?>
<h1>Hello World!</h1>
</body>
</html>
