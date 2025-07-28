import requests

def extract_filters(query, openrouter_api_key):
    prompt = f"""
Extract the structured clinical trial filters from the query below.
Return ONLY JSON with the fields: condition, phase, masking, location, age_group, sponsor.

Query: "{query}"
JSON:
"""
    headers = {
        "Authorization": f"Bearer {openrouter_api_key}"
    }

    data = {
        "model": "anthropic/claude-3-sonnet",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
    content = response.json()["choices"][0]["message"]["content"]

    # Safely eval JSON (or use json.loads if valid)
    import json
    try:
        return json.loads(content)
    except Exception:
        return {}

