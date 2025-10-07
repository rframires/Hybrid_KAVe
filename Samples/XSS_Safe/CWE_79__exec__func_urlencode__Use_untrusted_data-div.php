




<!DOCTYPE html>
<html>
<head/>
<body>
<div>
<?php
$script = "/tmp/tainted.php";
exec($script, $result, $return);

$tainted = $result[0];

$tainted = urlencode($tainted);


echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>