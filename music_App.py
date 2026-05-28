import streamlit as st
import cv2
from deepface import DeepFace
from music_recommendation import recommend_music
from music_generator import generate_music
from datetime import datetime

st.set_page_config(
    page_title="AI Emotion Music System",
    layout="wide"
)

# ---------- CSS ----------
st.markdown("""
<style>
.main {
    background-color: #FFF8F0;
}

.title-box {
    background: linear-gradient(90deg, #F7C8A9, #F6E7CB);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 20px;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

.big-text {
    font-size: 28px;
    font-weight: bold;
}

.small-text {
    font-size: 18px;
    color: #555;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("""
<div class="title-box">
    <h1>Emotion-Aware AI Music System</h1>
    <p>Facial Emotion Recognition + Music Recommendation + MIDI Generation</p>
</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("System Control")

    mode = st.radio(
        "Choose Mode",
        ["Webcam Detection", "Manual Demo"]
    )

    st.markdown("---")

    st.subheader("Project Information")

    st.write("Dataset: FER2013")
    st.write("Model: DeepFace CNN")
    st.write("Music Type: Pop Music")

# ---------- HISTORY ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- LAYOUT ----------
col1, col2 = st.columns([1.2, 1])

detected_emotion = None

# ---------- LEFT ----------
with col1:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Emotion Detection")

    if mode == "Webcam Detection":

        detect = st.button("Detect Emotion")

        frame_window = st.image([])

        if detect:

            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()

            if not ret:
                st.error("Cannot access webcam.")

            else:

                try:

                    result = DeepFace.analyze(
                        frame,
                        actions=["emotion"],
                        enforce_detection=False
                    )

                    if isinstance(result, list):
                        result = result[0]

                    detected_emotion = result["dominant_emotion"]

                    cv2.putText(
                        frame,
                        f"Emotion: {detected_emotion}",
                        (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )

                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    frame_window.image(frame)

                except Exception:
                    st.warning("Emotion detection failed.")

    else:

        detected_emotion = st.selectbox(
            "Select Emotion",
            [
                "happy",
                "sad",
                "angry",
                "neutral",
                "surprise",
                "fear",
                "disgust"
            ]
        )

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- RIGHT ----------
with col2:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Result")

    if detected_emotion:

        music_info = recommend_music(detected_emotion)

        midi_file = generate_music(detected_emotion)

        music = music_info["music"]

        description = music_info["description"]

        st.markdown(
            f"""
            <div class="big-text">
            Detected Emotion: {detected_emotion}
            </div>

            <p class="small-text">
            Recommended Music: {music}
            </p>
            """,
            unsafe_allow_html=True
        )

        st.success(description)

        # MIDI Download
        with open(midi_file, "rb") as f:

            st.download_button(
                label="Download Generated MIDI Music",
                data=f,
                file_name="generated_music.mid",
                mime="audio/midi"
            )

        # Save history
        st.session_state.history.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "emotion": detected_emotion,
            "music": music
        })

    else:
        st.info("No emotion detected yet.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- TABLE ----------
st.markdown("---")

st.subheader("Emotion and Music Mapping")

mapping = {
    "Emotion": [
        "Happy",
        "Sad",
        "Angry",
        "Neutral",
        "Surprise",
        "Fear",
        "Disgust"
    ],
    "Recommended Music": [
        "Upbeat Pop",
        "Pop Ballad",
        "Calm Acoustic Pop",
        "Lo-fi Pop",
        "Dance Pop",
        "Soft Pop",
        "Chill Pop"
    ]
}

st.table(mapping)

# ---------- HISTORY ----------
st.subheader("Detection History")

if st.session_state.history:
    st.dataframe(st.session_state.history)
else:
    st.write("No history available.")