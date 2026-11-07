import streamlit as st
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import zipfile

st.set_page_config(
    page_title="Image-Wenk Pro",
    page_icon="🔬",
    layout="wide"
)

# ===================== CSS =====================

st.markdown("""
<style>
.stApp {
    background: #0B1120;
    color: #F1F5F9;
}
[data-testid="stSidebar"] {
    background: #111C30;
}
.block-container {
    max-width: 1450px;
    padding-top: 2rem;
}
.hero {
    background: linear-gradient(120deg,#142C50,#25215C,#351E65);
    border: 1px solid #344B80;
    border-radius: 22px;
    padding: 35px;
    margin-bottom: 25px;
}
.hero-title {
    font-size: 42px;
    font-weight: 900;
    color: white;
}
.hero-desc {
    color: #CBD5E1;
    line-height: 1.8;
}
.metric {
    background: #172943;
    border: 1px solid #293D5A;
    border-radius: 15px;
    padding: 20px;
}
.metric-label {
    color: #94A3B8;
    font-size: 12px;
}
.metric-value {
    color: white;
    font-size: 26px;
    font-weight: 800;
}
.stButton button, .stDownloadButton button {
    background: #1D3A62;
    color: white;
    border-radius: 10px;
    border: 1px solid #35527A;
    font-weight: 700;
}
.stButton button:hover, .stDownloadButton button:hover {
    background: #2563EB;
    color: white;
}
.stTabs [data-baseweb="tab-list"] {
    background: #111C30;
    border-radius: 12px;
    padding: 7px;
}
.stTabs [aria-selected="true"] {
    background: #1D3A62 !important;
    color: white !important;
}
[data-testid="stImage"] img {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ===================== ALGORITHMS =====================

def translation(img, tx, ty):
    h, w = img.shape[:2]
    matrix = np.float32([[1, 0, tx], [0, 1, ty]])
    return cv2.warpAffine(
        img, matrix, (w, h),
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(12, 17, 30)
    )


def scaling(img, factor):
    h, w = img.shape[:2]
    nw = max(1, int(w * factor))
    nh = max(1, int(h * factor))
    interpolation = cv2.INTER_AREA if factor < 1 else cv2.INTER_CUBIC
    return cv2.resize(img, (nw, nh), interpolation=interpolation)


def rotation(img, angle):
    h, w = img.shape[:2]
    center = (w / 2, h / 2)

    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    cos = abs(matrix[0, 0])
    sin = abs(matrix[0, 1])

    nw = int(w * cos + h * sin)
    nh = int(h * cos + w * sin)

    matrix[0, 2] += nw / 2 - center[0]
    matrix[1, 2] += nh / 2 - center[1]

    return cv2.warpAffine(
        img, matrix, (nw, nh),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(12, 17, 30)
    )


def horizontal_flip(img):
    return cv2.flip(img, 1)


def vertical_flip(img):
    return cv2.flip(img, 0)


# ===================== HELPERS =====================

def metric(label, value):
    st.markdown(f"""
    <div class="metric">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def to_png(img):
    success, encoded = cv2.imencode(
        ".png",
        cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    )
    return encoded.tobytes() if success else None


def make_zip(images):
    memory = BytesIO()
    with zipfile.ZipFile(memory, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, img in images.items():
            filename = name.lower().replace(" ", "_").replace("°", "deg")
            archive.writestr(filename + ".png", to_png(img))
    memory.seek(0)
    return memory.getvalue()


# ===================== SIDEBAR =====================

with st.sidebar:
    st.markdown("""
    <h2 style="color:white">🔬 IMAGE-WENK <span style="color:#60A5FA">PRO</span></h2>
    <p style="color:#94A3B8;font-size:11px;letter-spacing:2px">
    IMAGE PROCESSING STUDIO
    </p>
    """, unsafe_allow_html=True)

    st.divider()

    uploaded = st.file_uploader(
        "📂 Upload your image",
        type=["jpg", "jpeg", "png"]
    )

    st.divider()
    st.markdown("### Translation Controls")

    tx = st.slider("Horizontal X", -500, 500, 100, 10)
    ty = st.slider("Vertical Y", -500, 500, 50, 10)

    st.divider()
    st.success("SYSTEM ONLINE")
    st.caption("Python · OpenCV · NumPy")
    st.caption("Informatics Engineering · Semester 5")


# ===================== HEADER =====================

st.markdown("""
<div class="hero">
    <div style="color:#93C5FD;font-size:12px;font-weight:800;letter-spacing:2px">
        DIGITAL IMAGE PROCESSING / WORKSPACE 01
    </div>
    <div class="hero-title">
        Transform your vision.<br>
        <span style="color:#93C5FD">Create something amazing.</span>
    </div>
    <div class="hero-desc">
        Interactive image processing platform.
        Explore Translation, Scaling, Rotation and Flip
        through real-time image transformation.
    </div>
</div>
""", unsafe_allow_html=True)


# ===================== EMPTY STATE =====================

if uploaded is None:
    st.markdown("## Welcome to Image-Wenk Pro")
    st.markdown("""
    <div style="background:#14243B;border:1px dashed #45658F;
    border-radius:18px;padding:45px;text-align:center">
        <div style="font-size:60px">🖼️</div>
        <h2 style="color:white">Your workspace starts here</h2>
        <p style="color:#94A3B8">
        Upload an image through the sidebar to get started.
        </p>
        <b style="color:#60A5FA">JPG · JPEG · PNG</b>
    </div>
    """, unsafe_allow_html=True)

    a, b, c, d = st.columns(4)
    with a:
        metric("TRANSFORMATIONS", "08")
    with b:
        metric("ALGORITHMS", "04")
    with c:
        metric("FORMATS", "JPG/PNG")
    with d:
        metric("PROCESSING", "LIVE")
    st.stop()


# ===================== LOAD IMAGE =====================

try:
    original = np.array(Image.open(uploaded).convert("RGB"))
except Exception as e:
    st.error(f"Gagal membaca gambar: {e}")
    st.stop()

h, w = original.shape[:2]
file_size = len(uploaded.getvalue()) / 1024


# ===================== TRANSFORMATIONS =====================

images = {
    "Original Image": original,
    "Translation": translation(original, tx, ty),
    "Scaling 0.5x": scaling(original, 0.5),
    "Scaling 2x": scaling(original, 2.0),
    "Rotation 45°": rotation(original, 45),
    "Rotation 90°": rotation(original, 90),
    "Rotation 180°": rotation(original, 180),
    "Horizontal Flip": horizontal_flip(original),
    "Vertical Flip": vertical_flip(original)
}


# ===================== METADATA =====================

st.markdown("## 📊 Image Overview")

a, b, c, d = st.columns(4)

with a:
    metric("IMAGE WIDTH", f"{w:,} px")
with b:
    metric("IMAGE HEIGHT", f"{h:,} px")
with c:
    metric("FILE SIZE", f"{file_size:.1f} KB")
with d:
    metric("TOTAL RESULTS", "09")


# ===================== NAVIGATION =====================

tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Overview",
    "🔄 Transformations",
    "🎛️ Interactive Studio",
    "📥 Export Center"
])


