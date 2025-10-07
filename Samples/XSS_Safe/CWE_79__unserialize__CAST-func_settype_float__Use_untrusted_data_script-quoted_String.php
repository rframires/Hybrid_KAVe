




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$string = $_POST['UserData'] ;
$tainted = unserialize($string);
    

if(settype($tainted, "float"))
  $tainted = $tainted ;
else
  $tainted = 0.0 ;


echo "alert('". $tainted ."')" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>