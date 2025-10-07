




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$handle = popen('/bin/cat /tmp/tainted.txt', 'r');
$tainted = fread($handle, 4096);
pclose($handle);

$sanitized = filter_var($tainted, FILTER_SANITIZE_FULL_SPECIAL_CHARS);
  $tainted = $sanitized ;
     


echo "<div id='".  $tainted ."'>content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>