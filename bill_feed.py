import requests
import json

from secrets import API_KEY
from bill import Bill
from hvac_bill import HVACBill

# curl "https://api.propublica.org/congress/v1/115/house/bills/introduced.json?offset=60" -H "X-API-Key: H33K9IKOOD9SIjhXBGkhriE56oCRwdxxUxqQq56O"

# last_seen_id = ""
congress_id = 116

class BillFeed():
    # Class to execute the main bill feed pipeline, and process incoming bills
    # segment them into relevant buckets and start the processes there

    def __init__(self):
        # Represents last bill seen by the feed, so next time this runs it stops when it hits this bill
        self.last_seen_id = open("last_seen_id.txt", "r").read()

    def publish(self):
        for bill in self.latest_bills():
            self.process_bill(bill)

    def process_bill(self, bill):
        # look at the attributes we care about
        # if a bill matches certain attributes, process it in a certain way
        if bill["committee"] == "Veteran's Affairs" and bill["subcommittee"] == "DMCA":
            bill.process() # probably the best way to do this? maybe?

    def latest_bills(self):
        """Return a generator of bill objects representing all bills introduced
        since the function was last run.
        :params
        """
        print("hello?")

        bill_type = "introduced" # might want to look into active
        first_seen_id = None
        offset = 0
        while True: 
            response = requests.get(
                f"https://api.propublica.org/congress/v1/{congress_id}/house/bills/{bill_type}.json",
                headers={'X-API-Key': API_KEY},
                params={"offset": offset}
            )
            offset += 20

            # Assumption that there is only one result in results list
            for bill in response.json()["results"][0]["bills"]:
                if first_seen_id is None:
                    first_seen_id = bill["bill_id"]

                # stop the whole function if we've hit the last bill
                if bill["bill_id"] == self.last_seen_id:
                    self._update_last_seen(first_seen_id)
                    return

                yield Bill.from_json(bill)

    def _update_last_seen(self, new_last_seen):
        with open("last_seen_id.txt", "w") as f:
            f.write(new_last_seen)
        self.last_seen_id = new_last_seen


if __name__ == "__main__":
    # assumption that there is no newline at the end of the file
    bills = list(latest_bills(last_seen_id))
    print(len(bills))
    feed = BillFeed()
    feed.publish()
