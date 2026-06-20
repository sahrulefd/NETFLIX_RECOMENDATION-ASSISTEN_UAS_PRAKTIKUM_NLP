import streamlit as st
from workflow import recommend_movies

st.set_page_config(
    page_title="Netflix Recommendation Assistant",
    page_icon="https://img.icons8.com/?size=100&id=Ioap5V1DjU3F&format=png&color=000000",
    layout="wide"
)

st.title("Netflix Recommendation Assistant")
st.write(
    "Sistem rekomendasi film dan serial Netflix menggunakan "
    "LangChain, LangGraph, dan LangSmith."
)

st.markdown("---")

user_input = st.text_input(
    "Masukkan preferensi tontonan:",
    placeholder="Contoh: Saya suka film action dan horror"
)

if st.button("Cari Rekomendasi"):
    
    if not user_input:
        st.warning("Silakan masukkan preferensi terlebih dahulu.")
    
    else:
        with st.spinner("Mencari rekomendasi..."):
            recommendations = recommend_movies(user_input)

        st.success("Rekomendasi ditemukan!")

        st.subheader("Hasil Rekomendasi")

        if len(recommendations) == 0:
            st.error("Tidak ditemukan film yang sesuai.")
        else:
            for i, movie in enumerate(recommendations, start=1):
                st.markdown(f"### {i}. {movie['title']}")
                st.write(f"**Tipe:** {movie['type']}")
                st.write(f"**Genre:** {movie['listed_in']}")
                st.write(f"**Deskripsi:** {movie['description']}")
                st.markdown("---")