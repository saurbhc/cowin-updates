# cowin-updates

[BUY ME COFFEE](https://buymeacoffee.com/saurabhchopra)

This project is created for getting COVID Vaccine alerts on my SLACK Channel.

I created and deployed this project on my AWS in an hour so any Code Improvements are welcome.

Email me at saurabhchopra0108@gmail.com with your user credentials to get alerts on your channel too!

### If you want to setup this on your own server, follow the steps below:

1. Clone repo.
2. Create python3 virtualenv. `python3 -m venv .venv`
3. Activate virtualenv. `source .venv/bin/activate`
4. Install dependencies. `pip install -r requirements.txt`
5. Update User Credentials file. 

```
[
  {
    "token": "<your www.cowin.gov.in user token>",
    "state": <your cowin unique state id>,
    "districts": [<your cowin unique district ids>],
    "slack_member_id": "<your slack member id>",  # optional
    "SLACK_WEBHOOK": "<your slack webhook>",  # optional
    "email": "<your email address>"  # optional
  },
  {
    "token": "<your www.cowin.gov.in user token>",
    "state": <your cowin unique state id>,
    "districts": [<your cowin unique district ids>],
    "slack_member_id": "<your slack member id>",  # optional
    "SLACK_WEBHOOK": "<your slack webhook>",  # optional
    "email": "your email address"  # optional
  },
]
```

It can send updates on your:

    a. email
    b. slack

6. Run the script. `cd /home/ubuntu/saurabh/cowin-updates/ && /home/ubuntu/saurabh/cowin-updates/.venv/bin/python /home/ubuntu/saurabh/cowin-updates/cowin_alerts.py >> /home/ubuntu/saurabh/cowin-updates/cowin_alerts_log.py`
7. Add to crontab. 
```
crontab -e
*/1 * * * * cd /home/ubuntu/saurabh/cowin-updates/ && /home/ubuntu/saurabh/cowin-updates/.venv/bin/python /home/ubuntu/saurabh/cowin-updates/cowin_alerts.py >> /home/ubuntu/saurabh/cowin-updates/cowin_alerts_log.py 2>&1
```
8. [BMC](https://buymeacoffee.com/saurabhchopra)

### Any feedback is welcome :)
