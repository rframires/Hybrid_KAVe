




<!DOCTYPE html>
<html>
<head>
<style>
<?php
$array = array();
$array[] = 'safe' ;
$array[] = $_GET['userData'] ;
$array[] = 'safe' ;
$tainted = $array[1] ;

if(settype($tainted, "float"))
  $tainted = $tainted ;
else
  $tainted = 0.0 ;


echo "body { color :". $tainted ." ; }" ;
?>
 </style> 
 </script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>