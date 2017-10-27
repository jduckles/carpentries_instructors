import sys
import requests
from requests.auth import HTTPBasicAuth
import json

try:
    import local_settings

except:
    print("Local settings not found")
    sys.exit(1)

data = requests.get('https://amy.software-carpentry.org/api/v1/persons/?badges=2&badges=5&username=&personal=&middle=&family=&email=&may_contact=1&is_instructor=1&o=lastname', auth=HTTPBasicAuth(local_settings.user, local_settings.pw))

# print(data.text)

# Pull just the persons records & transform to python dictionary
persons = json.loads(data.text)['results']

instructors = []

for person in persons[10:20]:
    d = {}

    airport = person['airport'].split("/")[-2]

    workshops = requests.get(person['tasks'], auth=HTTPBasicAuth(local_settings.user, local_settings.pw))
    workshops = json.loads(workshops.text)
    workshops_list = []
    for workshop in workshops:
        workshops_list.append(workshop['event'].split("/")[-2] + " " + workshop['role'])

    d['full name'] = person['personal'] + " " +  person['family']
    d['email'] = person['email']
    d['airport'] = person['airport']
    d['workshops'] = workshops_list

    instructors.append(d)

print(instructors)


# Above code works for one page of API results. Will need to loop through to get all pages.
