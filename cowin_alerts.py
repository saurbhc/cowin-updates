import json
import smtplib
from datetime import datetime, timedelta

import requests

CALENDER_BY_DISTRICT = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict"


class CoWinAlerts:
    def __init__(self):
        self.users = []
        self.current_datetime = datetime.now() + timedelta(minutes=300)
        self.smtp = smtplib.SMTP(host='smtp.gmail.com', port=587)

    def execute(self):
        print("running script at: {current_datetime}".format(current_datetime=str(self.current_datetime)))
        self._setup_smtp()
        self._get_all_users()
        self._check_available_slots_and_notify()

    def _setup_smtp(self):
        self.smtp.starttls()
        with open("admin_credentials.json") as admin_credentials_file:
            admin_credentials = json.loads(admin_credentials_file.read())
            user_email = admin_credentials.get("user_email")
            user_email_password = admin_credentials.get("user_email_password")

            self.smtp.login(user_email, user_email_password)

    def _get_all_users(self):
        with open("cowin_user_credentials.json") as co_win_user_credentials_file:
            co_win_user_credentials = json.loads(co_win_user_credentials_file.read())
            self.users = co_win_user_credentials

    def _check_available_slots_and_notify(self):
        for user in self.users:
            token = user.get("token")
            state = user.get("state")
            districts = user.get("districts")
            slack_member_id = user.get("slack_member_id")
            SLACK_WEBHOOK = user.get("SLACK_WEBHOOK")
            user_email = user.get("email")
            current_date = self.current_datetime.strftime("%d-%m-%Y")

            for district_id in districts:
                url = CALENDER_BY_DISTRICT + "?district_id={district_id}&date={date}".format(
                    district_id=district_id,
                    date=current_date
                )
                authorization = "Bearer {token}".format(token=token)
                headers = {
                    'accept': "application/json, text/plain, */*",
                    'authorization': authorization,
                    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
                    'origin': "https://selfregistration.cowin.gov.in"
                }
                response = requests.get(url, headers=headers)
                response_data = json.loads(response.text)

                centers = response_data.get("centers")
                for center in centers:
                    name = center.get("center")
                    address = center.get("address")
                    state_name = center.get("state_name")
                    district_name = center.get("district_name")
                    block_name = center.get("block_name")
                    pincode = center.get("pincode")
                    _from = center.get("from")
                    _to = center.get("to")
                    fee_type = center.get("fee_type")
                    sessions = center.get("sessions")

                    for session in sessions:
                        min_age_limit = session.get("min_age_limit")
                        if min_age_limit == 45:
                            continue

                        available_capacity = session.get("available_capacity")
                        if available_capacity <= 0:
                            continue

                        _date = session.get("date")
                        vaccine = session.get("vaccine")
                        slots = session.get("slots")

                        if SLACK_WEBHOOK:
                            if slack_member_id:
                                slack_user = "<@{slack_member_id}>".format(slack_member_id=slack_member_id)
                            else:
                                slack_user = "there"

                            slack_payload = json.dumps({
                                "text": "Hey {slack_user}, Age: ({min_age_limit}) - '{available_capacity}' capacity of '{vaccine}' available at {address} - {block_name}, {state}. Slots - {slots}".format(
                                    slack_user=slack_user,
                                    min_age_limit=min_age_limit,
                                    available_capacity=available_capacity,
                                    vaccine=vaccine,
                                    address=address,
                                    block_name=block_name,
                                    state=state_name,
                                    slots=" ".join(slots)
                                )
                            })
                            slack_headers = {
                                'Content-type': 'application/json'
                            }
                            print("...posting to slack: ", slack_payload)
                            slack_response = requests.post(SLACK_WEBHOOK, headers=slack_headers, data=slack_payload)

                        if user_email:
                            pass

    def _send_email(self):
        pass


if __name__ == "__main__":
    co_win_alerts_object = CoWinAlerts()
    co_win_alerts_object.execute()
