from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)
CORS(app)

def scrape_linkedin_company(company_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        time.sleep(2)  # تأخير لتجنب الحظر
        response = requests.get(company_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        company_data = {
            "name": (soup.find("h1", class_="org-top-card-summary__title") or {}).get_text(strip=True) or "N/A",
            "industry": (soup.find("div", class_="org-top-card-summary__industry") or {}).get_text(strip=True) or "N/A",
            "size": (soup.find("div", class_="org-top-card-summary__size") or {}).get_text(strip=True) or "N/A",
            "location": (soup.find("div", class_="org-top-card-summary__location") or {}).get_text(strip=True) or "N/A"
        }
        
        return company_data
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch data: {str(e)}"}

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    company_url = data.get('company_url')
    
    if not company_url:
        return jsonify({"error": "Company URL is required"}), 400
    
    result = scrape_linkedin_company(company_url)

import json
with open('company_data.json', 'a') as f:
    json.dump(result, f, ensure_ascii=False)
    f.write('\n')
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
