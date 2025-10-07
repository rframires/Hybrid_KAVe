




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = $_GET['UserData'];

$tainted = mysql_real_escape_string($tainted);

//flaw
echo "body { color :\"". $tainted ."\" ; }" ;
?>
</style> 
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>