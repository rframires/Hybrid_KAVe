




<!DOCTYPE html>
<html>
<head/>
<body>
<div>
<?php
$tainted = $_POST['UserData'];

$tainted = addslashes($tainted);

//flaw
echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>