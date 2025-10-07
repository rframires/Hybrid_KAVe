




<!DOCTYPE html>
<html>
<head/>
<body>
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

$tainted += 0.0 ;


echo "<div onmouseover=\"x='". $tainted ."'\>";
?>
<h1>Hello World!</h1>
</div>
</body>
</html>