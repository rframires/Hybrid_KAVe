




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$string = $_POST['UserData'] ;
$tainted = unserialize($string);
    

$tainted = rawurlencode($tainted);


echo $tainted ;
?>
<h1>Hello World!</h1>
</body>
</html>
