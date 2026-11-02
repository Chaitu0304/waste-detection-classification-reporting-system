from ultralytics import YOLO
import streamlit as st
import cv2
import settings
from pathlib import Path
import PIL.Image
import PIL.ExifTags


# ============================================================
# NEW: IMAGE DIMENSIONS & EXIF LOCATION EXTRACTION HELPERS
# ============================================================

def get_image_dimensions(image: PIL.Image.Image):
    """Returns (width, height) of a PIL Image."""
    return image.size


def extract_exif_location(image: PIL.Image.Image):
    """Extracts GPS coordinates from image EXIF metadata if available."""
    try:
        exif = image._getexif()
        if not exif:
            return None

        gps_info = {}
        for key, val in exif.items():
            if key in PIL.ExifTags.TAGS and PIL.ExifTags.TAGS[key] == 'GPSInfo':
                for k in val:
                    sub_tag = PIL.ExifTags.GPSTAGS.get(k, k)
                    gps_info[sub_tag] = val[k]

        if 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info:

            def _convert_to_degrees(value):
                d = float(value[0])
                m = float(value[1])
                s = float(value[2])
                return d + (m / 60.0) + (s / 3600.0)

            lat = _convert_to_degrees(gps_info['GPSLatitude'])
            if gps_info.get('GPSLatitudeRef', 'N') != 'N':
                lat = -lat

            lon = _convert_to_degrees(gps_info['GPSLongitude'])
            if gps_info.get('GPSLongitudeRef', 'E') != 'E':
                lon = -lon

            return f'GPS: {lat:.5f}°, {lon:.5f}°'
    except Exception:
        pass
    return None


# ============================================================
# MODEL & VIDEO UTILITIES
# ============================================================

@st.cache_resource
def load_model(model_path):
    """
    Loads a YOLO or HybridWasteDetector object detection model from the specified model_path.

    Parameters:
        model_path (str or Path): The path to the model file or 'hybrid'.

    Returns:
        A YOLO object detection model or HybridWasteDetector.
    """
    if str(model_path) == "hybrid" or "hybrid" in str(model_path).lower():
        from hybrid_detector import HybridWasteDetector
        return HybridWasteDetector()
    model = YOLO(model_path)
    return model


def display_tracker_options():
    """
    Display object tracking controls in the main application area.
    """

    st.markdown("### Tracking Options")

    display_tracker = st.radio(
        "Enable Object Tracking",
        ("No", "Yes"),
        horizontal=True
    )

    is_display_tracker = display_tracker == "Yes"

    if is_display_tracker:

        tracker_type = st.selectbox(
            "Tracking Algorithm",
            ("bytetrack.yaml", "botsort.yaml")
        )

        return True, tracker_type

    return False, None


def _display_detected_frames(conf, model, st_frame, image, is_display_tracking=None, tracker=None):
    """
    Display the detected objects on a video frame using the YOLOv8 model.
    """

    # Resize the image to a standard width, keeping its aspect ratio
    h, w = image.shape[:2]
    image = cv2.resize(image, (720, int(720 * h / w)))

    # Display object tracking, if specified
    if is_display_tracking:
        res = model.track(image, conf=conf, iou=0.45, agnostic_nms=False, persist=True, tracker=tracker)
    else:
        # Predict the objects in the image using the YOLOv8 model
        res = model.predict(image, conf=conf, iou=0.45, agnostic_nms=False)

    # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   width='stretch'
                   )


def play_youtube_video(conf, model, source_youtube=None):
    """
    Plays a YouTube video stream and detects objects in real-time.
    """
    if source_youtube is None:
        source_youtube = st.session_state.get(
            "youtube_url",
            ""
        )

    is_display_tracker, tracker = display_tracker_options()

    if source_youtube:
        try:
            # pyrefly: ignore [missing-import]
            import pafy
            video = pafy.new(source_youtube)
            best = video.getbest(preftype="mp4")
            vid_cap = cv2.VideoCapture(best.url)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             is_display_tracker,
                                             tracker
                                             )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading YouTube video: " + str(e))


