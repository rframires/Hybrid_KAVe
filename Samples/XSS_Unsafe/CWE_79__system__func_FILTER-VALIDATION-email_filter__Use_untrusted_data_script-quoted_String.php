




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = system('ls', $retval);

if (filter_var($sanitized, FILTER_VALIDATE_EMAIL))
  $tainted = $sanitized ;
else
  $tainted = "" ;

//flaw
echo "alert('". $tainted ."')" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>