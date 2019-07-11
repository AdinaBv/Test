import sys, subprocess

try:
    url = sys.argv[1]
except OSError:
    exit("Wrong url!")
except:
    exit("Wrong url!")

CMD = f"curl -s '{url}' | grep 'https://downloads.wordpress' | sed 's?=\"?\\n?g' | grep 'https://downloads' | sed 's?\">.*??' | sed 's?\" .*??'"
URLS = subprocess.check_output(CMD, shell=True)
URLS = str(URLS)
URLS = URLS.replace("b'", "").replace("'", "")
URLS = URLS.split("\\n")

for url in URLS:
    if url != "":
        print(url)
