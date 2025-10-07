




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$string = $_POST['UserData'] ;
$tainted = unserialize($string);
    

//no_sanitizing

//flaw
echo $tainted ;
?>
</script>
</head>
<body onload="xss()">
<h1>Hello World!</h1>
</body>
</html>