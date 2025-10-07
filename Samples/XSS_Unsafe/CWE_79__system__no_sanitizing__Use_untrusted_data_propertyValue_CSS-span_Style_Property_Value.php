




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = system('ls', $retval);

//no_sanitizing

//flaw
echo "<span style=\"color :". checked_data ."\">Hey</span>" ;
?>
<h1>Hello World!</h1>
</body>
</html>