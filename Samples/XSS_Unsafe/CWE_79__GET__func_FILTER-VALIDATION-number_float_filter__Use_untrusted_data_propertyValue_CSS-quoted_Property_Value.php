




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = $_GET['UserData'];

if (filter_var($sanitized, FILTER_VALIDATE_FLOAT))
  $tainted = $sanitized ;
else
  $tainted = "" ;

//flaw
echo "body { color :\'". $tainted ."\' ; }" ;
?>
</style> 
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>