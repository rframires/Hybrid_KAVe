




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = $_POST['UserData'];

$tainted = urlencode($tainted);


echo "<div onmouseover=\"x='". $tainted ."'\>";
?>
<h1>Hello World!</h1>
</div>
</body>
</html>