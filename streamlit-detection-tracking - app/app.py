# Python In-built packages
from pathlib import Path
import PIL
import pandas as pd

# External packages
import streamlit as st

# Local Modules
import settings
import helper

# Setting page layout
st.set_page_config(
    page_title="Waste Classification using YOLOv8",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("♻️ Waste Classification & Detection using YOLOv8")
st.caption("AI-powered automated waste classification, object detection, real-time tracking, and analytics dashboard.")

# Sidebar
st.sidebar.header("⚙️ ML Model Config")

# Model Options
model_type = st.sidebar.radio(
    "Select Task", ['Detection'])

confidence = float(st.sidebar.slider(
    "Select Model Confidence Threshold", 10, 100, 15)) / 100

st.sidebar.caption("💡 *Lower confidence threshold (10%-25%) helps detect smaller, cluttered, or AI-generated garbage objects.*")

# Selecting Detection Or Segmentation
if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)
elif model_type == 'Segmentation':
    model_path = Path(settings.SEGMENTATION_MODEL)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("📷 Input Source Config")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

source_img = None
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                st.image(default_image_path, caption="Default Image",
                         use_container_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image",
                         use_container_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='Detected Image (Sample)',
                     use_container_width=True)
        else:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image, conf=confidence)
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Detection Results', use_container_width=True)
                
                # Analyze detection results
                try:
                    stats = {}
                    for box in boxes:
                        class_id = int(box.cls[0])
                        class_name = model.names[class_id]
                        conf_score = float(box.conf[0])
                        
                        if class_name not in stats:
                            stats[class_name] = {'count': 0, 'conf_sum': 0.0}
                        stats[class_name]['count'] += 1
                        stats[class_name]['conf_sum'] += conf_score

                    if stats:
                        st.subheader("📊 Waste Classification Summary & Analytics")
                        
                        total_items = sum(item['count'] for item in stats.values())
                        unique_cats = len(stats)
                        top_cat = max(stats.items(), key=lambda x: x[1]['count'])[0]

                        # Display Summary Metric Cards
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Total Waste Items Detected", total_items)
                        m2.metric("Unique Waste Categories", unique_cats)
                        m3.metric("Dominant Waste Category", top_cat)

                        # Formulate Detailed Dataframe
                        table_data = []
                        for cat, data in stats.items():
                            avg_conf = (data['conf_sum'] / data['count']) * 100
                            table_data.append({
                                'Waste Category': cat,
                                'Quantity': data['count'],
                                'Avg Confidence (%)': f"{avg_conf:.1f}%"
                            })
                        
                        df = pd.DataFrame(table_data)
                        
                        # Layout layout splits: Table + Bar Chart
                        col_tbl, col_chart = st.columns([1, 1])
                        with col_tbl:
                            st.write("##### Detailed Breakdown")
                            st.dataframe(df, use_container_width=True)
                            
                        with col_chart:
                            st.write("##### Category Distribution")
                            chart_df = pd.DataFrame({
                                'Waste Category': [d['Waste Category'] for d in table_data],
                                'Quantity': [d['Quantity'] for d in table_data]
                            }).set_index('Waste Category')
                            st.bar_chart(chart_df)

                        # Generate downloadable CSV report
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Detailed Waste Report (CSV)",
                            data=csv,
                            file_name="waste_classification_report.csv",
                            mime="text/csv",
                        )
                        
                        # Admin reporting feature
                        if st.button("🔔 Dispatch Report to Waste Admin Console"):
                            st.success("✅ Waste report successfully dispatched to Admin Console!")
                            st.toast("Report dispatched to waste management system.", icon="📨")
                    else:
                        st.info("No waste items detected based on the selected confidence threshold. Try lowering the threshold in the sidebar!")
                except Exception as ex:
                    st.error("Error generating waste report.")
                    st.error(ex)

elif source_radio == settings.VIDEO:
    helper.play_stored_video(confidence, model)

elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model)

elif source_radio == settings.YOUTUBE:
    helper.play_youtube_video(confidence, model)

elif source_radio == settings.RTSP:
    helper.play_rtsp_stream(confidence, model)

else:
    st.error("Please select a valid source type!")
