




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$string = $_POST['UserData'] ;
$tainted = unserialize($string);
    

$sanitized = filter_var($tainted, FILTER_SANITIZE_SPECIAL_CHARS);
  $tainted = $sanitized ;
      


echo $tainted ;
?>
<h1>Hello World!</h1>
</body>
</html>
