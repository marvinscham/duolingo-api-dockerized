import json, time, logging, schedule, requests
from datetime import datetime
import duolingo
from duo_settings import duo_user_name, duo_user_password, server_url

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


def job():
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

        username = user_total_info["trackingProperties"]["username"]
        learning_language_abbr = user_total_info["learningLanguage"]

        user_date_timestamp = user_total_info["creationDate"]
        user_date_str = datetime.fromtimestamp(user_date_timestamp).strftime("%d/%m/%Y")

        language_progress = duo_user.get_language_progress(learning_language_abbr)

        xp_progress = duo_user.get_daily_xp_progress()

        streak_info = duo_user.get_streak_info()

        user_object = {
            "username": username,
            "streak": language_progress["streak"],
            "xp": user_total_info["totalXp"],
            "creation_date": user_date_str,
            "learning_language": language_progress["language_string"],
            "xp_today": xp_progress["xp_today"],
            "lessons_today": len(xp_progress["lessons_today"]),
            "streak_today": streak_info["streak_extended_today"],
            "timestamp": str(int(time.time())),
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
        log.error(e)


schedule.every(30).minutes.do(job)
log.info("Schedule registered, starting first job execution...")
job()

while True:
    schedule.run_pending()

    time.sleep(1)
