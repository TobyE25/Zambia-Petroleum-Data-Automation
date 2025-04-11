{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "9f7f650d-6797-4322-ad5f-c24daa2a5171",
   "metadata": {},
   "outputs": [
    {
     "ename": "Exception",
     "evalue": "❌ GITHUB_TOKEN is not set in environment variables.",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mException\u001b[0m                                 Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[1], line 19\u001b[0m\n\u001b[0;32m     17\u001b[0m GITHUB_TOKEN \u001b[38;5;241m=\u001b[39m os\u001b[38;5;241m.\u001b[39mgetenv(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mGITHUB_TOKEN\u001b[39m\u001b[38;5;124m\"\u001b[39m)\n\u001b[0;32m     18\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m GITHUB_TOKEN:\n\u001b[1;32m---> 19\u001b[0m     \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mException\u001b[39;00m(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124m❌ GITHUB_TOKEN is not set in environment variables.\u001b[39m\u001b[38;5;124m\"\u001b[39m)\n\u001b[0;32m     21\u001b[0m \u001b[38;5;66;03m# --- STEP 1: Download ZIP ---\u001b[39;00m\n\u001b[0;32m     22\u001b[0m \u001b[38;5;28mprint\u001b[39m(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124m📦 Downloading ZIP...\u001b[39m\u001b[38;5;124m\"\u001b[39m)\n",
      "\u001b[1;31mException\u001b[0m: ❌ GITHUB_TOKEN is not set in environment variables."
     ]
    }
   ],
   "source": [
    "#This code is for use in github\n",
    "\n",
    "import requests\n",
    "import zipfile\n",
    "import os\n",
    "import base64\n",
    "from io import BytesIO\n",
    "\n",
    "# --- CONFIGURATION ---\n",
    "ZIP_URL = \"https://www.erb.org.zm/wp-content/uploads/files/ips2023.zip\"\n",
    "EXTRACT_DIR = \"extracted\"\n",
    "REPO = \"TobyE25/Zambia-Petroleum-Data-Automation\"\n",
    "BRANCH = \"main\"\n",
    "TARGET_PATH = \"data/petroleum_stats.xlsm\"\n",
    "\n",
    "# Load GitHub token from environment (set in GitHub Actions secrets)\n",
    "GITHUB_TOKEN = os.getenv(\"GITHUB_TOKEN\")\n",
    "if not GITHUB_TOKEN:\n",
    "    raise Exception(\"❌ GITHUB_TOKEN is not set in environment variables.\")\n",
    "\n",
    "# --- STEP 1: Download ZIP ---\n",
    "print(\"📦 Downloading ZIP...\")\n",
    "response = requests.get(ZIP_URL, verify=False)\n",
    "if response.status_code != 200:\n",
    "    raise Exception(f\"❌ Failed to download ZIP: {response.status_code}\")\n",
    "\n",
    "# --- STEP 2: Extract ZIP ---\n",
    "print(\"🧵 Extracting ZIP contents...\")\n",
    "os.makedirs(EXTRACT_DIR, exist_ok=True)\n",
    "with zipfile.ZipFile(BytesIO(response.content)) as z:\n",
    "    z.extractall(EXTRACT_DIR)\n",
    "\n",
    "# --- STEP 3: Find the .xlsm file ---\n",
    "xlsm_files = [f for f in os.listdir(EXTRACT_DIR) if f.endswith(\".xlsm\")]\n",
    "if not xlsm_files:\n",
    "    raise Exception(\"❌ No .xlsm file found in the ZIP.\")\n",
    "xlsm_file = xlsm_files[0]\n",
    "xlsm_path = os.path.join(EXTRACT_DIR, xlsm_file)\n",
    "\n",
    "# --- STEP 4: Encode for GitHub upload ---\n",
    "print(\"🔐 Encoding file...\")\n",
    "with open(xlsm_path, \"rb\") as f:\n",
    "    encoded_content = base64.b64encode(f.read()).decode()\n",
    "\n",
    "# --- STEP 5: Prepare GitHub API call ---\n",
    "api_url = f\"https://api.github.com/repos/{REPO}/contents/{TARGET_PATH}\"\n",
    "headers = {\"Authorization\": f\"token {GITHUB_TOKEN}\"}\n",
    "\n",
    "# Check if the file already exists\n",
    "existing = requests.get(api_url, headers=headers)\n",
    "payload = {\n",
    "    \"message\": \"🚀 Auto update of petroleum stats\",\n",
    "    \"content\": encoded_content,\n",
    "    \"branch\": BRANCH\n",
    "}\n",
    "if existing.status_code == 200:\n",
    "    payload[\"sha\"] = existing.json()[\"sha\"]\n",
    "\n",
    "# --- STEP 6: Upload to GitHub ---\n",
    "print(\"📤 Uploading to GitHub...\")\n",
    "res = requests.put(api_url, headers=headers, json=payload)\n",
    "\n",
    "# --- STEP 7: Status Output ---\n",
    "if res.ok:\n",
    "    print(\"✅ Upload complete!\")\n",
    "else:\n",
    "    print(f\"❌ Upload failed: {res.json()}\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "dd895258-83ad-4555-b5f2-3f2958f6a619",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
