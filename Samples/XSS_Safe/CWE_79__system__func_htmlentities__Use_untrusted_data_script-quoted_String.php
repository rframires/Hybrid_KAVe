




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = system('ls', $retval);

$tainted = htmlentities($tainted, ENT_QUOTES);


echo "alert('". $tainted ."')" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>