




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = $_SESSION['UserData'];

$tainted = preg_replace('/\W/si','',$tainted);


echo $tainted ;
?>
</style>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>