<?php
//SENTRY script for GITHUB projects


$compUrl = $argv[1];
if (substr($argv[1], -1) != "/") {
    $compUrl = $argv[1] . "/";
}
print "$compUrl\n";
//download main project page
while (true) {
    exec("curl -s $compUrl > /tmp/githubPage");
    $redirectText = '<html><body>You are being <a href="https://github.com/';

    //split the component URL into multiple fields
    $splitComp = explode("/", $compUrl);
    $comp = $splitComp[3] . "/" . $splitComp[4];

    //check if page redirects to a different project. One example that does this is https://github.com/ziyaddin/xampp
    if (!exec("grep '$redirectText' '/tmp/githubPage'")) {

        //get number of releases
        $relNumber = str_replace(',', '', exec("grep -a -m 1 -A2 '<svg class=\"octicon octicon-tag\"' /tmp/githubPage | tail -n 1 | xargs"));
        print "Number of releases: $relNumber\n";

        break;
    } else {
        $compUrl = exec("grep '$redirectText' '/tmp/githubPage' | sed 's?^.*a href=\"??' | sed 's?\">.*?/?'");
    }

}

function getUrls($compUrl, $pages)
{
    global $comp;
    $grep1 = $comp . "/releases/download";
    $grep2 = $comp . "/files/";
    $grep3 = $comp . "/archive/";
    $grep4 = $comp . "/releases?after=";
    $grep5 = "relative-time datetime";
    $compRels = $compUrl . "releases";
    for ($i = 1; $i <= $pages; $i++) {
        $rc = 0; //save the retry count so that we stop trying to get the urls of a page after 3 attempts
        while (true) {
            exec("curl -s '$compRels' | grep -a ' href=\|$grep5' | grep -a '$grep1\|$grep2\|$grep3\|$grep4\|$grep5' | sed 's?^.* href=\"/?https://github.com/?' | sed 's?^.*href=\"??' | sed 's?\" .*??' | sed 's?^.*datetime=\"?date=?' | sed 's?\">.*??' | tr '\n' '|' | sed 's?date=?\\ndate=?g' | sed 's?|$??' | sed '\$a\' | sed 's?^date=??'", $urls);
            if (!empty($urls)) {
                foreach ($urls as $release) {
                    $url = explode("|", $release);
                    foreach (array_slice($url, 1) as $dlink) {
                        if (!strpos($dlink, "/releases?after=")) {
                            print "$dlink\n";
                        } else { $compRels = $dlink;}
                    }
                }
                unset($urls);
                break;
            } else {
                print "Abuse mechanism triggered. Waiting \n";
                $rc++;
                if ($rc <= '2') {
                    sleep(90);
                } else {
                    print "Already retried 3 times. Skipping to next project.\n";
                    break;
                }
            }
        }
    }
}

$pageNum = ceil($relNumber / 10);
getUrls($compUrl, $pageNum);
