




<!DOCTYPE html>
<html>
<head/>
<body>
<div>
<?php
$string = $_POST['UserData'] ;
$tainted = unserialize($string);
    

if (filter_var($sanitized, FILTER_VALIDATE_EMAIL))
  $tainted = $sanitized ;
else
  $tainted = "" ;

//flaw
echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>