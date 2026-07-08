import streamlit as st
import google.generativeai as genai

# 1. Masukkan API Key kamu di bawah ini
# Kita menyuruh Streamlit mengambil API Key dari pengaturan rahasia cloud nanti
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# 2. FITUR BARU: Auto-detect model (Mencari model yang tersedia otomatis)
nama_model_aktif = None
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        nama_model_aktif = m.name
        break # Ambil model pertama yang ditemukan

# 3. Desain Tampilan Website
st.set_page_config(page_title="Super App Mahasiswa", page_icon="🎓")
st.title("🤖 Super App AI Mahasiswa")

# Cek apakah model berhasil ditemukan
if nama_model_aktif:
    model = genai.GenerativeModel(nama_model_aktif)
    st.caption(f"*(Berhasil terhubung ke server Google menggunakan model: {nama_model_aktif})*")
else:
    st.error("Gawat, API Key kamu tidak mendeteksi model apapun. Pastikan API Key sudah benar.")

st.write("Halo! Aku asisten akademik kamu. Ada materi kuliah yang mau didiskusikan hari ini?")

# 4. Kotak Tempat Pengguna Mengetik
pertanyaan = st.text_input("Ketik pertanyaan atau tugasmu di sini:")

# 5. Tombol Kirim & Logika AI
if st.button("Kirim ke AI"):
    if pertanyaan:
        with st.spinner("AI sedang memproses..."):
            try:
                # Mengirim pertanyaan ke server AI
                response = model.generate_content(pertanyaan)
                
                # Menampilkan jawaban di website
                # st.success("Selesai!")
                st.write(response.text)
            except Exception as e:
                # Jika masih ada error, akan muncul di sini agar mudah dicek
                st.error(f"Terjadi kesalahan teknis: {e}")
    else:
        st.warning("Ketik sesuatu dulu ya sebelum klik kirim!")
