# get_crowdstrike_mtc_token

Generate a CrowdStrike Falcon **maintenance (MTC) uninstall token** for a specific sensor using the Falcon API (`reveal-uninstall-token`).

## Prerequisites

- **Python 3.10+**
- A CrowdStrike Falcon **API OAuth2 client** with permission to call the reveal uninstall token API (see [CrowdStrike documentation](https://supportportal.crowdstrike.com/s/article/ka16T000000wt8AQAQ); portal access may require a CrowdStrike account)
- The sensor **device ID** (`aid`) for the host you are uninstalling from

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/scnetter/get_crowdstrike_mtc_token.git
cd get_crowdstrike_mtc_token
```

### 2. Install dependencies

**Option A — [uv](https://docs.astral.sh/uv/) (recommended; repo includes `uv.lock`):**

```bash
uv sync
```

**Option B — pip + venv:**

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
# or: pip install python-dotenv requests
```

### 3. Configure credentials

```bash
cp .env.example .env
```

Edit `.env` with your Falcon API client ID, client secret, and API base URL. **Do not commit `.env`** — it is gitignored.

| Variable | Description |
|----------|-------------|
| `CROWDSTRIKE_CLIENT_ID` | OAuth2 API client ID |
| `CROWDSTRIKE_CLIENT_SECRET` | OAuth2 API client secret |
| `CROWDSTRIKE_BASE_URL` | Falcon API host for your cloud (must match your tenant) |

Example base URLs (use the host for your Falcon cloud):

| Cloud | `CROWDSTRIKE_BASE_URL` |
|-------|-------------------------|
| US-1 | `https://api.crowdstrike.com` |
| US-2 | `https://api.us-2.crowdstrike.com` |
| EU-1 | `https://api.eu-1.crowdstrike.com` |
| US-GOV-1 | `https://api.laggar.gcw.crowdstrike.com` |

Wrong base URL often causes authentication or API errors even with valid credentials.

### 4. Get the device ID

On the **target host**, run the command for its OS. The value is labeled `aid`, `agentID`, or `AG` depending on platform.

**Windows:**

```cmd
reg query HKLM\System\CurrentControlSet\services\CSAgent\Sim\ /f AG
```

**macOS:**

```bash
sudo /Applications/Falcon.app/Contents/Resources/falconctl stats | grep agentID
```

**Linux:**

```bash
sudo /opt/CrowdStrike/falconctl -g --aid
```

### 5. Run the script

From the project directory (with the virtual environment activated if you used one):

```bash
# with uv
uv run python get_crowdstrike_mtc_token.py <device_id>

# or with python directly
python get_crowdstrike_mtc_token.py <device_id>
```

Example:

```bash
python get_crowdstrike_mtc_token.py a1b2c3d4e5f6...
```

On success, the script prints authentication confirmation and the **MTC uninstall token**. Treat that token as sensitive; use it only for the intended uninstall workflow.

## CrowdStrike documentation

- [Support article (linked from this project)](https://supportportal.crowdstrike.com/s/article/ka16T000000wt8AQAQ)

## Troubleshooting

| Symptom | Things to check |
|---------|------------------|
| `Missing required environment variables` | `.env` exists in the project root; all three variables are set (no `YOUR_*` placeholders left) |
| Authentication failed (401/403) | Client ID/secret; API client scopes; base URL matches your Falcon cloud |
| Token request failed | Device ID correct for that tenant; sensor still reporting; API permissions for reveal uninstall token |
| `Device ID is required` | Pass device ID as the first argument: `python get_crowdstrike_mtc_token.py <device_id>` |

## Security notes

- Never commit `.env` or share client secrets / MTC tokens in chat or tickets.
- Rotate API credentials if a secret is exposed.
- Run this only from trusted machines; the output allows sensor uninstallation when used with CrowdStrike’s process.
