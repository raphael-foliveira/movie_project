import requests
from keys import tmdb_api, access_token

tmdb_endpoint = "https://api.themoviedb.org/3/search/movie"


def find_movie(movie_title):
    headers = {
        "Authorization": access_token
    }
    params = {
        "api_key": tmdb_api,
        "query": movie_title
    }

    data = requests.get(tmdb_endpoint, headers=headers, params=params)
    print(data.json())
    results = data.json()["results"][0]
    original_title = results["original_title"]
    description = results["overview"]
    year = results["release_date"][:4]
    img_url = f"https://image.tmdb.org/t/p/w500{results['poster_path']}"
    rating = results["vote_average"]
    movie_data = [original_title, year, description, rating, img_url]
    return movie_data