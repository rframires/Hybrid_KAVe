




<!DOCTYPE html>
<html>
<body>
<?php
$tainted = $_SESSION['UserData'];

$tainted = urlencode($tainted);

//flaw
echo "<div ". $tainted ."= bob />" ;
?>
<h1>Hello World!</h1>
</div>
</body>
</html>