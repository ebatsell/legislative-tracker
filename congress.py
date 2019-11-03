import requests
import json

# house
# 116
# committee = house committee on veteran's affairs > health, DAMA
# committee ID = HVAC
# subcomitte
# for all bills under those two subcommittees, you want bill name, url, summary (name if summary is null), cosponsors, 
# if no short_title, long title is title
# title is short_title, summary is title if summary is empty

# from https://www.propublica.org/datastore/api/propublica-congress-api
api_key = 'H33K9IKOOD9SIjhXBGkhriE56oCRwdxxUxqQq56O'
congress_id = 116
bill_id = 'hr4249'

def get_bill_info_by_id(bill_id):
	response = requests.get(
		f"https://api.propublica.org/congress/v1/{congress_id}/bills/{bill_id}.json",
		headers={'X-API-Key': api_key}
	)


	# print(json.dumps(response.json(), indent=2))


	bill = response.json()["results"][0]
	short_title = bill["short_title"] 
	long_title = bill["title"] 
	summary = bill["summary"] 
	link = bill["congressdotgov_url"]
	num_cosponsors = bill["cosponsors"]
	sponsor = bill["sponsor"]
	sponsor_party = bill["sponsor_party"]
	sponsor_state = bill["sponsor_state"]

	# fetch sponsor district
	sponsor_response = requests.get(
		bill["sponsor_uri"],
		headers={'X-API-Key': api_key}
	)

	# print(json.dumps(sponsor_response.json(), indent=2))
	sponsor_district = sponsor_response.json()["results"][0]["roles"][0]["district"]

	summary = long_title if (summary == "" or (summary is None)) else summary
	title = short_title if (short_title != "" or short_title is not None) else long_title

	return ','.join([title, summary, link, sponsor, sponsor_party, sponsor_state, sponsor_district, str(num_cosponsors)])

with open("my_congress.csv", "w") as f:
	f.write(','.join(["title", "summary", "link", "sponsor", "sponsor_party", "sponsor_state", "sponsor_district", "cosponsors"]))
	f.write('\n')
	f.write(get_bill_info_by_id(bill_id))

# figure out interface - bill IDs? search terms? something else?

# once you parse through bills and get bill IDs, make call to cosponsors API

# print out data

