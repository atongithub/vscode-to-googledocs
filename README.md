# Formats and inserts Java Code to Google Docs 

A Python script that formats Java code with styles (monospace font, shading, etc.) and inserts it into a Google Docs document using the Google Docs API.

## Features

- Parses and reads local `.java` files
- Authenticates with Google Docs API using a service account
- Inserts formatted code into a Google Docs file
- Applies:
  - Monospace font (`Courier New`)
  - Background shading
  - Custom paragraph styles

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/atongithub/vscode-to-googledocs.git
cd vscode-to-googledocs
```

### 2. Install libraries
```bash
pip install -r requirements.txt
```

### 3. Google Cloud Setup

To set up Google Docs API access:
1. Go to [Google Cloud Console](https://console.cloud.google.com/) and create a **New Project**
2. Go to API's and Services > In the search bar Enable the **Google Docs API**
3. Go to IAM & Admin
4. Under the **Service Account** Section create a Service Account with the Editor Role
5. Go to the newly created service account > Keys > Create Key (JSON) 
6. Download the JSON credentials
7. Place the credentials file in the same directory as the script and rename it as `credentials.json`


