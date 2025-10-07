




<!DOCTYPE html>
<html>
<head>
<style>
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

if (filter_var($sanitized, FILTER_VALIDATE_EMAIL))
  $tainted = $sanitized ;
else
  $tainted = "" ;

//flaw
echo $tainted ;
?>
</style>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>