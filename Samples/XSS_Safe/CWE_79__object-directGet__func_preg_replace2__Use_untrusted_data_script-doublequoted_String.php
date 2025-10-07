




<!DOCTYPE html>
<html>
<head>
<script>
<?php
class Input{
  public function getInput(){
    return $_GET['UserData'] ;
  }
}

$temp = new Input();
$tainted =  $temp->getInput();

$tainted = preg_replace('/\W/si','',$tainted);


echo "alert(\"". $tainted ."\")" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>