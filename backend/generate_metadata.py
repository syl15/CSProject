# OpenRouter limits: 20 requests/minute, 200 requests/day 
# TODO: Add retry logic on failure

import os, requests, re, json
from datetime import datetime
from collections import OrderedDict


def parse_llm_response(response): 
    """
    Parses and cleans LLM response JSON, stripping any markdown/formatting.
    Returns a Python dictionary if valid, else None
    """

    try: 
        raw_response = response.json()["choices"][0]["message"]["content"]

        if raw_response.strip().startswith("```"):
            raw_response = re.sub(r"^```(?:json)?|```$", "", raw_response.strip(), flags=re.MULTILINE).strip()

        return json.loads(raw_response)

    except (KeyError, json.JSONDecodeError):
        return None

def validate_metadata(metadata): 
    """
    Checks LLM generated metadata to validate: 
    - All required keys exists 
    - Data types are correct
    - Latitude and longtiude are in within valid ranges 
    - Latitude/longitude have up to 6 decimal places 
    - Radius is positive 

    Returns True if valid, False otherwise
    """

    required_keys = ["disaster_name", "summary", "disaster_location", "location", "start_date"]

    if not isinstance(metadata, dict): 
        print("Not a dict")
        return False 

    for key in required_keys:
        if key not in metadata: 
            print(f"Missing key: {key}")
            return False 
    
    if not isinstance(metadata["disaster_name"], str):
        print("disaster_name not a string")
        return False 
    
    if not isinstance(metadata["disaster_location"], str):
        print("summary not a string")
        return False 
    
    if not isinstance(metadata["start_date"], str): 
        print("start_date is not a string")
        return False 
    
    try: 
        datetime.strptime(metadata["start_date"], "%Y-%m-%d")
    except ValueError:
        print(f"start_date {metadata["start_date"]} is not in YYYY-MM-DD format")
        return False 
    
    location = metadata["location"]
    if not isinstance(location, dict):
        print("location is not a dict")
        return False
    
    if not all(key in location for key in ["latitude", "longitude", "radius"]):
        print("Missing one of latitude, longitude, or radius")
        return False
    
    try: 
        latitude = float(location.get("latitude"))
        longitude = float(location.get("longitude"))
        radius = float(location.get("radius"))
    except (TypeError, ValueError): 
        print("latitude/longitude/radius could not be converted to float")
        return False 

    if not (-90 <= latitude <= 90): 
        print(f"latitude {latitude} out of range")
        return False 
    
    if not (-180 <= longitude <= 180): 
        print(f"longitude {longitude} out of range")
        return False 
    
    if radius <= 0: 
        print(f"radius {radius} is not positive")
        return False 
    
    return True 

def format_metadata(metadata): 
    """
    Ensure consistent key ordering 
    Returns OrderedDict for JSON serialization
    """

    # Fix precision to 6 decimal places and convert to string
    latitude = float(metadata["location"]["latitude"])
    longitude = float(metadata["location"]["longitude"])
    radius = metadata["location"]["radius"]

    metadata["location"]["latitude"] = f"{latitude:.6f}"
    metadata["location"]["longitude"] = f"{longitude:.6f}"
    metadata["location"]["radius"] = f"{radius}"

    # Reorder and wrap as an OrderedDict 
    return OrderedDict([
        ("disaster_name", metadata["disaster_name"]),
        ("summary", metadata["summary"]),
        ("disaster_location", metadata["disaster_location"]),
        ("location", OrderedDict([
            ("latitude", metadata["location"]["latitude"]),
            ("longitude", metadata["location"]["longitude"]),
            ("radius", metadata["location"]["radius"]),
        ])),
        ("start_date", metadata["start_date"])
    ])



