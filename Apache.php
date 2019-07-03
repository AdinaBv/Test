<?php

//SENTRY SCRIPT FOR ARCHIVE.APACHE.ORG/DIST

include "../txungo.php";

function noprotocol($url)
{
    $array = explode("//", $url);
    return $array[1];
}

$txdb = array(
    "root" => "../urls/apache",
    "new" => array("break" => 2.1),
);

$txdbm = array(
    "root" => "../",
    "MASTER" => array("break" => 2.1, "lookup" => true),
);

function scanFolder($url)
{
    global $txdb;
    global $txdbm;
    exec("curl -s \"$url\" | grep -v 'PARENTDIR\|\"../' | grep '^<img src' | grep 'a href=' | sed 's?^.*href=\"?$url?' | sed 's?\">.*.</a>??' | awk {'print $1\"|\"$2'}", $itemList);
    foreach ($itemList as $item) {
        $array = explode("|", $item);
        if (substr($array[0], -1) != "/") {
            $file = $array[0];
            $urlid = txungo_j64_encode(md5(noprotocol($file)));
            $new = false;
            $fork = "UNDEFINED";
            if (!strtotime($array[1])) {
                $date = "UNDEFINED";
            } else { $date = date("Y-m-d", strtotime($array[1]));}
            $lic = "UNDEFINED";
            if (!txungo_exists($txdb, "new", $urlid)) {
                if (!txungo_exists($txdbm, "MASTER", $urlid)) {
                    print "$file\n";
                    txungo_insert($txdb, "new", $urlid, "$fork|$date|$lic|$file");
                    $new = true;
                }
            }
            if (!$new) {print "$file\n";}
        } else {
            scanFolder($array[0]);
        }
    }
    unset($itemList);
}
$url = $argv[1];
//$url=$argv[1];
scanFolder($url);
