




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$string = $_POST['UserData'] ;
$tainted = unserialize($string);
    

if (filter_var($sanitized, FILTER_VALIDATE_FLOAT))
  $tainted = $sanitized ;
else
  $tainted = "" ;

//flaw
echo $tainted ;
?>
</style>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>