def play_rtsp_stream(conf, model, source_rtsp=None):
    """
    Plays an RTSP stream and detects objects in real-time.
    """
    if source_rtsp is None:
        source_rtsp = st.session_state.get(
            "rtsp_url",
            ""
        )
    is_display_tracker, tracker = display_tracker_options()
    if source_rtsp:
        try:
            vid_cap = cv2.VideoCapture(source_rtsp)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             is_display_tracker,
                                             tracker
                                             )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading RTSP stream: " + str(e))


def play_webcam(conf, model, start_webcam=False):
    """
    Plays a webcam stream.
    Detects objects in real-time using the YOLOv8 object detection model.
    """

    source_webcam = settings.WEBCAM_PATH

    is_display_tracker, tracker = display_tracker_options()

    if start_webcam:

        try:

            vid_cap = cv2.VideoCapture(source_webcam)

            if not vid_cap.isOpened():
                st.error("Unable to access the webcam.")
                return

            st_frame = st.empty()

            while vid_cap.isOpened():

                success, image = vid_cap.read()

                if success:

                    _display_detected_frames(
                        conf,
                        model,
                        st_frame,
                        image,
                        is_display_tracker,
                        tracker,
                    )

                else:

                    vid_cap.release()
                    break

        except Exception as e:

            st.error(
                "Error loading webcam stream: " + str(e)
            )

        finally:

            if 'vid_cap' in locals():
                vid_cap.release()


def play_stored_video(conf, model):
    """
    Plays a stored video file or uploaded video. Tracks and detects objects in real-time.
    """
    uploaded_video = st.sidebar.file_uploader("Upload a video...", type=["mp4", "avi", "mov", "mkv"])
    
    selected_video_path = None
    if uploaded_video is not None:
        import tempfile
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        tfile.write(uploaded_video.read())
        selected_video_path = tfile.name
        st.video(selected_video_path)
    elif settings.VIDEOS_DICT:
        source_vid = st.sidebar.selectbox("Or choose a sample video...", list(settings.VIDEOS_DICT.keys()))
        selected_video_path = str(settings.VIDEOS_DICT.get(source_vid))
        if Path(selected_video_path).exists():
            with open(selected_video_path, 'rb') as video_file:
                video_bytes = video_file.read()
                if video_bytes:
                    st.video(video_bytes)

    is_display_tracker, tracker = display_tracker_options()

    if selected_video_path and st.sidebar.button('Detect Video Trash'):
        try:
            vid_cap = cv2.VideoCapture(selected_video_path)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             is_display_tracker,
                                             tracker
                                             )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error processing video: " + str(e))

import streamlit as st

def get_live_device_location():
    """Triggers browser HTML5 Geolocation API and returns coordinates string."""
    geo_html = """
    <div id="location-status" style="font-family: sans-serif; font-size: 13px; color: #176044;">
        🌐 Fetching live device GPS coordinates...
    </div>
    <script>
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude.toFixed(5);
                const lon = position.coords.longitude.toFixed(5);
                const locStr = `GPS: ${lat}°, ${lon}°`;
                document.getElementById("location-status").innerHTML = `✅ Captured Live: <b>${locStr}</b>`;
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: locStr}, '*');
            },
            (error) => {
                document.getElementById("location-status").innerHTML = `⚠️ GPS Access Denied / Unavailable`;
            },
            { enableHighAccuracy: true, timeout: 8000 }
        );
    } else {
        document.getElementById("location-status").innerHTML = `⚠️ Geolocation not supported by browser.`;
    }
    </script>
    """
    return st.iframe(geo_html, height=35)

def parse_gps_coords(gps_data):
    """Parses location data into float (latitude, longitude) tuple."""
    if isinstance(gps_data, dict) and "lat" in gps_data and "lon" in gps_data:
        return float(gps_data["lat"]), float(gps_data["lon"])
    if isinstance(gps_data, str) and "GPS:" in gps_data:
        try:
            clean_str = gps_data.replace("GPS:", "").replace("°", "").strip()
            lat_str, lon_str = clean_str.split(",")
            return float(lat_str.strip()), float(lon_str.strip())
        except Exception:
            return None
    return None