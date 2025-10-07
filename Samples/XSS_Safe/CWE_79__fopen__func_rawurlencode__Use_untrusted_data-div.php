




<!DOCTYPE html>
<html>
<head/>
<body>
<div>
<?php
$handle = @fopen("/tmp/tainted.txt", "r");

if ($handle) {
  if(($tainted = fgets($handle, 4096)) == false) {
    $tainted = "";
  }
  fclose($handle);
} else {
  $tainted = "";
}

$tainted = rawurlencode($tainted);


echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>