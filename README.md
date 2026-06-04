# get_crowdstrike_mtc_token - Generate a crowdstrike MTC token using the swagger API

## TODOs
* Create actual README with instructions
* Add links to Crowdstrike Documentation (with requirement to have accounts to access)
* ~~Template for .env~~ — use `.env.example` (see Setup below)
* pip install instructions

Crowdstrike Documentation: https://supportportal.crowdstrike.com/s/article/ka16T000000wt8AQAQ

## Setup

1. Copy the environment template and fill in your values:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your Falcon API client ID, client secret, and base URL. `.env` is gitignored; `.env.example` is safe to commit.

## Environment variables

| Variable | Description |
|----------|-------------|
| `CROWDSTRIKE_CLIENT_ID` | OAuth2 API client ID |
| `CROWDSTRIKE_CLIENT_SECRET` | OAuth2 API client secret |
| `CROWDSTRIKE_BASE_URL` | Falcon API host (e.g. `https://api.crowdstrike.com`) |