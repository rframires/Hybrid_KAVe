




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = $_GET['UserData'];

$sanitized = filter_var($tainted, FILTER_SANITIZE_FULL_SPECIAL_CHARS);
  $tainted = $sanitized ;
     


echo "x='". $tainted ."'" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>