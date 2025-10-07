




<!DOCTYPE html>
<html>
<head>
<script>
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

if(settype($tainted, "float"))
  $tainted = $tainted ;
else
  $tainted = 0.0 ;


echo "x='". $tainted ."'" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>