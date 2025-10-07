




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = $_GET['UserData'];

$tainted = addslashes($tainted);

//flaw
echo "window.setInterval('". $tainted ."');" ;
?>
 </script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>