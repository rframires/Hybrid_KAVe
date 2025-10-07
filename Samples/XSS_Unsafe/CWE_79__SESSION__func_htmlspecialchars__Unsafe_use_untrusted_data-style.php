




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = $_SESSION['UserData'];

$tainted = htmlspecialchars($tainted, ENT_QUOTES);

//flaw
echo $tainted ;
?>
</style>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>