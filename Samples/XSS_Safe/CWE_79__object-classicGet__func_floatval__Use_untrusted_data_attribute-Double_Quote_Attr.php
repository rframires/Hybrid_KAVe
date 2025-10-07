




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
class Input{
  private $input;

  public function getInput(){
    return $this->input;
  }

  public  function __construct(){
   $this->input = $_GET['UserData'] ;
  }
}
$temp = new Input();
$tainted =  $temp->getInput();

$tainted = floatval($tainted);


echo "<div id=\"". $tainted ."\">content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>