




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = $_SESSION['UserData'];

$tainted = intval($tainted);


echo "alert(\"". $tainted ."\")" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>