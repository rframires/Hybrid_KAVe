




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$string = $_POST['UserData'] ;
$tainted = unserialize($string);
    

if (filter_var($sanitized, FILTER_VALIDATE_INT))
  $tainted = $sanitized ;
else
  $tainted = "" ;

//flaw
echo "<div id=". $tainted .">content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>