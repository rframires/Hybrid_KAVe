




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = $_POST['UserData'];

$tainted = mysql_real_escape_string($tainted);

//flaw
echo "<div onmouseover=\"x=\"". $tainted ."\"\>";
?>
<h1>Hello World!</h1>
</div>
</body>
</html>