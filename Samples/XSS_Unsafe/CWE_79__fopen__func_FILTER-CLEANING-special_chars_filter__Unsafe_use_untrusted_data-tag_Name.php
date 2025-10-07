




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

$sanitized = filter_var($tainted, FILTER_SANITIZE_SPECIAL_CHARS);
  $tainted = $sanitized ;
      

//flaw
echo "<".  $tainted ." href= \"/bob\" />" ;
?>
<h1>Hello World!</h1>
</body>
</html>