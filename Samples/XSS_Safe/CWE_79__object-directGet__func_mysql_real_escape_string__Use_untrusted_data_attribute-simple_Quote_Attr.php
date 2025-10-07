




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

$tainted = mysql_real_escape_string($tainted);


echo "<div id='".  $tainted ."'>content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>