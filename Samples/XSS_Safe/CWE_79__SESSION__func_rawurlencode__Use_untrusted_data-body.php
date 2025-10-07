




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = $_SESSION['UserData'];

$tainted = rawurlencode($tainted);


echo $tainted ;
?>
<h1>Hello World!</h1>
</body>
</html>
