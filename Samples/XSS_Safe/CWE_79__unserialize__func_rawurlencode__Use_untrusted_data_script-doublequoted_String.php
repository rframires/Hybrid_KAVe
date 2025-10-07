




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$string = $_POST['UserData'] ;
$tainted = unserialize($string);
    

$tainted = rawurlencode($tainted);


echo "alert(\"". $tainted ."\")" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>