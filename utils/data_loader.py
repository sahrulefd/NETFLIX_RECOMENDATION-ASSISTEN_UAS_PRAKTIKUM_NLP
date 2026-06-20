import pandas as pd


def load_netflix_data(file_path="data/netflix_titles.csv"):
    """
    Membaca dan membersihkan dataset Netflix.

    Parameters
    ----------
    file_path : str
        Lokasi file CSV Netflix.

    Returns
    -------
    pandas.DataFrame
        Dataset yang sudah dibersihkan.
    """

    try:
        df = pd.read_csv(file_path)

        # Kolom yang akan digunakan
        required_columns = [
            "title",
            "type",
            "listed_in",
            "description"
        ]

        # Pastikan kolom tersedia
        missing_columns = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Kolom tidak ditemukan: {missing_columns}"
            )

        # Bersihkan data kosong
        df["title"] = df["title"].fillna("Unknown Title")
        df["type"] = df["type"].fillna("Unknown Type")
        df["listed_in"] = df["listed_in"].fillna("")
        df["description"] = df["description"].fillna("No Description")

        return df

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Dataset tidak ditemukan pada path: {file_path}"
        )


def get_movies_by_genres(df, genres, limit=5):
    """
    Mengambil rekomendasi film berdasarkan genre.

    Parameters
    ----------
    df : pandas.DataFrame
    genres : list
    limit : int

    Returns
    -------
    list
    """

    filtered_df = df.copy()

    for genre in genres:

        filtered_df = filtered_df[
            filtered_df["listed_in"].str.contains(
                genre,
                case=False,
                na=False
            )
        ]

    results = filtered_df.head(limit)

    recommendations = []

    for _, row in results.iterrows():

        recommendations.append({
            "title": row["title"],
            "type": row["type"],
            "listed_in": row["listed_in"],
            "description": row["description"]
        })

    return recommendations


# Testing
if __name__ == "__main__":

    df = load_netflix_data()

    print("Jumlah Data:")
    print(len(df))

    print("\nContoh Data:")
    print(df.head())