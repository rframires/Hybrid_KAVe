




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$string = $_POST['UserData'] ;
$tainted = unserialize($string);
    

$sanitized = filter_var($tainted, FILTER_SANITIZE_FULL_SPECIAL_CHARS);
  $tainted = $sanitized ;
     

//flaw
echo "body { color :\"". $tainted ."\" ; }" ;
?>
</style> 
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>