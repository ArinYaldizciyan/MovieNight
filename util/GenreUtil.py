from datetime import datetime


def readable_genre(genre_ids):
    genres = {
        28: "Action",
        12: "Adventure",
        16: "Animation",
        35: "Comedy",
        80: "Crime",
        99: "Documentary",
        18: "Drama",
        10751: "Family",
        14: "Fantasy",
        36: "History",
        27: "Horror",
        10402: "Music",
        9648: "Mystery",
        10749: "Romance",
        878: "Science Fiction",
        10770: "TV Movie",
        53: "Thriller",
        10752: "War",
        37: "Western"
    }

    genre_list = []
    for genre in genre_ids:
        genre_list.append(genre["name"])
    genre_string = ', '.join(genre_list)
    return genre_list, genre_string


def readable_date(date):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%B %dth, %Y")
    return formatted_date
