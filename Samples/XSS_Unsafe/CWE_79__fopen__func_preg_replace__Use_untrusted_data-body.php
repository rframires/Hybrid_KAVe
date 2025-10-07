




<!DOCTYPE html>
<html>
<head/>
<body>
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

$tainted = preg_replace('/\'/', '', $tainted);

//flaw
echo $tainted ;
?>
<h1>Hello World!</h1>
</body>
</html>
