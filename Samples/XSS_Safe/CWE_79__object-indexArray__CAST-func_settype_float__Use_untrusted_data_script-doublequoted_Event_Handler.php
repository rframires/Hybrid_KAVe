




<!DOCTYPE html>
<html>
<head/>
<body>
<?php
class Input{
  private $input;

  public function getInput(){
    return $this->input['realOne'];
  }

  public  function __construct(){
    $this->input = array();
    $this->input['test']= 'safe' ;
    $this->input['realOne']= $_GET['UserData'] ;
    $this->input['trap']= 'safe' ;
  }
}
$temp = new Input();
$tainted =  $temp->getInput();

if(settype($tainted, "float"))
  $tainted = $tainted ;
else
  $tainted = 0.0 ;


echo "<div onmouseover=\"x=\"". $tainted ."\"\>";
?>
<h1>Hello World!</h1>
</div>
</body>
</html>