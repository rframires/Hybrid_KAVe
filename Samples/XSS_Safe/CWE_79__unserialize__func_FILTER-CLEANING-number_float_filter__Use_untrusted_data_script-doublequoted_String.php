




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$string = $_POST['UserData'] ;
$tainted = unserialize($string);
    

$sanitized = filter_var($tainted, FILTER_SANITIZE_NUMBER_FLOAT);
if (filter_var($sanitized, FILTER_VALIDATE_FLOAT))
  $tainted = $sanitized ;
else
  $tainted = "" ;


echo "alert(\"". $tainted ."\")" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>