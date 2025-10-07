




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = $_SESSION['UserData'];

$tainted = preg_replace('/\W/si','',$tainted);


echo "body { color :". $tainted ." ; }" ;
?>
 </style> 
 </script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>