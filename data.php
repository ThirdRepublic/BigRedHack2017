<?php
	$classNames = $_POST["classNamesLst"];
	$url = $_POST["url"];
	$username = $_POST["username"];
	$password = $_POST["password"];
	$urlType = $_POST["urlList"];
	
	$myfile = fopen("data.csv", "a");
	for($i = 0; $i < count($classNames); $i++){
		$str = $classNames[$i].",".$urlType[$i].",".$url[$i].",".$username[$i].",".$password[$i]."\n";
		//echo($str);
		fwrite($myfile, $str);
	}
	fclose($myfile);

$command = escapeshellcmd('login.py');
$output = shell_exec($command);
echo $output;


	//header('Location: index.html');
	//exit;
?>