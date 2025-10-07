




<!DOCTYPE html>
<html>
<head>
<style>
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

$sanitized = filter_var($tainted, FILTER_SANITIZE_MAGIC_QUOTES);
  $tainted = $sanitized ;
      

//flaw
echo $tainted ;
?>
</style>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>