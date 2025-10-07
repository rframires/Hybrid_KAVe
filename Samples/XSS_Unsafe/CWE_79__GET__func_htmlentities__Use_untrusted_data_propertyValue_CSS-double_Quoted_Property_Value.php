




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = $_GET['UserData'];

$tainted = htmlentities($tainted, ENT_QUOTES);

//flaw
echo "body { color :\"". $tainted ."\" ; }" ;
?>
</style> 
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>