




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = $_GET['UserData'];

$sanitized = filter_var($tainted, FILTER_SANITIZE_MAGIC_QUOTES);
  $tainted = $sanitized ;
      

//flaw
echo "window.setInterval('". $tainted ."');" ;
?>
 </script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>