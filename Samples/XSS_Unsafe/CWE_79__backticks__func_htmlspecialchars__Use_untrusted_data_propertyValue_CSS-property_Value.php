




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = `cat /tmp/tainted.txt`;

$tainted = htmlspecialchars($tainted, ENT_QUOTES);

//flaw
echo "body { color :". $tainted ." ; }" ;
?>
 </style> 
 </script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>