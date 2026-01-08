import io
import streamlit as st
from PIL import Image
from rembg import remove

st.set_page_config(page_title="BG Remover", page_icon="🪄", layout="centered")

st.title("🪄 Background Remover")
st.caption("Upload an image → remove background → download transparent PNG.")

uploaded = st.file_uploader("Upload image", type=["png", "jpg", "jpeg", "webp"])

if uploaded:
    data = uploaded.read()
    img = Image.open(io.BytesIO(data)).convert("RGBA")

    st.subheader("Original")
    st.image(img, use_container_width=True)

    if st.button("Remove background"):
        with st.spinner("Removing background... (first run can take time)"):
            out = remove(img)

        st.subheader("Result (PNG)")
        st.image(out, use_container_width=True)

        buf = io.BytesIO()
        out.save(buf, format="PNG")
        st.download_button(
            "Download PNG",
            data=buf.getvalue(),
            file_name="no-bg.png",
            mime="image/png",
        )
else:
    st.info("Upload an image to start.")

