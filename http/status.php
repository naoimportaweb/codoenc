<?php

$data = json_decode(file_get_contents('php://input'), true);
$filename = dirname(__FILE__) . '/data/config.json';
$config = json_decode(file_get_contents($filename), true);

if( $token != $config["token"] ) {
    header("HTTP/1.1 500 Internal Server Error");
    die();  
}


echo json_encode(array("status" => true));

?>