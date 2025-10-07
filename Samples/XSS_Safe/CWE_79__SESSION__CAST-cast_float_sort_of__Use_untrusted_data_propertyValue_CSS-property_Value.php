




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = $_SESSION['UserData'];

$tainted += 0.0 ;


echo "body { color :". $tainted ." ; }" ;
?>
 </style> 
 </script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>