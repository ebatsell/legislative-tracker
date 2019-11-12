import requests
import json

from secrets import API_KEY

# house
# 116
# committee = house committee on veteran's affairs > health, DAMA
# committee ID = HVAC
# subcomitte
# for all bills under those two subcommittees, you want bill name, url, summary (name if summary is null), cosponsors, 
# if no short_title, long title is title
# title is short_title, summary is title if summary is empty

congress_id = 116

class Bill():
    def __init__(self, bill_id):
        self.id = bill_id
        self.title = None
        self.summary = None
        self.link = None
        self.sponsor = None
        self.sponsor_party = None
        self.sponsor_state = None
        self.sponsor_district = None
        self.num_cosponsors = None

    @classmethod
    def from_json(cls, bill_json):
        # TODO... actually create it
        
        return Bill(bill_json["bill_id"])


    def fetch_bill_info(self):
        response = requests.get(
            f"https://api.propublica.org/congress/v1/{congress_id}/bills/{self.bill_id}.json",
            headers={'X-API-Key': API_KEY}
        )

        bill = response.json()["results"][0]

        short_title = bill["short_title"] 
        long_title = bill["title"] 
        summary = bill["summary"] 
        self.summary = long_title if (summary == "" or (summary is None)) else summary
        self.title = short_title if (short_title != "" or short_title is not None) else long_title

        self.link = bill["congressdotgov_url"]
        self.num_cosponsors = bill["cosponsors"]
        self.sponsor = bill["sponsor"]
        self.sponsor_party = bill["sponsor_party"]
        self.sponsor_state = bill["sponsor_state"]

        # fetch sponsor district
        sponsor_response = requests.get(
            bill["sponsor_uri"],
            headers={'X-API-Key': api_key}
        )

        # print(json.dumps(sponsor_response.json(), indent=2))
        self.sponsor_district = sponsor_response.json()["results"][0]["roles"][0]["district"]


        return ','.join([
            self.title,
            self.summary,
            self.link,
            self.sponsor,
            self.sponsor_party,
            self.sponsor_state,
            self.sponsor_district,
            str(self.num_cosponsors)
        ])


    def update_bill(self):
        response = requests.get(
            f"https://api.propublica.org/congress/v1/{congress_id}/bills/{self.bill_id}.json",
            headers={'X-API-Key': API_KEY}
        )

        bill = response.json()["results"][0]
        num_cosponsors = bill["cosponsors"]

        if self.num_cosponsors << num_cosponsors:
            print("alert or something") 

        # update in bill_db


if __name__ == "__main__":
    with open("my_congress.csv", "w") as f:
        f.write(','.join(["title", "summary", "link", "sponsor", "sponsor_party", "sponsor_state", "sponsor_district", "cosponsors"]))
        f.write('\n')
        f.write(Bill('hr4249').fetch_bill_info())

# figure out interface - bill IDs? search terms? something else?

# once you parse through bills and get bill IDs, make call to cosponsors API

# print out data

