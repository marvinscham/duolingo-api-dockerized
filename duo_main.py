import json
import logging
import os
import time
from datetime import datetime

import pytz
import schedule

import duolingo

__version__ = "v2.3.0-beta"

duo_user_name = os.getenv("DUO_USERNAME")
duo_user_jwt = os.getenv("DUO_JWT")

timezone = os.getenv("TIMEZONE", "Europe/Berlin")
xp_summary_days = int(os.getenv("XP_SUMMARY_DAYS", 30))
update_interval = int(os.getenv("UPDATE_INTERVAL", 15))
max_retries = int(os.getenv("MAX_RETRIES", 3))

log = logging.getLogger("duolingo-data")
log.setLevel("INFO")
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
)
log.addHandler(handler)

if not duo_user_name or not duo_user_jwt:
    raise KeyError("Incorrect setup: username, jwt missing.")

log.info("I'm alive!")
log.info(f"Running {__version__}")


def convert_timestamp(timestamp, timezone):
    dt = datetime.utcfromtimestamp(timestamp)
    dt_utc = pytz.utc.localize(dt)
    tz = pytz.timezone(timezone)
    dt_local = dt_utc.astimezone(tz)

    formatted_date = dt_local.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date


def job(retries=max_retries):
    try:
        duo_user = duolingo.Duolingo(
            username=duo_user_name,
            jwt=duo_user_jwt,
        )
        user_fields = [
            "courses",
            "creationDate",
            "id",
            "learningLanguage",
            "totalXp",
            "trackingProperties",
        ]
        user_total_info = duo_user.get_data_by_user_id(user_fields)

        date_format = "%Y-%m-%d"

        username = user_total_info["trackingProperties"]["username"]
        learning_language_abbr = user_total_info["learningLanguage"]

        user_date_timestamp = user_total_info["creationDate"]
        user_date_str = datetime.fromtimestamp(user_date_timestamp).strftime(
            date_format
        )

        language_progress = duo_user.get_language_progress(
            learning_language_abbr)

        streak_info = duo_user.get_streak_info()

        xp_summary_start = datetime.fromtimestamp(
            time.time() - (60 * 60 * 24 * (xp_summary_days - 1))
        ).strftime(date_format)
        xp_summary_end = datetime.fromtimestamp(
            time.time()).strftime(date_format)

        lang_data = duo_user.get_all_languages()
        timestamp = str(int(time.time()))
        timestamp_date = convert_timestamp(int(timestamp), timezone)

        user_object = {
            "username": username,
            "streak": language_progress["streak"],
            "xp": user_total_info["totalXp"],
            "creation_date": user_date_str,
            "learning_language": learning_language_abbr,
            "streak_today": streak_info["streak_extended_today"],
            "timestamp": timestamp,
            "timestamp_hr": timestamp_date,
            "xp_summary_timezone": timezone,
            "xp_summary_count": xp_summary_days,
            "xp_summary": duo_user.get_xp_summaries(
                xp_summary_start,
                xp_summary_end,
                timezone,
            ),
            "lang_data": lang_data,
        }

        str_user = json.dumps(user_object, indent=4)

        if len(str_user) < 10:
            log.error("Faulty response from Duolingo")
        else:
            f = open("duo_user_info.json", "w")
            f.write(str_user)
            f.close()

            log.info(
                f"Updated {username}'s info: {user_total_info['totalXp']} XP @ {timestamp_date}")

        time.sleep(2)
    except Exception as e:
        log.warning(e)

        retries -= 1

        if retries <= 0:
            log.error("Out of retries. Waiting for next execution.")
            return

        log.info("Attempt {}, retrying in 60 seconds".format(
            max_retries - retries))
        time.sleep(60)
        job(retries)

        return


schedule.every(update_interval).minutes.do(job)
log.info("Schedule registered, starting first job execution...")
job()

while True:
    schedule.run_pending()

    time.sleep(1)
