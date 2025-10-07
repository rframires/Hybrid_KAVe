




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = $_POST['UserData'];

$tainted = htmlspecialchars($tainted, ENT_QUOTES);

//flaw
echo "<div id=". $tainted .">content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>