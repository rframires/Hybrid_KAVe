




<!DOCTYPE html>
<html>
<head/>
<body>
<div>
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

$tainted = preg_replace('/\'/', '', $tainted);

//flaw
echo $tainted ;
?>
</div>
<h1>Hello World!</h1>
</body>
</html>