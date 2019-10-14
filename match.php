<?php

$CPEs = file($argv[1], FILE_IGNORE_NEW_LINES);
$URLs = file($argv[2], FILE_IGNORE_NEW_LINES);
$license = "NOLICENSE";
if (isset($argv[3])) {
    $license = $argv[3];
}

$cpeUrlArray = array();
$cpeArray = array();

foreach ($CPEs as $cpe) {
    $check1 = explode(":", $cpe);

    $componentName = $check1[4];
    if ($check1[6] == "*" || $check1[6] == "-") {
        $ver = $check1[5];
        $ver = str_replace("alpha", "alpha.", $ver);
        $ver = str_replace("beta", "beta.", $ver);
        $ver = str_replace("milestone", "m", $ver);
        $ver = str_replace("-", ".", $ver);
        $ver = str_replace("-", ".", $ver);
        $ver = str_replace(".dev.", "", $ver);
        $ver = str_replace("rc", "rc.", $ver);
        /*$ver = str_replace("rc", "rc.", $ver);
        $ver = str_replace("1.0.0", "1.0", $ver);
        $ver = str_replace("1.1.0", "1.1", $ver);
        $ver = str_replace("1.2.0", "1.2", $ver);
        $ver = str_replace("2.0.0", "2.0", $ver);
        $ver = str_replace("2.1.0", "2.1", $ver);
        $ver = str_replace("2.2.0", "2.2", $ver);*/
        //$ver = str_replace($replaceThis, $withThis, $ver);
    } else {
        $ver = "$check1[5].$check1[6]";
        $ver = str_replace("alpha", "alpha.", $ver);
        $ver = str_replace("beta", "beta.", $ver);
        $ver = str_replace("milestone", "m", $ver);
        $ver = str_replace("-", ".", $ver);
        $ver = str_replace(":", ".", $ver);
        $ver = str_replace("rc", "rc.", $ver);
        $ver = str_replace(".dev.", "", $ver);
        /*$ver = str_replace("1.0.0", "1.0", $ver);
        $ver = str_replace("1.1.0", "1.1", $ver);
        $ver = str_replace("1.2.0", "1.2", $ver);
        $ver = str_replace("2.0.0", "2.0", $ver);
        $ver = str_replace("2.1.0", "2.1", $ver);
        $ver = str_replace("2.2.0", "2.2", $ver);*/
        //$ver = str_replace($replaceThis, $withThis, $ver);
        //$ver = str_replace(".rc", "rc", $ver);
    }
    foreach ($URLs as $url) {
        $origURL = $url;
        $url = strtolower($url);
        $array1 = explode("/", $url);
        $replaceThis = ["$componentName-", "miniupnpd_", "release-", "-release", "_", "v", "alpha", "beta", "rc", "ddpre", "beta1111", "beta2222", "beta311", "beta411", ".zip", ".exe", ".tar.gz", ".dmg", ".bin", ".win-amd64-py2.7", "-", ".win32-py2.7", ".win.x64.portable", ".win.x64.", ".tar.bz2", ".win32", ".win64", ".win.x86.portable", ".win.x86", ".final", "linux-", "e2fsprogs.", "hdf5.", "windows", "elasticsearch-oss.", "elasticsearch.", ".release", ".final", "platform.", ".release", "xwikiplatform", "elefant.", ".stable", "rrrrc.", "betaaaa", "rrc", ".msi", ".tar.xz", ".x64", ".x32",".tgz"];
        $withThis = ["", "", "", "", ".", "", "alpha.", "beta.", "rc.", ".pre.", ".beta.1", ".beta.2", "beta.3", "beta.4", "", "", "", "", "", "", ".", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "beta.", "rc.", "", "", "", "",""];
        if (isset($array1[7])) {
            //if ($array1[5] != ""){
            $urlVer = str_replace($replaceThis, $withThis, $array1[7]);
            //  }

        } else {
            $urlVer = str_replace($replaceThis, $withThis, end($array1));
        }

        $x = explode(".", $ver);
        $y = explode(".", $urlVer);
        $aa = strlen($urlVer);
        $ab = strlen($ver);

        //$ver = $ver.".0";
        
        // if (count($x) == 2) {
        //     if ($ver !== $urlVer) {
        //         $ver = $ver . ".0";
        //     }
        // }
        // print "$ver|$urlVer\n";
        if ($aa == $ab) {
            if ($ver == $urlVer && strlen(substr(strrchr($ver, "."), 1)) == strlen(substr(strrchr($urlVer, "."), 1))) {
                //if (strpos($urlVer,$ver) !== False ) {
                //print "$ver|$urlVer\n";

                $cpeUrl = $cpe . $origURL;
                array_push($cpeUrlArray, $cpeUrl);
                if (!in_array($cpe, $cpeArray)) {
                    array_push($cpeArray, $cpe);
                    //break;
                }
            }
        }
    }
}

foreach ($cpeUrlArray as $cpeResult) {
    if (substr($cpeResult, -1) !== "/") {
        print($cpeResult . "|" . $license . "\n");
    }
}
foreach ($CPEs as $cpe) {
    if (!in_array($cpe, $cpeArray)) {
        print "$cpe" . "NOURL|" . $license . "\n";
    }
}
