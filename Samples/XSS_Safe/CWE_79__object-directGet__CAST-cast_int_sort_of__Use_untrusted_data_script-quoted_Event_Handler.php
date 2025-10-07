




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

$tainted += 0 ;


echo "<div onmouseover=\"x='". $tainted ."'\>";
?>
<h1>Hello World!</h1>
</div>
</body>
</html>