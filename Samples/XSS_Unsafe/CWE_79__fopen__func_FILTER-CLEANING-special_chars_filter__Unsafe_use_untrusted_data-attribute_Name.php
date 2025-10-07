




<!DOCTYPE html>
<html>
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
echo "<div ". $tainted ."= bob />" ;
?>
<h1>Hello World!</h1>
</div>
</body>
</html>