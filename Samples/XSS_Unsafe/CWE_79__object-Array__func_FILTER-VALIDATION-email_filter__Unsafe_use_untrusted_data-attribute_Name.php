




<!DOCTYPE html>
<html>
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

if (filter_var($sanitized, FILTER_VALIDATE_EMAIL))
  $tainted = $sanitized ;
else
  $tainted = "" ;

//flaw
echo "<div ". $tainted ."= bob />" ;
?>
<h1>Hello World!</h1>
</div>
</body>
</html>