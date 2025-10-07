




<!DOCTYPE html>
<html>
<head>
<script>
<?php
$tainted = $_GET['UserData'];

$tainted = $tainted  == 'safe1' ? 'safe1' : 'safe2';

//flaw
echo "alert(\"". $tainted ."\")" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>