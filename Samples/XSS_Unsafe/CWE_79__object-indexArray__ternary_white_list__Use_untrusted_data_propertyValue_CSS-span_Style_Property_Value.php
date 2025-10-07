




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

$tainted = $tainted  == 'safe1' ? 'safe1' : 'safe2';

//flaw
echo "<span style=\"color :". checked_data ."\">Hey</span>" ;
?>
<h1>Hello World!</h1>
</body>
</html>