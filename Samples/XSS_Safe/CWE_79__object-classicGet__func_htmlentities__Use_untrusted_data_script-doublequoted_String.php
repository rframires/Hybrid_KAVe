




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

$tainted = htmlentities($tainted, ENT_QUOTES);


echo "alert(\"". $tainted ."\")" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>