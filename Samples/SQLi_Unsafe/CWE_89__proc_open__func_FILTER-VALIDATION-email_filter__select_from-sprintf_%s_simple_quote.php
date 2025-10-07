<?php







$descriptorspec = array(
  0 => array("pipe", "r"),
  1 => array("pipe", "w"),
  2 => array("file", "/tmp/error-output.txt", "a")
  );
$cwd = '/tmp';
$process = proc_open('more /tmp/tainted.txt', $descriptorspec, $pipes, $cwd, NULL);
if (is_resource($process)) {
  fclose($pipes[0]);
  $tainted = stream_get_contents($pipes[1]);
  fclose($pipes[1]);
  $return_value = proc_close($process);
}

if (filter_var($sanitized, FILTER_VALIDATE_EMAIL))
  $tainted = $sanitized ;
else
  $tainted = "" ;

$query = sprintf("SELECT * FROM '%s'", $tainted);

//flaw
$conn = mysql_connect('localhost', 'mysql_user', 'mysql_password'); // Connection to the database (address, user, password)
mysql_select_db('dbname') ;
echo "query : ". $query ."<br /><br />" ;

$res = mysql_query($query); //execution

while($data =mysql_fetch_array($res)){
print_r($data) ;
echo "<br />" ;
} 
mysql_close($conn);

?>