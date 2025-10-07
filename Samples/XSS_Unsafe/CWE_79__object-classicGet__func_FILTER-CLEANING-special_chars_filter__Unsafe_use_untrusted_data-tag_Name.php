




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

$sanitized = filter_var($tainted, FILTER_SANITIZE_SPECIAL_CHARS);
  $tainted = $sanitized ;
      

//flaw
echo "<".  $tainted ." href= \"/bob\" />" ;
?>
<h1>Hello World!</h1>
</body>
</html>