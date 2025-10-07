




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
class Input{
  private $input;

  public function getInput(){
    return $this->input[1];
  }

  public  function __construct(){
    $this->input = array();
    $this->input[0]= 'safe' ;
    $this->input[1]= $_GET['UserData'] ;
    $this->input[2]= 'safe' ;
  }
}
$temp = new Input();
$tainted =  $temp->getInput();

//no_sanitizing

//flaw
echo "<div onmouseover=\"x=\"". $tainted ."\"\>";
?>
<h1>Hello World!</h1>
</div>
</body>
</html>