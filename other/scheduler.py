import schedule
from datetime import timedelta, time, datetime
import time as clk
from pytz import utc
from tzlocal import get_localzone

# 09:00 - 00:00 UTC Time Market Data Updates
# 14:30 - 21:00 UTC Trading Hours

# 14:00 Fetch Today's Pre-Market Data
# If Pre-Market Data Exists, Market is Open Today Continue, Else Wait Next Day
# 15:00 - 20:00 Every Hour Buy/Sell Depending On Next Hour's Open Price LSTM Prediction
# 21:00 Sell Stock

def job():
    print("Starting Day... Fetching New Data")

def job2():
    print("Call The Hourly Job")
    return

def job3():
    # is the 1 minute after the func is first called
    schedule.every(1).minutes.until(timedelta(hours=6)).do(job2)
    # schedule.every(1).hours.until(timedelta(hours=6)).do(job2)


# schedule.every().day.at('10:00', timezone('UTC')).do(job)
def utc2local(utc):
    tz = get_localzone() # local timezone 
    d = datetime.now(tz) # or some other local date 
    offset = int(d.utcoffset().total_seconds() / 3600)
    if offset < 0:
        offset += 24
    hi = utc + timedelta(hours=offset)
    string_time = hi.strftime('%Y-%m-%d-%H:%M:%SS')
    return string_time[11:16]
    

hi = utc2local(datetime(2001, 6, 14, 6,0, 0, tzinfo=utc))

schedule.every().day.at(hi).do(job)
# at 10am zulu time, check if data has arrived
# if it has then market is open today else not open

schedule.every().day.at(time(5, 0, 41, 0).isoformat(timespec='auto')).do(job3)
# schedule.every().day.at("1 hour before i wante to make my first trade").do(job3)


# if it is open continue from 9am to 3pm at every interval (2pm zulu to 8pm zulu)
# run the lstm algo to decide wehter to buy thes tock or sell

while True:
    schedule.run_pending()
    clk.sleep(1)