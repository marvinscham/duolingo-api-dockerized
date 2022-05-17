import json, time, logging, schedule, requests
from datetime import datetime
import duolingo
from duo_settings import (
    duo_user_name,
    duo_user_password,
    server_url,
    count_days,
    timezone,
)

log = logging.getLogger("duolingo-data")
log.setLevel("INFO")
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
)
log.addHandler(handler)

log.info("I'm alive!")


def connectivity_handler():
    page = requests.get(server_url + "/duo_user_info.json")
    if page.status_code != 200:
        log.error("Server cannot be reached.")


def job(retries=5):
    try:
        duo_user = duolingo.Duolingo(duo_user_name, duo_user_password)
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

        language_progress = duo_user.get_language_progress(learning_language_abbr)

        streak_info = duo_user.get_streak_info()

        user_object = {
            "username": username,
            "streak": language_progress["streak"],
            "xp": user_total_info["totalXp"],
            "creation_date": user_date_str,
            "learning_language": learning_language_abbr,
            "streak_today": streak_info["streak_extended_today"],
            "timestamp": str(int(time.time())),
            "last_week_timezone": timezone,
            "last_week_count": count_days,
            "last_week": duo_user.get_xp_summaries(
                datetime.fromtimestamp(
                    time.time() - (60 * 60 * 24 * (count_days - 1))
                ).strftime(date_format),
                datetime.fromtimestamp(time.time()).strftime(date_format),
                timezone,
            ),
        }

        lang_data = duo_user.get_all_languages()
        str_user = json.dumps(user_object, indent=4)
        str_lang = json.dumps(lang_data, indent=4)

        if len(str_user) < 10 or len(str_lang) < 10:
            log.error("Faulty response from Duolingo")
        else:
            f = open("duo_user_info.json", "w")
            f.write(str_user)
            f.close()

            f = open("duo_lang_info.json", "w")
            f.write(str_lang)
            f.close()

            log.info("Successfully updated info")

        time.sleep(2)
        connectivity_handler()
    except Exception as e:
        log.warn(e)

        retries -= 1

        if retries == 0:
            log.error("Out of retries. Waiting for next execution.")
            return

        log.info("Attempt {}, retrying in 60 seconds".format(5 - retries))
        time.sleep(60)
        job(retries)

        return


schedule.every(30).minutes.do(job)
log.info("Schedule registered, starting first job execution...")
job()

while True:
    schedule.run_pending()

    time.sleep(1)
