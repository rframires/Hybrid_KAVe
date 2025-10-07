




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = $_POST['UserData'];

$tainted = urlencode($tainted);


echo "alert('". $tainted ."')" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>