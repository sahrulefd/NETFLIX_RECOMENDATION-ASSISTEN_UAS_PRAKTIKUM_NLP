from typing import TypedDict, List, Dict

from langgraph.graph import StateGraph, END

from chains.recommendation_chain import extract_genres
from utils.data_loader import (
    load_netflix_data,
    get_movies_by_genres
)

# ==================================
# LOAD DATASET SEKALI SAAT APLIKASI DIMULAI
# ==================================

df = load_netflix_data()


# ==================================
# STATE LANGGRAPH
# ==================================

class RecommendationState(TypedDict):
    user_input: str
    genres: List[str]
    recommendations: List[Dict]


# ==================================
# NODE 1
# EKSTRAK GENRE DARI INPUT USER
# ==================================

def genre_extraction_node(state: RecommendationState):

    genres = extract_genres(
        state["user_input"]
    )

    return {
        "genres": genres
    }


# ==================================
# NODE 2
# CARI FILM BERDASARKAN GENRE
# ==================================

def movie_search_node(state: RecommendationState):

    genres = state["genres"]

    recommendations = get_movies_by_genres(
        df=df,
        genres=genres,
        limit=5
    )

    return {
        "recommendations": recommendations
    }


# ==================================
# MEMBANGUN LANGGRAPH WORKFLOW
# ==================================

graph = StateGraph(RecommendationState)

graph.add_node(
    "genre_extraction",
    genre_extraction_node
)

graph.add_node(
    "movie_search",
    movie_search_node
)

graph.set_entry_point(
    "genre_extraction"
)

graph.add_edge(
    "genre_extraction",
    "movie_search"
)

graph.add_edge(
    "movie_search",
    END
)

recommendation_graph = graph.compile()


# ==================================
# FUNGSI UNTUK APP.PY
# ==================================

def recommend_movies(user_input: str):

    result = recommendation_graph.invoke(
        {
            "user_input": user_input,
            "genres": [],
            "recommendations": []
        }
    )

    return result["recommendations"]


# ==================================
# TESTING
# ==================================

if __name__ == "__main__":

    user_input = (
        "Saya suka film action dan sci-fi"
    )

    recommendations = recommend_movies(
        user_input
    )

    print("\nRekomendasi Film:\n")

    for idx, movie in enumerate(
        recommendations,
        start=1
    ):
        print(
            f"{idx}. {movie['title']}"
        )
        print(
            f"   Type : {movie['type']}"
        )
        print(
            f"   Genre: {movie['listed_in']}"
        )
        print(
            f"   Description: {movie['description']}"
        )
        print()