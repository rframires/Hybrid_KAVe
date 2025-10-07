<?php







$array = array();
$array[] = 'safe' ;
$array[] = $_GET['userData'] ;
$array[] = 'safe' ;
$tainted = $array[1] ;

$legal_table = array("safe1", "safe2");
if (in_array($tainted, $legal_table, true)) {
  $tainted = $tainted;
} else {
  $tainted = $legal_table[0];
}

$query = "SELECT lastname, firstname FROM drivers, vehicles WHERE drivers.id = vehicles.ownerid AND vehicles.tag='". $tainted . "'";

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