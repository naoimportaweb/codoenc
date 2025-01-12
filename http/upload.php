
<?php
$uploaddir = dirname(__FILE__) . '/uploads/';
$token = $_GET["token"];
$data = json_decode(file_get_contents('php://input'), true);
$config = null;

$filename = dirname(__FILE__) . '/data/config.json';
$config = json_decode(file_get_contents($filename), true);

if( $token != $config["token"] ) {
    header("HTTP/1.1 500 Internal Server Error");
    die();  
}


if (!file_exists( $uploaddir )) {
    mkdir( $uploaddir, 1777, true);
}

$uploaddirworkspace = $uploaddir . $_GET["id"] . '/';
if (!file_exists( $uploaddirworkspace )) {
    mkdir( $uploaddirworkspace, 1777, true);
}

$uploadfile = $uploaddirworkspace . basename($_FILES['userfile']['name']);

if (move_uploaded_file($_FILES['userfile']['tmp_name'], $uploadfile)) {
    $retorno = array("status" => true);
    echo json_encode( $retorno );
} else {
    $retorno = array("status" => false);
    echo json_encode( $retorno );
}


?>
