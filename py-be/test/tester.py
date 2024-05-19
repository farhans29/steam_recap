import requests

def test_get_genres():
    url = 'http://localhost:5000/api/genre/get'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Print the response status code
        print(f"Status Code: {response.status_code}")
        
        # Print the JSON response
        genres = response.json()
        print("Genres:", len(genres[0]['genre_titles']))
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTP error
    except Exception as err:
        print(f"An error occurred: {err}")  # Other errors

if __name__ == "__main__":
    test_get_genres()
