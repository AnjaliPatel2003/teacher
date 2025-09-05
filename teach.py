# app.py
from pathlib import Path
from PIL import Image, UnidentifiedImageError
import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="Teacher's Day Celebration", page_icon="🎓", layout="wide")

# ---------- Simple theming ----------
st.markdown("""
<style>
.header {
  font-size: 44px; font-weight: 800; text-align:center; margin: 0.2rem 0 0.6rem;
  background: linear-gradient(90deg,#ff6b9a,#ffbd59,#3ec5ff);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.sub {text-align:center; font-size:18px; opacity:0.9; margin-bottom:1.2rem;}
.card {
  background:#fff; padding:28px; border-radius:18px;
  box-shadow:0 10px 28px rgba(0,0,0,.10);
  border:1px solid rgba(0,0,0,.06);
}
.quote {
  font-size:20px; font-weight:800; line-height:1.7; color:#222; text-align:center;
}
.badge {
  display:inline-block; padding:6px 12px; border-radius:999px;
  background:#ffeef6; color:#c2185b; font-weight:700; border:1px solid #ffc7de;
}
.footer {text-align:center; opacity:.7; font-size:14px; margin-top: 28px;}
.teacher-name {font-size:26px; font-weight:800; text-align:center; margin: .6rem 0 1rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">🎓 Happy Teacher’s Day</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">A small tribute with love and gratitude</div>', unsafe_allow_html=True)

# ---------- Special Message ----------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="quote">
        🌸 <span class="badge">Thank You, Dear Teacher</span> 🌸<br><br>
        <b>Thank you for everything you have done for me. Happy Teacher's Day!</b><br>
        <b>Your patience, guidance, and lessons have made me what I am today.</b><br>
        <b>I am grateful to have you in my life as my teacher. ❤️</b>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Celebration button
left, _ = st.columns([1,3])
with left:
    if st.button("🎉 Celebrate"):
        st.balloons()

st.markdown("---")

# ---------- Teacher selector ----------
st.markdown("### 📸 View Teacher Photo")

teacher_options = [
    "Rahul Sir", "Chhaya Mam", "Jay sir", "Suraj sir", "Vaishanavi mam", "Vikas sir", "Priyanka mam"
]

IMG_DIR = Path("images")
IMG_DIR.mkdir(exist_ok=True)  # create if missing

# Use base names (no extension) — the resolver below will find .jpg/.png etc.
teacher_to_file = {
    "Rahul Sir": "rahul sir",
    "Chhaya Mam": "chhaya mam",
    "Jay sir": "jay",
    "Suraj sir": "suraj",
    "Vaishanavi mam": "vaishanavi",
    "Vikas sir": "vikas",
    "Priyanka mam": "priyanka",
}

def _normalize_text(s: str) -> str:
    # lower and remove non-alphanumeric for flexible matching
    return "".join(ch for ch in s.lower() if ch.isalnum())

def find_image_for(name_or_base: str) -> Path | None:
    """
    Given a base name or filename (possibly with extension), try to resolve an actual file
    inside IMG_DIR. Returns Path or None.
    """
    val = str(name_or_base)

    # 1) check if user provided exact filename (with or without extension)
    candidate = IMG_DIR / val
    if candidate.exists():
        return candidate

    # 2) if value has an extension, try that exact name again (already done), then strip suffix
    p = Path(val)
    if p.suffix:
        base = p.stem
    else:
        base = val

    # 3) try common extensions
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        cand = IMG_DIR / f"{base}{ext}"
        if cand.exists():
            return cand

    # 4) normalized matching: compare stems ignoring spaces/underscores/case
    norm_target = _normalize_text(base)
    for f in IMG_DIR.iterdir():
        if f.is_file():
            if _normalize_text(f.stem) == norm_target:
                return f

    # 5) nothing found
    return None

c1, c2 = st.columns([2,3])
with c1:
    selected = st.selectbox("Select a teacher:", teacher_options, index=0)

with c2:
    st.markdown(f'<div class="teacher-name">{selected}</div>', unsafe_allow_html=True)

    base_name = teacher_to_file.get(selected, selected)
    img_path = find_image_for(base_name)

    if img_path:
        try:
            img = Image.open(img_path)
            st.image(img, caption=selected, use_column_width=True)
            st.image(img,caption=selected,width=15)
            
        except UnidentifiedImageError:
            st.error(f"⚠️ Found file '{img_path.name}' but it couldn't be opened as an image. Try re-saving the image.")
        except Exception as e:
            st.error(f"⚠️ Error opening image: {e}")
    else:
        # show helpful error plus list of current files in images/
        files = [f.name for f in IMG_DIR.iterdir() if f.is_file()]
        st.error(f"❌ Photo for {selected} not found. Please add a file matching '{base_name}' (e.g. '{base_name}.jpg' or '{base_name}.png') into the images/ folder.")
        if files:
            st.info("Current files in `images/`:\n\n- " + "\n- ".join(files))
        else:
            st.info("Your `images/` folder is currently empty. Add the teacher photos there.")

st.markdown('<div class="footer">Made with ❤️ for Teacher’s Day</div>', unsafe_allow_html=True)
