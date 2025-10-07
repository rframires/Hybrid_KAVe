




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
class Input{
  public function getInput(){
    return $_GET['UserData'] ;
  }
}

$temp = new Input();
$tainted =  $temp->getInput();

if(settype($tainted, "float"))
  $tainted = $tainted ;
else
  $tainted = 0.0 ;


echo $tainted ;
?>
<h1>Hello World!</h1>
</body>
</html>
