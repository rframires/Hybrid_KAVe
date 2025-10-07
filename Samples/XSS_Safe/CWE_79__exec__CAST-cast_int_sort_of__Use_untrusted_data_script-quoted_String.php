




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$script = "/tmp/tainted.php";
exec($script, $result, $return);

$tainted = $result[0];

$tainted += 0 ;


echo "alert('". $tainted ."')" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>