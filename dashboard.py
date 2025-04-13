import streamlit as st
import threading
import numpy as np
from consumer import latest_tracks, consume_messages
from utils import draw_bbox, generate_heatmap, detect_anomaly, background
from PIL import Image

# Khởi động consumer
if 'consumer_started' not in st.session_state:
    threading.Thread(target=consume_messages, daemon=True).start()
    st.session_state['consumer_started'] = True

st.title("📡 Multi-Camera Tracking Dashboard")
st.sidebar.header("🔍 Bộ lọc")
camera_filter = st.sidebar.selectbox("Chọn Camera ID", options=[None] + list(set(d["camera_id"] for d in latest_tracks[-500:])))
obj_filter = st.sidebar.selectbox("Chọn Object ID", options=[None] + list(set(d["obj_id"] for d in latest_tracks[-500:])))

# Áp dụng filter
filtered_tracks = [
    d for d in latest_tracks
    if (camera_filter is None or d["camera_id"] == camera_filter)
    and (obj_filter is None or d["obj_id"] == obj_filter)
]

st.subheader("🎯 Khung hình mới nhất")

if filtered_tracks:
    latest = filtered_tracks[-1]
    img = draw_bbox(latest, background)
    st.image(img[:, :, ::-1], caption=f"Camera {latest['camera_id']} | Object {latest['obj_id']}", use_column_width=True)

    # Cảnh báo
    warning = detect_anomaly(latest)
    if warning:
        st.error(warning)

st.subheader("🔥 Heatmap Di chuyển")
points = [(d['gps']['xworld']*5, d['gps']['yworld']*5) for d in filtered_tracks]
heatmap_img = generate_heatmap(points, background)
st.image(heatmap_img[:, :, ::-1], use_column_width=True)

st.subheader("📜 Lịch sử Tracking")
for item in reversed(filtered_tracks[-10:]):
    st.markdown(f"""
    **Cam:** {item['camera_id']} | **ID:** {item['obj_id']} | **Frame:** {item['frame_id']}  
    **BBox:** ({item['bbox']['xmin']}, {item['bbox']['ymin']} - {item['bbox']['width']}x{item['bbox']['height']})  
    **GPS:** ({item['gps']['xworld']}, {item['gps']['yworld']})
    ---
    """)
