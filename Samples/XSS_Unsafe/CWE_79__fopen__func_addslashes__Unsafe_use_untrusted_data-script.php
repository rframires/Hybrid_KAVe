




<!DOCTYPE html>
<html>
<head>
<script>
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

$tainted = addslashes($tainted);

//flaw
echo $tainted ;
?>
</script>
</head>
<body onload="xss()">
<h1>Hello World!</h1>
</body>
</html>