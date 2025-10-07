




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$string = $_POST['UserData'] ;
$tainted = unserialize($string);
    

if (filter_var($sanitized, FILTER_VALIDATE_FLOAT))
  $tainted = $sanitized ;
else
  $tainted = "" ;


echo "<div onmouseover=\"x=\"". $tainted ."\"\>";
?>
<h1>Hello World!</h1>
</div>
</body>
</html>