def generate_disaster_metadata(clusters): 
    """
    Prompts LLM to generate metadata about each cluster. 
    """

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}", 
        "Content-Type": "application/json"
    }

    results = [] 

    for index, cluster in enumerate(clusters): 
        approx_date = cluster["date"]
        posts = cluster["posts"]
        post_texts = "\n".join([f"{i+1}. {text}" for i, (_, text) in enumerate(posts)])

        prompt = f"""
            You are a metadata extraction assistant. 
            Given the following social media posts, generate structured metadata describing the disaster.
            Only use the information in these posts and do not rely on any outside knowledge or facts. 

            The approximate date of these posts is {approx_date}. 
            If no disaster start date is explicitly mentioned in the posts, use this as the inferred start date. 
            If you must infer a date, assume the current year is 2025. Do not guess or default to 2023.
            
            Generate a "disaster_name" in the format: "<City or Country> <Disaster Type>", 
            e.g. "Myanmar Earthquake", "Los Angeles Wildfire", etc. 

            Output constraints: 
            - Latitude must be between -90 and 90 (inclusive), with exactly six decimal places.
            - Longitude must be between -180 and 180 (inclusive), with exactly six decimal places.
            - Radius must be a positive number in meters

            Return ONLY a valid JSON object, nothing else. Do not include explanations, markdown formatting, or commentary. Do not wrap it in code blocks.

            Expected JSON format:
            - "disaster_name": string (a short descriptive title, e.g. "Los Angeles Wilfires", "Myanmar Earthquake")
            - "summary": string (3-4 sentences)
            - "disaster_location": string (city + country name if available, e.g. "Naypyidaw, Myanmar") 
            - "location":{{
                "latitude": float, 
                "longitude": float, 
                "radius": float
            }}
            - "start_date": string in YYYY-MM-DD format
        
            Posts:
            {post_texts}

        """
        # Model options: 
            # default: mistral/ministral-8b (stronger reasoning)
            # openchat: openchat/openchat-7b (more structured)
            
        data = {
            "model": "openchat/openchat-7b", 
            "temperature": 0,
            "messages": [
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        }

        # Post the response 
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

        print(f"\nCluster {index+1} status code: {response.status_code}")

        # Ensure the response is a valid json and all fields are present and in correct format
        parsed_response = parse_llm_response(response)
        if parsed_response and validate_metadata(parsed_response): 
            ordered_metadata = format_metadata(parsed_response)
            print(json.dumps(ordered_metadata, indent=2, ensure_ascii=False)) 
            results.append(ordered_metadata)
        else: 
            print("Failed to parse a valid JSON.") 
            try: 
                print(response.json()["choices"][0]["message"]["content"])
            except: 
                print(response.text)
            results.append({"error": True, "raw_response": response.text})
        
    return results


if __name__ == "__main__":
    # Clusters are in format cluster = {date: "YYYY-MM-DD", posts: [("post_id", "post_text")]}

    # Mock generated data
    la_wildfires = {
        "date": "2025-01-10",
        "posts": [
            ("post_001", "Smoke everywhere in Santa Clarita. Is there a fire?"),
            ("post_002", "Helicopters overhead dropping water—classic LA wildfire season."),
            ("post_003", "My cousin just evacuated from near Angeles National Forest."),
            ("post_004", "Can’t see the sun this morning, air quality's awful."),
            ("post_005", "Brush fire near 210 freeway. Firefighters on scene."),
            ("post_006", "Hope this doesn't get like 2020 again..."),
            ("post_007", "LA County alert just came in about high winds and fire risk."),
            ("post_008", "Friends near Burbank say there's ash on their cars."),
            ("post_009", "Red flag warning extended through the weekend."),
            ("post_010", "Power outages reported near Pasadena, maybe from fire lines?")
        ]
    }

    armenia_floods = {
        "date": "2024-04-22",
        "posts": [
            ("post_001", "Streets in Yerevan are completely underwater after last night’s rain."),
            ("post_002", "No school today. Our whole neighborhood is flooded."),
            ("post_003", "Heard Syunik province got hit worst by the floods."),
            ("post_004", "People being rescued by boats in some parts of the city."),
            ("post_005", "Heavy rainfall warning had been issued but this is worse than expected."),
            ("post_006", "Cars floating down the road in videos. Crazy."),
            ("post_007", "Volunteers organizing relief supplies on Baghramyan Ave."),
            ("post_008", "Is this climate change or what?"),
            ("post_009", "Bridge collapsed near Vanadzor. Hope no one was hurt."),
            ("post_010", "Electricity is out in parts of the capital.")
        ]
    }

    tibet_earthquake = {
        "date": "2025-02-03",
        "posts": [
            ("post_001", "Felt a strong shake this morning in Lhasa."),
            ("post_002", "My building swayed for 10 seconds, thought it was just wind."),
            ("post_003", "Quake hit 6.5 magnitude, epicenter near Nyingchi."),
            ("post_004", "Temples damaged. Some walls cracked."),
            ("post_005", "Still aftershocks in the evening."),
            ("post_006", "People are scared to go back indoors."),
            ("post_007", "Emergency crews heading to rural villages."),
            ("post_008", "I thought it was construction work until the whole floor moved."),
            ("post_009", "No internet in some areas."),
            ("post_010", "Please donate to local rescue teams. Supplies needed urgently.")
        ]
    }

    mock_clusters = [la_wildfires, armenia_floods, tibet_earthquake]

    # Manually clustered from temp_bluesky
    myanmar_earthquake = {
        "date": "2025-04-04", 
        "posts": [
            ("3llxi5sfidd2g", "@Reuters: United Nations aid chief Tom Fletcher will arrive in earthquake devastated Myanmar on Friday, said U.N. Secretary-General Antonio Guterres as he appealed for more international funding and rapid, unimpeded aid access in the country.  https://t.co/i1dYgkMR1B"), 
            ("3llxi7n65mc2u", "Thiri, a Burmese media expert, exposes the devastating toll of Myanmar’s 7.7 magnitude earthquake, from the staggering loss of life to the military’s obstruction of aid.“We just want to live in peace,” Thiri says.Hear the urgent call for action: insightmyanmar.org/complete-sho..."), 
            ("3llxiivagek2u", "Myanmar’s fractured governance hampers earthquake aid. The junta weaponizes relief, while EAOs & civil groups struggle with resources. With monsoon season looming, urgent support is needed. Listen to the discussion: insightmyanmar.org/complete-sho...GoFundMe: gofund.me/2d4fcbcf"), 
        ]
    }

    ollague_earthquake = {
        "date": "2025-03-24", 
        "posts": [
            ("3llxio3wddr2k", "On 2025-03-24, at 01:26:13 (UTC), there was an earthquake around southern Mid-Atlantic Ridge. The depth of the hypocenter is about 10.0km, and the magnitude of the earthquake is estimated to be about 4.6.nagix.github.io/world-eq-loc..."),
            ("3llxiza7rje2", "🌍 Earthquake Alert: Magnitude 4.3 quake 50 km W of Ollagüe, Chile. Earthquake time: 4/4/2025, 3:07:51 AM."), 
            ("3llxiwut5ml2v", "New earthquake reported: M 4.3 - 50 km W of Ollagüe, Chile - 2025-04-04T03:44:49.040Z"), 
            ("3llxivs57us2l", "🌍 Earthquake Alert 🌍📍 Location: 50 km W of Ollagüe, Chile📏 Magnitude (mb): 4.3🔽 Depth: 121.35 km⏰ Time: 2025-04-04 03:07:51 UTC🔗 Source: USGSStay safe!")
      ]
    }

    self_clustered = [myanmar_earthquake, ollague_earthquake]
    results = generate_disaster_metadata(self_clustered) 

    print("\nFinal Results:")
    print(json.dumps(results, indent=2, ensure_ascii=False))