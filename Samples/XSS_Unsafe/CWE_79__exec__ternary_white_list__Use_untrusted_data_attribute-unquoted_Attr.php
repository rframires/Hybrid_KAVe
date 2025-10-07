




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$script = "/tmp/tainted.php";
exec($script, $result, $return);

$tainted = $result[0];

$tainted = $tainted  == 'safe1' ? 'safe1' : 'safe2';

//flaw
echo "<div id=". $tainted .">content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>