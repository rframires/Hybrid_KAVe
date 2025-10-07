<?php







$tainted = `cat /tmp/tainted.txt`;

if (settype($tainted, "integer"))
  $tainted = $tainted ;
else
  $tainted = 0 ;

$query = sprintf("SELECT * FROM student where id=%u", $tainted);

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