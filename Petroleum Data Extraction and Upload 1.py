{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "331ac311-cdc0-428a-8e1b-ad9f04e1a7a5",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "📦 Downloading ZIP...\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\EDISON\\AppData\\Local\\anaconda3\\Lib\\site-packages\\urllib3\\connectionpool.py:1099: InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.erb.org.zm'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings\n",
      "  warnings.warn(\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "🧵 Extracting ZIP contents...\n",
      "🔐 Encoding file...\n",
      "📤 Uploading to GitHub...\n",
      "✅ Upload complete!\n"
     ]
    }
   ],
   "source": [
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
    "# 🔐 Use your personal GitHub token\n",
    "import os\n",
    "GITHUB_TOKEN = os.getenv(\"GITHUB_TOKEN\")  # ✅ This is safe\n",
    "                                                                  # Toby Personal Access Token Here\n",
    "\n",
    "\n",
    "# --- STEP 1: Download ZIP ---\n",
    "print(\"📦 Downloading ZIP...\")\n",
    "response = requests.get(ZIP_URL, verify=False)  # Set verify=True in production\n",
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
   "id": "edad488c-0d41-4e40-8cca-ded2ae1b1e96",
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
