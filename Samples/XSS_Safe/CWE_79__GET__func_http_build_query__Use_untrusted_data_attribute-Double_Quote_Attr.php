




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = $_GET['UserData'];

$tainted = http_build_query($tainted);


echo "<div id=\"". $tainted ."\">content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>