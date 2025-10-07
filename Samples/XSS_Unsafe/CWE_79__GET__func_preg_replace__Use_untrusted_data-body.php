




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = $_GET['UserData'];

$tainted = preg_replace('/\'/', '', $tainted);

//flaw
echo $tainted ;
?>
<h1>Hello World!</h1>
</body>
</html>
