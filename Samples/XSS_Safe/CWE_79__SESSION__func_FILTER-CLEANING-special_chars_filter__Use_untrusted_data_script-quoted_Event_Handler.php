




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
$tainted = $_SESSION['UserData'];

$sanitized = filter_var($tainted, FILTER_SANITIZE_SPECIAL_CHARS);
  $tainted = $sanitized ;
      


echo "<div onmouseover=\"x='". $tainted ."'\>";
?>
<h1>Hello World!</h1>
</div>
</body>
</html>