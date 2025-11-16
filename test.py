import streamlit as st
import pandas as pd
import time
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time # Đảm bảo bạn đã import time ở đầu file

# --- Giả lập Dữ liệu Real-time (Thay thế bằng Logic CNN-LSTM của bạn) ---
# Bỏ @st.cache_data để cho phép mô phỏng cập nhật real-time
def load_data():
    # Tải dữ liệu cơ sở của bạn
    
    # Tạo 500 điểm dữ liệu
    num_points = 500
    timestamps = [datetime.now() - pd.Timedelta(seconds=i) for i in range(num_points, 0, -1)]
    
    # --- Mô hình thị trường (Random Walk) ---
    start_price = 27000
    # Tạo 500 bước thay đổi ngẫu nhiên nhỏ
    price_changes = np.random.uniform(-4, 4.05, num_points) # Thay đổi nhỏ cho mỗi bước
    # Tính giá 'close' bằng cách cộng dồn các thay đổi (random walk)
    close_prices = start_price + np.cumsum(price_changes)
    
    # Đảm bảo giá không bị âm
    close_prices[close_prices <= 0] = 0.01 
    # --- Kết thúc mô hình ---
    
    # Tạo open, high, low dựa trên 'close' để mô phỏng nến
    open_prices = []
    high_prices = []
    low_prices = []
    
    for i in range(num_points):
        close = close_prices[i]
        
        # Mở cửa dựa trên giá đóng cửa trước đó (hoặc ngẫu nhiên nếu là nến đầu)
        if i > 0:
            # Giá mở cửa hôm nay = giá đóng cửa hôm qua + một chút biến động
            open_price = close_prices[i-1] + np.random.uniform(-2, 2)
        else:
            # Nến đầu tiên, giá mở cửa gần giá đóng cửa
            open_price = close + np.random.uniform(-5, 5) 
        
        # high phải là cao nhất, low là thấp nhất
        high_price = max(open_price, close) + np.random.uniform(0, 3)
        low_price = min(open_price, close) - np.random.uniform(0, 3)
        
        open_prices.append(open_price)
        high_prices.append(high_price)
        low_prices.append(low_price)

    df = pd.DataFrame({
        'timestamp': timestamps,
        'open': open_prices,
        'high': high_prices,
        'low': low_prices,
        'close': close_prices,
        # 'my_indicator': np.random.rand(num_points) * 50 + 27000 # Đã xoá theo yêu cầu
    })
    return df.set_index('timestamp')

# --- Hàm Vẽ Biểu đồ Plotly ---
def plot_chart(df):
    fig = go.Figure()
    
    # Biểu đồ Nến
    fig.add_trace(go.Candlestick(x=df.index,
                                open=df['open'],
                                high=df['high'],
                                low=df['low'],
                                close=df['close'],
                                name='Giá Cổ phiếu'))
    
    # Chỉ báo của bạn (My Indicator) - ĐÃ BỎ THEO YÊU CẦU
    # fig.add_trace(go.Scatter(x=df.index, y=df['my_indicator'], mode='lines', name='Chỉ báo AI', line=dict(color='red', dash='dot')))
    
    fig.update_layout(title='Biểu đồ Giá theo Thời gian Thực (Biểu đồ Nến)', 
                      xaxis_title='Thời gian', 
                      yaxis_title='Giá trị',
                      xaxis_rangeslider_visible=False) # Tắt range slider để gọn gàng hơn
    return fig

# --- Ứng dụng Streamlit (Cập nhật Real-time) ---
st.set_page_config(layout="wide")
st.title("🚀 Dashboard Giao dịch") # Đổi tiêu đề một chút

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
