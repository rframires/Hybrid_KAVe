




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$handle = popen('/bin/cat /tmp/tainted.txt', 'r');
$tainted = fread($handle, 4096);
pclose($handle);

$legal_table = array("safe1", "safe2");
if (in_array($tainted, $legal_table, true)) {
  $tainted = $tainted;
} else {
  $tainted = $legal_table[0];
}

//flaw
echo "body { color :\'". $tainted ."\' ; }" ;
?>
</style> 
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>