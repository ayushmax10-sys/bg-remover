import io
import streamlit as st
from PIL import Image
from rembg import remove

st.set_page_config(page_title="BG Remover Pro", page_icon="🪄", layout="wide")

# --- Custom CSS (creative UI) ---
st.markdown(
    """
<style>
/* Hide Streamlit default menu/footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.app-hero {
  padding: 26px 28px;
  border-radius: 22px;
  border: 1px solid rgba(255,255,255,.14);
  background:
    radial-gradient(900px 450px at 20% 0%, rgba(99,102,241,.35), transparent 55%),
    radial-gradient(900px 450px at 80% 15%, rgba(236,72,153,.28), transparent 55%),
    rgba(255,255,255,.06);
  backdrop-filter: blur(10px);
  box-shadow: 0 24px 70px rgba(0,0,0,.35);
}

.hero-title {
  font-size: 40px;
  font-weight: 900;
  line-height: 1.05;
  margin: 0;
  letter-spacing: -1px;
  background: linear-gradient(90deg, #ffffff, #fde047, #a78bfa, #fb7185, #ffffff);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shimmer 3s linear infinite;
}

@keyframes shimmer { to { background-position: 200% center; } }

.hero-sub {
  margin-top: 10px;
  opacity: 0.9;
  font-size: 16px;
}

.glass-card {
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,.12);
  background: rgba(255,255,255,.06);
  padding: 18px;
}

.pill {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: .12em;
  text-transform: uppercase;
  background: rgba(99,102,241,.22);
  border: 1px solid rgba(99,102,241,.35);
}

.small {
  font-size: 13px;
  opacity: .85;
}

.checker {
  border-radius: 14px;
  background-image:
    linear-gradient(45deg, rgba(255,255,255,.12) 25%, transparent 25%),
    linear-gradient(-45deg, rgba(255,255,255,.12) 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, rgba(255,255,255,.12) 75%),
    linear-gradient(-45deg, transparent 75%, rgba(255,255,255,.12) 75%);
  background-size: 24px 24px;
  background-position: 0 0, 0 12px, 12px -12px, -12px 0px;
  padding: 10px;
}
</style>
""",
    unsafe_allow_html=True,
)

# --- Background ---
st.markdown(
    """
<style>
.stApp {
  background:
    radial-gradient(1200px 600px at 15% 10%, rgba(99,102,241,.25), transparent 55%),
    radial-gradient(1000px 600px at 85% 20%, rgba(236,72,153,.22), transparent 55%),
    #0b1220;
  color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

# --- Hero ---
st.markdown(
    """
<div class="app-hero">
  <span class="pill">FREE • HIGH QUALITY • PNG</span>
  <h1 class="hero-title">Background Remover</h1>
  <div class="hero-sub">Upload an image → remove background → download a transparent PNG (lossless).</div>
  <div class="small">Tip: Best results for product photos, portraits, and clear foreground objects.</div>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# --- App layout ---
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("1) Upload")
    uploaded = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg", "webp"])
    st.caption("Your image is processed on the server running this app.")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("2) Settings")
    # Keep it simple; quality is mainly about saving PNG + not resizing.
    output_name = st.text_input("Download file name", value="no-bg.png")
    st.caption("Output is saved as PNG to keep **high quality** (lossless).")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.divider()

if uploaded:
    data = uploaded.read()
    img = Image.open(io.BytesIO(data)).convert("RGBA")

    c1, c2 = st.columns([1, 1], gap="large")

    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Original")
        st.image(img, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Result (transparent PNG)")
        if st.button("🪄 Remove background", use_container_width=True):
            with st.spinner("Removing background... please wait"):
                out = remove(img)

            # Encode as PNG (lossless / high quality)
            buf = io.BytesIO()
            out.save(buf, format="PNG")
            png_bytes = buf.getvalue()

            st.markdown('<div class="checker">', unsafe_allow_html=True)
            st.image(out, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.download_button(
                label="⬇️ Download PNG (HQ)",
                data=png_bytes,
                file_name=output_name if output_name.endswith(".png") else output_name + ".png",
                mime="image/png",
                use_container_width=True,
            )
            st.caption("PNG keeps quality. No extra compression applied.")
        else:
            st.info("Click “Remove background” to generate your PNG.")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Upload an image to start.")
