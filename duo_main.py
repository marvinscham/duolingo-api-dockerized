import json, sys, time
import duolingo
from datetime import datetime
from duo_settings import duo_user_name, duo_user_password

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
userid = user_total_info["id"]
learning_language_abbr = user_total_info["learningLanguage"]

user_date_timestamp = user_total_info["creationDate"]
user_date_str = datetime.fromtimestamp(user_date_timestamp).strftime("%d/%m/%Y")

language_progress = duo_user.get_language_progress(learning_language_abbr)

user_object = {
    "username": username,
    "streak": language_progress["streak"],
    "xp": user_total_info["totalXp"],
    "creation_date": user_date_str,
    "learning_language": language_progress["language_string"],
    "timestamp": str(int(time.time())),
}

lang_data = duo_user.get_all_languages()
str_user = json.dumps(user_object, indent=4)
str_lang = json.dumps(lang_data, indent=4)

if len(str_user) < 10 or len(str_lang) < 10:
    print("error...")
    sys.exit()
else:
    f = open("duo_user_info.json", "w")
    f.write(str_user)
    f.close()
    print("wrote user info")

    f = open("duo_lang_info.json", "w")
    f.write(str_lang)
    f.close()
    print("wrote lang info")
