import sys

def open_file(file):
    """
    Open file function
    """
    with open(file, encoding="ISO-8859-1") as opened_file:
        lines = opened_file.read().splitlines()
        return lines

REPLACE_CPE = ["alpha", "beta", "rc", "milestone", "pre"]
REPLACE_GIT = ["alpha", "beta", "rc", "milestone", "pre"]
UNUSUAL_GIT = ["a","b"]
CPE_URL = []
CPE_NOURL = []
CPE_ARRAY = []
try:
    CPE_LIST = open_file(sys.argv[1])
    GIT_LIST = open_file(sys.argv[2])
except IndexError:
    print(
        "Something is not right! Use the syntax :\npython3 match.py CPE-LIST GIT-LIST LICENSE-NAME STRING-THAT-YOU-NEED-TO-MATCH"
    )
    exit()
except FileNotFoundError:
    print("File not found!")
    exit()
except:
    print("Something went wrong! Mistakes were made!")
    exit()
try:
    LICENSE = sys.argv[3]
except:
    LICENSE = "NOLICENSE"

try:
    manual_component = sys.argv[4]
except:
    manual_component = ""        

for cpe in CPE_LIST:
    if cpe != "":
        organization = cpe.split(":")[3]
        component = cpe.split(":")[4]
        version = cpe.split(":")[5]
        subversion = cpe.split(":")[6]
        if subversion == "*" or subversion == "-":
            full_version = version
            full_version = full_version.replace("-ce","")
            full_version = full_version.replace("-","")
        else:
            for r in REPLACE_CPE:
                if r in subversion:
                    # if (r + ".") not in subversion:
                        subversion = subversion.replace(r, (r + "."))
            full_version = version + "." + subversion
            full_version = full_version.replace("-ce","")
            full_version = full_version.replace("-","")
    else:
        continue
    for url in GIT_LIST:
        orig_url = url
        url = url.lower()
        try:
            if len(url.split("/")) >= 7:
                url_version = url.split("/")[7]
        except:
            url_version = url.split("/")[-1]
        replaceThis = ["release-","release_", ".release", ".final", "_", "v", ".js", ".zip", ".exe","-ce",".tar.gz", ".dmg", ".bin", ".win-amd64-py2.7",".win32-py2.7", ".win.x64.portable", ".win.x64.", ".tar.bz2", ".win32", ".win64", ".win.x86.portable", ".win.x86", "linux-", "e2fsprogs.", "hdf5.", "windows", "elasticsearch-oss.", "elasticsearch.",  "platform.", ".release", "xwikiplatform", "elefant.", ".stable", "rrrrc.", "betaaaa", "rrc", ".msi", ".tar.xz", ".x64", ".x32", ".tgz",]
        withThis = ["","","","",".","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]

        try:
            if "github" in url:
                git_component = url.split("/")[4]
                url_version = url_version.replace((git_component+"-"),"")
            elif "wordpress" in url:
                url_version = url_version.replace((url_version.split(".")[0]+"."),"")
        except:
            continue

        for i in range(0,len(replaceThis)):
            url_version = url_version.replace(replaceThis[i],withThis[i])

        replaceThisComponent = [manual_component,"-"]
        withThisComponent = ["","."]
        for i in range(0,len(replaceThisComponent)):
            url_version = url_version.replace(replaceThisComponent[i],withThisComponent[i])
        # print(url_version)    
        for r in REPLACE_GIT:
            if r in url_version:
                if (r + ".") not in url_version:
                    url_version = url_version.replace(r, (r + "."))
                if ("." + r ) not in url_version:
                    url_version = url_version.replace(r, ("." + r ))  
        unusual_test = url_version             
        unusual_test = unusual_test.replace("alpha","")
        unusual_test = unusual_test.replace("beta","")
        # print(unusual_test)
        if "a" in unusual_test or "b" in unusual_test:
            for i in range(0,len(UNUSUAL_GIT)):
                url_version = url_version.replace(UNUSUAL_GIT[i],REPLACE_GIT[i])
                for r in REPLACE_GIT:
                    if r in url_version:
                        if (r + ".") not in url_version:
                            url_version = url_version.replace(r, (r + "."))
                        if ("." + r ) not in url_version:
                            url_version = url_version.replace(r, ("." + r ))  
        if full_version == url_version:
            if orig_url[-1] != "/":
                CPE_URL.append(cpe + orig_url)
                CPE_ARRAY.append(cpe)
        # print(full_version+" | "+url_version)            
    if cpe not in CPE_NOURL and cpe not in CPE_ARRAY:
        CPE_NOURL.append(cpe)
for cpe_url in CPE_URL:
    print(cpe_url + "|" + LICENSE)

for peaseant_cpe in CPE_NOURL:
    print(peaseant_cpe + "NOURL|" + LICENSE)    