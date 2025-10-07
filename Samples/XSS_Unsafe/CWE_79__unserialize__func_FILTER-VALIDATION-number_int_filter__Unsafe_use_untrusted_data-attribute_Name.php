




<!DOCTYPE html>
<html>
<body>
<?php
$string = $_POST['UserData'] ;
$tainted = unserialize($string);
    

if (filter_var($sanitized, FILTER_VALIDATE_INT))
  $tainted = $sanitized ;
else
  $tainted = "" ;

//flaw
echo "<div ". $tainted ."= bob />" ;
?>
<h1>Hello World!</h1>
</div>
</body>
</html>