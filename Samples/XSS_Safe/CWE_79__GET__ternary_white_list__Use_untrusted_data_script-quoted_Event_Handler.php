




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = $_GET['UserData'];

$tainted = $tainted  == 'safe1' ? 'safe1' : 'safe2';


echo "<div onmouseover=\"x='". $tainted ."'\>";
?>
<h1>Hello World!</h1>
</div>
</body>
</html>