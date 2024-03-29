<div align="center">

![Duolingo Logo](duolingo.png)

<h1>Duolingo API Dockerized</h1>

Serves your Duolingo progress info as JSON.

Based on [KartikTalwar/Duolingo](https://github.com/KartikTalwar/Duolingo), utilizing modifications from [lidiaCirrone/pw-duolingo-data](https://github.com/lidiaCirrone/pw-duolingo-data).

![GitHub release](https://img.shields.io/github/v/release/marvinscham/duolingo-api-dockerized)
[![Quality Gate Status](https://sonar.ms-ds.org/api/project_badges/measure?project=Duolingo-API-Dockerized&metric=alert_status&token=sqb_d0fa0ab8bdae8eda3db5414f9483e03e91034da3)](https://sonar.ms-ds.org/dashboard?id=Duolingo-API-Dockerized)

</div>

## Example Setup

See `example.docker-compose.yml`. You'll need to provide your own `docker-compose.yml`, which you can base on this example file.

In case you'd like to run this behind a nginx reverse proxy, you can use `nginx.conf` as a reference.

```yml
version: '3.2'

# e.g. reverse proxy network
networks:
  yourNetwork:
    external: true

services:
  duolingo-data:
    image: ghcr.io/marvinscham/duolingo-api-dockerized:latest
    container_name: duolingo-data
    restart: unless-stopped
    environment:
      - TIMEZONE=Europe/Berlin
      - DUO_USERNAME=yourUsername
      - DUO_JWT=yourJWT
      - XP_SUMMARY_DAYS=30
      - UPDATE_INTERVAL=15
      - MAX_RETRIES=3
    # ports:
    #   - 80:7000
    networks:
      - yourNetwork
```

This will serve your progress info at `https://duo.your-domain.com/duo_user_info.json`.

## Environment Variables

- `TIMEZONE`
  - Relevant for determining which lessons belong to which day
  - Default: `Europe/Berlin`
- `DUO_USERNAME`
  - Required for login
- `DUO_JWT`
  - Login token (**Not your password!** Info on obtaining this is in the following segment)
- `XP_SUMMARY_DAYS`
  - Number of past days to get data from. _Might stop working properly if > 300_
  - Default: `30`
- `UPDATE_INTERVAL`
  - Time in minutes to request fresh data from Duolingo
  - Default: `15`
- `MAX_RETRIES`
  - How often the app should retry in case of some connection error (retry interval 60 seconds)
  - Default: `3`

## Grabbing your JWT

Login on [Duolingo](duolingo.com) and run the following JavaScript in your browser console. The returned string is your JWT. Do not share this token as it will allow anyone to access your Duolingo account.

```js
document.cookie.match(new RegExp('(^| )jwt_token=([^;]+)'))[0].slice(11);
```

The token currently does not expire but will break if you change your Duolingo password.
