




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = $_POST['UserData'];

$tainted = rawurlencode($tainted);

//flaw
echo "body { color :\"". $tainted ."\" ; }" ;
?>
</style> 
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>