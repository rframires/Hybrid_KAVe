




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

$tainted = htmlspecialchars($tainted, ENT_QUOTES);

//flaw
echo $tainted ;
?>
</script>
</head>
<body onload="xss()">
<h1>Hello World!</h1>
</body>
</html>