




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = $_POST['UserData'];

$tainted = mysql_real_escape_string($tainted);


echo "<div id=\"". $tainted ."\">content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>