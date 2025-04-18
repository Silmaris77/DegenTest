import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from degen_details import degen_details
from questions import questions

# Konfiguracja strony
st.set_page_config(page_title="Degen Quiz", layout="centered")

# Stylizacja przycisków w sidebarze
st.markdown("""
<style>
section[data-testid="stSidebar"] .stRadio > div {
    flex-direction: column;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
    background-color: #f0f2f6;
    padding: 10px 16px;
    margin-bottom: 8px;
    border: 1px solid #ccc;
    border-radius: 6px;
    cursor: pointer;
    transition: 0.2s ease;
    height: 50px;
    display: flex;
    align-items: center;
    font-weight: 500;
    width: 100%;
    box-sizing: border-box;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
    background-color: #dce3ed;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-selected="true"] {
    background-color: #6cace4;
    color: white;
    border-color: #5a9bd6;
}
</style>
""", unsafe_allow_html=True)

# Inicjalizacja sesji
if "users" not in st.session_state:
    st.session_state.users = {"demo": "demo123"}
if "user" not in st.session_state:
    st.session_state.user = None
selected_page = None

# Ekran logowania
if st.session_state.user is None:
    st.title("🔐 Logowanie do DegenQuiz")
    menu = st.radio("Masz już konto?", ["🔓 Zaloguj się", "📝 Zarejestruj się"])

    if menu == "🔓 Zaloguj się":
        login_username = st.text_input("Login")
        login_password = st.text_input("Hasło", type="password")
        if st.button("Zaloguj się"):
            if login_username in st.session_state.users and st.session_state.users[login_username] == login_password:
                st.session_state.user = login_username
                st.success(f"Zalogowano jako: {login_username}")
                st.rerun()
            else:
                st.error("Niepoprawny login lub hasło.")

    if menu == "📝 Zarejestruj się":
        new_username = st.text_input("Nowy login")
        new_password = st.text_input("Nowe hasło", type="password")
        if st.button("Zarejestruj"):
            if new_username in st.session_state.users:
                st.warning("Taki użytkownik już istnieje.")
            elif not new_username or not new_password:
                st.warning("Wprowadź login i hasło.")
            else:
                st.session_state.users[new_username] = new_password
                st.success("Konto utworzone! Zaloguj się.")

# Po zalogowaniu
if st.session_state.user:
    st.sidebar.markdown(f"👤 Zalogowano jako: `{st.session_state.user}`")
    if st.sidebar.button("🚪 Wyloguj się"):
        st.session_state.user = None
        st.rerun()

    st.sidebar.title("🔍 Menu")
    main_nav = st.sidebar.radio("📂 Wybierz:", ["Strona główna (test)", "Typy degenów"])

    if main_nav == "Typy degenów":
        selected_page = st.sidebar.radio("📑 Wybierz typ degena:", list(degen_details.keys()))
    else:
        selected_page = "🏠 Strona główna (test)"

    if selected_page and selected_page != "🏠 Strona główna (test)":
        st.markdown(degen_details[selected_page], unsafe_allow_html=True)
        st.markdown("""
            <script>
                window.scrollTo(0, 0);
            </script>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("⬅️ Wróć do menu bocznego, aby wybrać inny typ lub przejdź do testu.")
    elif selected_page == "🏠 Strona główna (test)":
        def plot_radar_chart(scores):
            labels = list(scores.keys())
            values = list(scores.values())
            values += values[:1]
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.plot(angles, values, 'o-', linewidth=2)
            ax.fill(angles, values, alpha=0.25)
            ax.set_thetagrids(np.degrees(angles[:-1]), labels)
            ax.set_ylim(0, max(values) if max(values) > 0 else 1)
            ax.set_title("Twój profil inwestycyjny (Degen)", size=15)
            ax.grid(True)
            st.pyplot(fig)

        st.markdown("""
        ### 👉 Jak działa ten test?

        Ten test pomoże Ci sprawdzić, **jakim typem inwestora (degena)** jesteś.

        - Każde pytanie ma **8 odpowiedzi** – każda reprezentuje inny styl inwestycyjny.
        - **Wybierz tę odpowiedź, która najlepiej opisuje Twoje zachowanie lub sposób myślenia.**
        - Po zakończeniu zobaczysz graficzny wynik w postaci wykresu radarowego.

        🧩 Gotowy? Zaczynamy!
        """)

        scores = {k: 0 for k in degen_details.keys()}

        for idx, question in enumerate(questions):
            st.subheader(f"Pytanie {idx + 1}: {question['question']}")
            selected = st.radio("Wybierz jedną odpowiedź:", list(question["answers"].values()), key=f"q_{idx}")
            for degen_type, answer in question["answers"].items():
                if selected == answer:
                    scores[degen_type] += 1

        if st.button("🎯 Pokaż mój wynik"):
            st.markdown("### 📊 Twój wynik na wykresie radarowym:")
            plot_radar_chart(scores)
