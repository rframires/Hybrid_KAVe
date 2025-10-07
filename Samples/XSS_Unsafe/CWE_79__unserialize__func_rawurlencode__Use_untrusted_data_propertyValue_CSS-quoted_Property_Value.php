




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$string = $_POST['UserData'] ;
$tainted = unserialize($string);
    

$tainted = rawurlencode($tainted);

//flaw
echo "body { color :\'". $tainted ."\' ; }" ;
?>
</style> 
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>