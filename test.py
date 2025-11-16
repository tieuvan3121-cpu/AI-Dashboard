# dashboard.py

import streamlit as st
import pandas as pd
import time
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time # Đảm bảo bạn đã import time ở đầu file
# --- Giả lập Dữ liệu Real-time (Thay thế bằng Logic CNN-LSTM của bạn) ---
@st.cache_data
def load_data():
    # Tải dữ liệu cơ sở của bạn (ví dụ: giá đóng cửa gần nhất)
    df = pd.DataFrame({
        'timestamp': [datetime.now() - pd.Timedelta(seconds=i) for i in range(10, 0, -1)],
        'price': np.random.rand(10) * 100 + 27000,
        'my_indicator': np.random.rand(10) * 50 + 27000 
    })
    return df.set_index('timestamp')

# --- Hàm Vẽ Biểu đồ Plotly ---
def plot_chart(df):
    fig = go.Figure()
    
    # Biểu đồ Giá (Ví dụ: Dùng dạng đường đơn giản)
    fig.add_trace(go.Scatter(x=df.index, y=df['price'], mode='lines', name='Giá Cổ phiếu'))
    
    # Chỉ báo của bạn (My Indicator)
    fig.add_trace(go.Scatter(x=df.index, y=df['my_indicator'], mode='lines', name='Chỉ báo AI', line=dict(color='red', dash='dot')))
    
    fig.update_layout(title='Chỉ báo AI theo Thời gian Thực', 
                      xaxis_title='Thời gian', 
                      yaxis_title='Giá trị',
                      xaxis_rangeslider_visible=False)
    return fig

# --- Ứng dụng Streamlit (Cập nhật Real-time) ---
st.set_page_config(layout="wide")
st.title("🚀 Dashboard Chỉ báo AI")

# Thiết lập bộ chứa để biểu đồ có thể cập nhật
placeholder = st.empty()

# Thiết lập vòng lặp cập nhật
while True:
    df_data = load_data() 
    
    with placeholder.container():
        # Vẽ biểu đồ Plotly và hiển thị
        st.plotly_chart(plot_chart(df_data), use_container_width=True, key=f"chart_{time.time()}")
        st.write(f"Cập nhật lần cuối: {datetime.now().strftime('%H:%M:%S')}")
        
    time.sleep(5) # Chờ 5 giây trước khi cập nhật lại


    
# Sử dụng thời gian hiện tại làm key duy nhất
