




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = system('ls', $retval);

$tainted = mysql_real_escape_string($tainted);

//flaw
echo "x=\"". $tainted."\"" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>