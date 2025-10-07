




<!DOCTYPE html>
<html>
<body>
<?php
$tainted = $_POST['UserData'];

$sanitized = filter_var($tainted, FILTER_SANITIZE_SPECIAL_CHARS);
  $tainted = $sanitized ;
      

//flaw
echo "<div ". $tainted ."= bob />" ;
?>
<h1>Hello World!</h1>
</div>
</body>
</html>