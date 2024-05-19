from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

def fetch_data(api_url):
    data = []
    while api_url:
        response = requests.get(api_url)
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            break
        response_data = response.json()
        if 'data' in response_data and 'data' in response_data['data']:
            for item in response_data['data']['data']:
                if isinstance(item, dict) and 'response' in item and 'source' in item:
                    data.append(item)
            api_url = response_data['data'].get('next_page_url')  # Update for next page URL
        else:
            print("Key 'data' not found in the response")
            break
    return data

def get_citations(response_text, sources):
    citations = []
    for source in sources:
        if source['link']:
            citations.append({"id": source['id'], "link": source['link']})
    return citations

def main(api_url):
    data = fetch_data(api_url)
    result = []
    for item in data:
        response_text = item['response']
        sources = item.get('source', [])  # Safely get 'source' key
        citations = get_citations(response_text, sources)
        result.append({'citations': citations})
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_citations')
def get_citations_route():
    api_url = 'https://devapi.beyondchats.com/api/get_message_with_sources'
    result = main(api_url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
