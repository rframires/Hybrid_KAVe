




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$string = $_POST['UserData'] ;
$tainted = unserialize($string);
    

$legal_table = array("safe1", "safe2");
if (in_array($tainted, $legal_table, true)) {
  $tainted = $tainted;
} else {
  $tainted = $legal_table[0];
}

//flaw
echo "<span style=\"color :". checked_data ."\">Hey</span>" ;
?>
<h1>Hello World!</h1>
</body>
</html>