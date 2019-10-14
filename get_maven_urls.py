import requests
import sys

p_org = sys.argv[1]
p_name = sys.argv[2]

def sentry_check_extension(item):
    extensions_ignore = ["md5", "MD5", "md5sum", "MD5SUM", "asc", "sha", "sha1", "sha1sum", "SHA1SUM", "sha256",
                         "sha256sum",
                         "sha512", "sig", "pom", "meta", "readme", "README", "news", "changes", "html", "xml", "txt",
                         "pdf", "sign", "dsc", "CHECKSUM", "log"]
    filename_ignore = ["MD5", "CHECKSUM", "CHECKSUMS", "README", "MD5SUMS-for-bz2", "MD5SUMS-for-gz", "SOURCES",
                       "NEWS", "md5sum", "MD5SUM", "sha1sum", "SHA1SUM", "CHANGES", "COPYRIGHT", "Binary",
                       "SHASUMS256.txt"]
    extension_array = item.split(".")
    filename_array = item.split("/")
    # Check extension
    if extension_array[-1] in extensions_ignore or filename_array[-1] in filename_ignore:
        return True
    else:
        return False


artifact_api_page = 'https://search.maven.org/solrsearch/select?q=g:' + \
                    p_org + '+AND+a:' + p_name + '&core=gav&rows=20000&wt=json'
artifact_api_content = requests.get(artifact_api_page)
json_artifact = artifact_api_content.json()
for version_info in json_artifact['response']['docs']:
    ver = version_info['v']
    dl_extensions = version_info['ec']
    for extension in dl_extensions:
        url = 'http://repo1.maven.org/maven2/' + p_org.replace('.', '/') \
              + '/' + p_name + '/' + ver + '/' + p_name + '-' + ver + extension
        if not sentry_check_extension(url):
            print(url)


