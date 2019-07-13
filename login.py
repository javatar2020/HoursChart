from bs4 import BeautifulSoup
from datetime import datetime
from getpass import getpass
from login_data import url, headers, form_data
import json
import requests


def format_time(h):
    time = ""
    if h < 10:
        return "0{0}".format(h)
    return "{0}".format(h)

def format_seconds(s):
    hh = s // 3600
    mm = (s % 3600) // 60
    ss = (s % 3600) % 60
    time = "{0}:{1}:{2}".format(format_time(hh), format_time(mm), format_time(ss))
    return (time)

def main():
    form_data["user[login]"] = input("your username ")
    form_data["user[password]"] = getpass("your password ")
    s = requests.Session()
    response = s.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    form_data["authenticity_token"] = soup.find("meta", {"name" : "csrf-token"})["content"]
    response = s.post(url, data=form_data, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    parsed_data = soup.find("span", {"class" : "name"}).getText().replace("\n", "")
    print("Hello " + parsed_data)

    #calculate how many hours in month
    username = input("enter username that u want ")
    response = s.get("https://profile.intra.42.fr/users/"+ username + "/locations_stats").json()
    date_cal = datetime.now().strftime("%Y-%m-01")
    seconds = 0
    for k, v in sorted(response.items()):
        if (k >= date_cal):
            v = v.split(":")
            seconds += (int(v[0]) * 3600) + (int(v[1]) * 60) + (int(v[2].split(".")[0]))

    print(format_seconds(seconds))


if __name__ == '__main__':
    main()
