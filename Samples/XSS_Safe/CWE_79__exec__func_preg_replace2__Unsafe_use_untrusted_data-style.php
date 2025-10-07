




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$script = "/tmp/tainted.php";
exec($script, $result, $return);

$tainted = $result[0];

$tainted = preg_replace('/\W/si','',$tainted);


echo $tainted ;
?>
</style>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>