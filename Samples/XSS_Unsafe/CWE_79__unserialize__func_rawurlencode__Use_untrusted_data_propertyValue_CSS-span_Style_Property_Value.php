




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$string = $_POST['UserData'] ;
$tainted = unserialize($string);
    

$tainted = rawurlencode($tainted);

//flaw
echo "<span style=\"color :". checked_data ."\">Hey</span>" ;
?>
<h1>Hello World!</h1>
</body>
</html>