




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$tainted = $_SESSION['UserData'];

$tainted = intval($tainted);


echo "body { color :". $tainted ." ; }" ;
?>
 </style> 
 </script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>