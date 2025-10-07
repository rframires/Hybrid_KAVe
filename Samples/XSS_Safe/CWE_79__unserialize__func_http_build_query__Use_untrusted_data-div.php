




<!DOCTYPE html>
<html>
<head/>
<body>
<div>
<?php
$string = $_POST['UserData'] ;
$tainted = unserialize($string);
    

$tainted = http_build_query($tainted);


echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>