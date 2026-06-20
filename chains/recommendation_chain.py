from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os


load_dotenv()
print("LANGCHAIN_PROJECT =", os.getenv("LANGCHAIN_PROJECT"))
print("LANGCHAIN_TRACING_V2 =", os.getenv("LANGCHAIN_TRACING_V2"))

# API Key Groq
os.environ["GROQ_API_KEY"] = "API_KEY_GROQ_KAMU"

# Inisialisasi model
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

# Prompt
prompt = PromptTemplate(
    input_variables=["user_preference"],
    template="""
Kamu adalah asisten rekomendasi Netflix.

Tugasmu adalah mengekstrak genre utama dari preferensi pengguna.

Contoh:

Input:
"Saya suka film action dan petualangan"

Output:
Action, Adventure

Input:
"Saya suka film lucu dan romantis"

Output:
Comedy, Romance

Sekarang analisis:

Input:
{user_preference}

Output:
"""
)

# Chain
chain = prompt | llm | StrOutputParser()


def extract_genres(user_preference: str):
    """
    Mengubah preferensi user menjadi genre Netflix.
    """

    result = chain.invoke({
        "user_preference": user_preference
    })

    genres = [
        genre.strip()
        for genre in result.split(",")
        if genre.strip()
    ]

    return genres


# Testing langsung
if __name__ == "__main__":
    test = "Saya suka film action dan sci-fi"

    genres = extract_genres(test)

    print("Genre hasil ekstraksi:")
    print(genres)