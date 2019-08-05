import requests, json, sys
try:
    initial_link = sys.argv[1]
except:
    print("Add link to be checked !")

component = initial_link.split("/")[-1]
link = "https://replicate.npmjs.com/" + component

req = requests.get(link)
info = json.dumps(req.json())
json_dict = json.loads(info)

try:
    items = json_dict["versions"]
    for item in items:
        url = items[item]["dist"]["tarball"]
        print(url)
except KeyError:
    print("Something went super duper wrong!")

try:
    license = json_dict["license"]
    print("The license is : " + license)
except:
    print("Could not find any license !")
