<div align="center">
    
![Duolingo Logo](https://github.com/marvinscham/schmoekerei-icons/blob/main/icons/duolingo.png)
    
<h1>Duolingo Data</h1>

Duolingo Data is a Python-based Docker image which allows you to set up a basic JSON API to get cached data from.

</div>
    
## Example Setup

See example.docker-compose.yml. You'll need to provide your own docker-compose.yml, which you can base on this example file.

    version: '3.2'

    # e.g. swag reverse proxy network
    networks:
      yourNetwork:
        external: true

    services:
      duolingo-data:
        build: .
        container_name: duolingo-data
        restart: unless-stopped
        environment:
          - TIMEZONE=Europe/Berlin
          - DUO_USERNAME=yourUsername
          - DUO_PASSWORD=yourPassword
          - SERVER_URL=https://your-domain.com
          - XP_SUMMARY_DAYS=30
          - UPDATE_INTERVAL=15
          - MAX_RETRIES=3
        # ports:
        #   - 80:7000
        networks:
          - yourNetwork

## Environment Variables

- `TIMEZONE`
  - Relevant for determining which lessons belong to which day
  - Default: `Europe/Berlin`
- `DUO_USERNAME`
  - Required for login
- `DUO_PASSWORD`
  - Required for login
- `SERVER_URL`
  - Used for connectivity self check
  - Example: `https://your-domain.com` → no trailing slash!
- `XP_SUMMARY_DAYS`
  - Number of past days to get data from. Might stop working properly if > 300
  - Default: `30`
- `UPDATE_INTERVAL`
  - Time in minutes to request fresh data from Duolingo
  - Default: `15`
- `MAX_RETRIES`
  - How often the app should retry in case of some connection error (retry interval 60 seconds)
  - Default: `3`