# ===================== OVERVIEW =====================

with tab1:
    st.markdown("## 🖼️ Original Image")

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.image(original, use_container_width=True)

    with col2:
        st.markdown("### Image Metadata")
        st.write(f"**Filename:** {uploaded.name}")
        st.write(f"**Width:** {w} pixels")
        st.write(f"**Height:** {h} pixels")
        st.write("**Color Space:** RGB")
        st.write(f"**Size:** {file_size:.2f} KB")
        st.success("Image loaded successfully!")

    st.divider()
    st.markdown("## 🔬 All Transformation Results")

    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    fig.patch.set_facecolor("#0B1120")

    for ax, (name, img) in zip(axes.flat, images.items()):
        ax.imshow(img)
        ax.set_title(name, color="white", fontsize=11, fontweight="bold")
        ax.axis("off")

    plt.tight_layout(pad=2)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# ===================== GALLERY =====================

with tab2:
    st.markdown("## 🔄 Transformation Gallery")
    st.info(f"Translation: X = {tx}px | Y = {ty}px")

    names = list(images.keys())

    for i in range(1, len(names), 2):
        col1, col2 = st.columns(2)

        for col, index in zip([col1, col2], [i, i + 1]):
            if index >= len(names):
                continue

            name = names[index]
            img = images[name]

            with col:
                st.markdown(f"### {name}")
                st.image(img, use_container_width=True)
                st.caption(f"Resolution: {img.shape[1]} × {img.shape[0]} pixels")


