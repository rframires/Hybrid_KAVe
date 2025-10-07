




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = $_SESSION['UserData'];

$tainted = htmlentities($tainted, ENT_QUOTES);

//flaw
echo "window.setInterval('". $tainted ."');" ;
?>
 </script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>