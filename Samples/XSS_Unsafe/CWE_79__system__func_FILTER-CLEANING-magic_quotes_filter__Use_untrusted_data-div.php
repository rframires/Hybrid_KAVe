




<!DOCTYPE html>
<html>
<head/>
<body>
<div>
<?php
$tainted = system('ls', $retval);

$sanitized = filter_var($tainted, FILTER_SANITIZE_MAGIC_QUOTES);
  $tainted = $sanitized ;
      

//flaw
echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>