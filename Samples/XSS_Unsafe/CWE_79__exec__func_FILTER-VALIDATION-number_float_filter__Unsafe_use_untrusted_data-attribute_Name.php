




<!DOCTYPE html>
<html>
<body>
<?php
$script = "/tmp/tainted.php";
exec($script, $result, $return);

$tainted = $result[0];

if (filter_var($sanitized, FILTER_VALIDATE_FLOAT))
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