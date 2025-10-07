




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

if(settype($tainted, "float"))
  $tainted = $tainted ;
else
  $tainted = 0.0 ;


echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>