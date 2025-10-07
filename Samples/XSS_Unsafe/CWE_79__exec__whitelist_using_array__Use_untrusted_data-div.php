




<!DOCTYPE html>
<html>
<head/>
<body>
<div>
<?php
$script = "/tmp/tainted.php";
exec($script, $result, $return);

$tainted = $result[0];

$legal_table = array("safe1", "safe2");
if (in_array($tainted, $legal_table, true)) {
  $tainted = $tainted;
} else {
  $tainted = $legal_table[0];
}

//flaw
echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>