# ===================== INTERACTIVE STUDIO =====================

with tab3:
    st.markdown("## 🎛️ Interactive Transformation Studio")

    mode = st.selectbox(
        "Choose transformation",
        ["Translation", "Scaling", "Rotation", "Horizontal Flip", "Vertical Flip"]
    )

    result = original

    st.divider()

    if mode == "Translation":
        c1, c2 = st.columns(2)
        with c1:
            custom_x = st.slider("Horizontal X", -500, 500, 100, 5, key="studio_x")
        with c2:
            custom_y = st.slider("Vertical Y", -500, 500, 50, 5, key="studio_y")
        result = translation(original, custom_x, custom_y)

    elif mode == "Scaling":
        factor = st.slider("Scale Factor", 0.1, 3.0, 1.0, 0.1)
        result = scaling(original, factor)

    elif mode == "Rotation":
        angle = st.slider("Rotation Angle", -180, 180, 45, 5)
        result = rotation(original, angle)

    elif mode == "Horizontal Flip":
        result = horizontal_flip(original)
        st.success("Horizontal Flip Applied!")

    elif mode == "Vertical Flip":
        result = vertical_flip(original)
        st.success("Vertical Flip Applied!")

    st.divider()
    st.markdown("### Before & After Comparison")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**ORIGINAL**")
        st.image(original, use_container_width=True)

    with c2:
        st.markdown("**TRANSFORMED**")
        st.image(result, use_container_width=True)

    st.success(f"Output: {result.shape[1]} × {result.shape[0]} pixels")

    st.download_button(
        "⬇️ Download Result",
        data=to_png(result),
        file_name="image-wenk_result.png",
        mime="image/png",
        use_container_width=True
    )


# ===================== EXPORT CENTER =====================

with tab4:
    st.markdown("## 📥 Export Center")
    st.caption("Download all transformation results.")

    st.download_button(
        "📦 DOWNLOAD ALL RESULTS (.ZIP)",
        data=make_zip(images),
        file_name="Image-Wenk_Results.zip",
        mime="application/zip",
        use_container_width=True
    )

    st.divider()
    st.markdown("### Individual Downloads")

    names = list(images.keys())

    for i in range(0, len(names), 3):
        cols = st.columns(3)

        for col, name in zip(cols, names[i:i + 3]):
            safe_name = name.lower().replace(" ", "_").replace("°", "deg")

            with col:
                st.markdown(f"**{name}**")
                st.download_button(
                    "⬇️ Download PNG",
                    data=to_png(images[name]),
                    file_name=f"{safe_name}.png",
                    mime="image/png",
                    key=f"download_{safe_name}",
                    use_container_width=True
                )


# ===================== FOOTER =====================

st.markdown("""
<div style="text-align:center;border-top:1px solid #263750;
padding:25px;margin-top:40px;color:#64748B">
    <h3 style="color:#93C5FD">🔬 IMAGE-WENK PRO</h3>
    DIGITAL IMAGE PROCESSING WORKSPACE<br>
    Built with Python · OpenCV · NumPy · Matplotlib · Streamlit<br><br>
    Informatics Engineering | Semester 5
</div>
""", unsafe_allow_html=True)
