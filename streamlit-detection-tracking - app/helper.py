from ultralytics import YOLO
import streamlit as st
import cv2
import settings
from pathlib import Path


def load_model(model_path):
    """
    Loads a YOLO object detection model from the specified model_path.

    Parameters:
        model_path (str): The path to the YOLO model file.

    Returns:
        A YOLO object detection model.
    """
    model = YOLO(model_path)
    return model


def display_tracker_options():
    """
    Display object tracking controls in the main application area.
    """

    st.markdown("### 🎯 Tracking Options")

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

    Args:
    - conf (float): Confidence threshold for object detection.
    - model (YoloV8): A YOLOv8 object detection model.
    - st_frame (Streamlit object): A Streamlit object to display the detected video.
    - image (numpy array): A numpy array representing the video frame.
    - is_display_tracking (bool): A flag indicating whether to display object tracking (default=None).

    Returns:
    None
    """

    # Resize the image to a standard size
    image = cv2.resize(image, (720, int(720*(9/16))))

    # Display object tracking, if specified
    if is_display_tracking:
        res = model.track(image, conf=conf, persist=True, tracker=tracker)
    else:
        # Predict the objects in the image using the YOLOv8 model
        res = model.predict(image, conf=conf)

    # # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_container_width=True
                   )


def play_youtube_video(conf, model,source_youtube=None):
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


def play_rtsp_stream(conf, model,source_rtsp=None):
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
                st.error("❌ Unable to access the webcam.")
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
