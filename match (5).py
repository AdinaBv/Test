import sys , argparse

def open_file(file):
    """
    Open file function
    """
    with open(file, encoding="ISO-8859-1") as opened_file:
        lines = opened_file.read().splitlines()
        return lines

def count_letters(version):
    """
    Verify how many letters are in a version by scanning the url link
    """
    result = []
    for letter in version:
        if letter.isalpha():
            result.append(letter)
    return result            
parser = argparse.ArgumentParser(description='Script for matching CPEs with URLs')


parser.add_argument('-cpe', '--cpe',
                      action='store',
                      help='Add path to CPE list',
                      required=True)
parser.add_argument('-urls', '--urls',
                      action='store',
                      help='Add path to URL list',
                      required=True)
parser.add_argument('-lic', '--lic',
                      action='store',
                      help='Add LICENSE for the component',
                      required=False)
parser.add_argument('-remove', '--remove',
                      action='store',
                      help='Remove a string form the version text',
                      required=False)                      
parser.add_argument('--debug', 
                      action='store_true',
                      help='Use this option to see what the script actually matches',
                      required=False)

args = parser.parse_args()._get_kwargs()
dict_args  = dict(args)

REPLACE_CPE = ["alpha", "beta", "rc", "milestone", "pre"]
REPLACE_GIT = ["alpha", "beta", "rc", "milestone", "pre"]
UNUSUAL_GIT = ["a","b"]
CPE_URL = []
CPE_NOURL = []
CPE_ARRAY = []
IGNORE_LIST = [".asc",".sha",".md5","a256","html",".sum"]

try:
    CPE_LIST = open_file(dict_args['cpe'])
    GIT_LIST = open_file(dict_args['urls'])
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
    
if dict_args['lic'] is not None:
    LICENSE = dict_args['lic']
else:
    LICENSE = "NOLICENSE"

if dict_args['remove'] is not None:
    manual_component = dict_args['remove']
else:
    manual_component = ""        

for cpe in CPE_LIST:
    if cpe != "":
        organization = cpe.split(":")[3]
        component = cpe.split(":")[4]
        version = cpe.split(":")[5]
        subversion = cpe.split(":")[6]
        cpeReplaceThis = ["x-","-ce","v","-"]
        cpeWithThis = ["x.","","","."]
        if subversion == "*" or subversion == "-":
            full_version = version
            for i in range(0,len(cpeReplaceThis)):
                full_version = full_version.replace(cpeReplaceThis[i],cpeWithThis[i])
        else:
            for r in REPLACE_CPE:
                if r in subversion:
                    if (r + ".") not in subversion:
                        subversion = subversion.replace(r, (r + "."))
            full_version = version + "." + subversion
            for i in range(0,len(cpeReplaceThis)):
                full_version = full_version.replace(cpeReplaceThis[i],cpeWithThis[i])
    else:
        continue
    for url in GIT_LIST:
        orig_url = url
        url = url.lower()
        try:
            if "pythonhosted" in url:
                url_version = url.split("/")[-1]
            elif len(url.split("/")) >= 7:
                url_version = url.split("/")[7]
            else:
                url_version = url.split("/")[-1]
        except:
            url_version = url.split("/")[-1]

        replaceThis = [manual_component,"stable-","-src","-api","-sources","-release","release-","release_", ".release", ".final", "version-","ver_", "_", "v", ".js", ".zip", ".exe","-ce",".tar.gz", ".dmg", ".bin","-bin", ".win-amd64-py2.7",".win32-py2.7", ".win.x64.portable", ".win.x64.", ".tar.bz2", ".win32", ".win64", ".win.x86.portable", ".win.x86", "linux-", "e2fsprogs.", "hdf5.", "windows", "elasticsearch-oss.", "elasticsearch.",  "platform.", ".release", "xwikiplatform", "elefant.", ".stable", "rrrrc.", "betaaaa", "rrc", ".msi", ".tar.xz", ".x64", ".x32", ".tgz","-win32","-win64","-macosx",".jar"]
        withThis = ["","","","","","","","","","","","",".","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]
        
        try:
            if "github" in url:
                git_component = url.split("/")[4]
                url_version = url_version.replace((git_component+"-"),"")
            elif "wordpress" in url:
                url_version = url_version.replace((url_version.split(".")[0]+"."),"")
            else:
                url_version = url.split("/")[-1]
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
        alpha_test = count_letters(url_version)
        if len(alpha_test) == 1:
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
        if dict_args['debug']:  
            print(full_version + " | " + url_version)            
    if cpe not in CPE_NOURL and cpe not in CPE_ARRAY:
        CPE_NOURL.append(cpe)
if not dict_args['debug']:        
    for cpe_url in CPE_URL:
        print(cpe_url + "|" + LICENSE)

    for peaseant_cpe in CPE_NOURL:
        print(peaseant_cpe + "NOURL|" + LICENSE)    
