




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

$sanitized = filter_var($tainted, FILTER_SANITIZE_FULL_SPECIAL_CHARS);
  $tainted = $sanitized ;
     


echo "x='". $tainted ."'" ;
?>
</script>
</head>
<body>
<h1>Hello World!</h1>
</body>
</html>