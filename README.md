# FishingBooker QA Automation Task

This project contains automated UI tests written in Python, using Playwright and PyTest, as part of a QA Junior Automation Engineer assignment.

## Tech stack

- Python
- Playwright (sync API)
- PyTest

## Setup

1. Clone the repository
2. Install dependencies:
```
pip install -r requirements.txt
```

3. Install Playwright browsers:
```
playwright install
```

## Environment variables

The tested environment is protected by Basic Authentication.
Credentials are provided in the task description PDF and should be set as environment variables.

Set the following variables before running the tests:
```
FB_USERNAME=<your_username>
FB_PASSWORD=<your_password>
```

### Windows (PowerShell)
```
$env:FB_USERNAME="your_username"
$env:FB_PASSWORD="your_password"
```

### macOS / Linux
```
export FB_USERNAME="your_username"
export FB_PASSWORD="your_password"
```

## Running tests

Run all tests with:
```
pytest
```