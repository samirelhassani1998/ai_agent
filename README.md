# IT Strategy Updates WhatsApp Agent

This project contains a simple Python script that fetches recent
articles from selected IT strategy consulting sources, summarizes them
using a free open source language model, and sends the summaries to a
WhatsApp number via Twilio.

## Requirements

- Python 3.8+
- Packages listed in `requirements.txt`
- A Twilio account with WhatsApp API access (for sending messages)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Set the following environment variables before running the script:

- `TWILIO_ACCOUNT_SID` – your Twilio Account SID
- `TWILIO_AUTH_TOKEN` – your Twilio Auth Token
- `TWILIO_WHATSAPP_FROM` – the WhatsApp-enabled Twilio number (e.g. `whatsapp:+14155238886`)
- `WHATSAPP_TO` – your WhatsApp number (e.g. `whatsapp:+33600000000`)

## Usage

Run the agent manually:

```bash
python agent.py
```

To execute it daily, schedule it with `cron` or another job scheduler.

## Notes

The script stores processed article URLs in `seen_urls.txt` to avoid
sending duplicate updates.

