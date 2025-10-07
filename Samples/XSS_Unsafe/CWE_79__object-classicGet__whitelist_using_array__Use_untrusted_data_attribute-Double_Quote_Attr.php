




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

$legal_table = array("safe1", "safe2");
if (in_array($tainted, $legal_table, true)) {
  $tainted = $tainted;
} else {
  $tainted = $legal_table[0];
}

//flaw
echo "<div id=\"". $tainted ."\">content</div>" ;
?>
<h1>Hello World!</h1>
</body>
</html>