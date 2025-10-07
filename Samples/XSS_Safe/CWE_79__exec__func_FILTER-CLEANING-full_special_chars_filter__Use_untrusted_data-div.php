




<!DOCTYPE html>
<html>
<head/>
<body>
<div>
<?php
$script = "/tmp/tainted.php";
exec($script, $result, $return);

$tainted = $result[0];

$sanitized = filter_var($tainted, FILTER_SANITIZE_FULL_SPECIAL_CHARS);
  $tainted = $sanitized ;
     


echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>