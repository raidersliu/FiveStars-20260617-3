
import streamlit as st
import streamlit.components.v1 as components
import math
import base64
import os
from datetime import datetime

# ==========================================
# 1. 核心計算邏輯
# ==========================================
def split_and_sum(date_str):
    digits = [int(ch) for ch in date_str if ch.isdigit()]
    total = sum(digits)
    if date_str[0] == '2':
        total += 18
    return digits, total

def reduce_to_single_digit(n):
    while n > 10:
        n = sum(int(d) for d in str(n))
    return n

def get_next_type(current):
    if current == 10:
        return 2
    return current + 1

def get_type_chain(start_type, steps):
    chain = []
    curr = start_type
    for _ in range(steps):
        curr = get_next_type(curr)
        chain.append(curr)
    return chain

def count_10_components(date_str):
    year, month, day = int(date_str[2:4]), int(date_str[4:6]), int(date_str[6:8])
    return sum(1 for val in [year, month, day] if val % 10 == 0)

def sum_mmdd_digits(date_str):
    mmdd = date_str[4:8]
    summ = sum([int(d) for d in mmdd])
    while summ > 10:
        summ = sum(int(d) for d in str(summ))
    return summ

def analyze_date_code(date_str):
    yy, mm, dd = date_str[2:4], date_str[4:6], date_str[6:8]
    combined_digits = yy + mm + dd
    digit_count = {str(i): 0 for i in range(1, 11)}
    for ch in combined_digits:
        if ch in digit_count:
            digit_count[ch] += 1
    digit_count["10"] = sum(1 for x in [yy, mm, dd] if int(x) % 10 == 0)
    return digit_count

def modify_code(date_str, digit_count):
    yy, mm, dd = int(date_str[2:4]), int(date_str[4:6]), int(date_str[6:8])
    aaa = sum(1 for v in [yy, mm, dd] if v == 10)
    digit_count["1"] = str(int(digit_count["1"]) - aaa)
    return digit_count

def calculate_star_type(birthday_str):
    digits, total_sum = split_and_sum(birthday_str)
    simplified = reduce_to_single_digit(total_sum)
    ten_count = count_10_components(birthday_str)
    personality = sum_mmdd_digits(birthday_str)
    return {
        "生日": birthday_str,
        "原始加總": total_sum,
        "轉換次數": ten_count,
        "類型 Type": simplified,
        "人格 Personality": personality,
        "星型類型變化": get_type_chain(simplified, ten_count),
        "成熟年齡": total_sum,
        "轉變年齡": [total_sum + 10 * i for i in range(1, ten_count + 1)]
    }, simplified, ten_count

# ==========================================
# 2. 影像處理與網頁視覺化生成器
# ==========================================
def get_image_as_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    return None

def generate_stars_html(start_t, digit_count, ten_count, b64_image):
    numbers_with_counts = [(str(i), int(digit_count[str(i)])) for i in range(1, 11)]
    stars_html = ""
    current_t = start_t
    
    # 畫布大小
    svg_size = 560
    # 將座標中心微微向下偏移，讓星星在視覺上更置中
    center_x, center_y = svg_size / 2, (svg_size / 2) + 5 
    
    # 【關鍵修改 1：精準抓取您銀色星星的實際頂點半徑】
    # 這些數值是配合圖片縮放比例(60%)所推算出來的，用來計算角度
    radius_outer = 150  # 模擬外角尖端位置
    radius_inner = 70   # 模擬內凹角位置
    
    # 【關鍵修改 2：設定適當的貼齊距離】
    # 這是文字距離星星邊緣向外延伸的「專屬空間」，不會太遠也不會壓到角
    offset_outer = 40  # 外角文字向外推的距離
    offset_inner = 35  # 內角文字向外推的距離

    for trans in range(ten_count + 1):
        if trans > 0:
            current_t = get_next_type(current_t)
            
        points = []
        # 計算 10 個頂點的基準座標
        for i in range(5):
            outer_angle = math.radians(90 + i * 72)
            inner_angle = math.radians(90 + i * 72 + 36)
            
            points.append((center_x + radius_outer * math.cos(outer_angle),
                           center_y - radius_outer * math.sin(outer_angle), "outer"))
            points.append((center_x + radius_inner * math.cos(inner_angle),
                           center_y - radius_inner * math.sin(inner_angle), "inner"))

        texts_html = ""
        for idx, (px, py, point_type) in enumerate(points):
            number, count = numbers_with_counts[idx]
            static_text = ",".join([number] * count) if count > 0 else ""
            
            shift_idx = (idx - 1 + current_t) % 10
            number1, count1 = numbers_with_counts[shift_idx]
            dy_text = f"({','.join([number1] * count1)})" if count1 > 0 else ""

            # 計算該頂點與中心的角度
            angle = math.atan2(py - center_y, px - center_x)
            
            # 【關鍵修改 3：根據是內角還是外角，給予不同的延伸距離】
            current_offset = offset_outer if point_type == "outer" else offset_inner
            
            # 算出文字的最終圓心座標
            base_x = px + current_offset * math.cos(angle)
            base_y = py + current_offset * math.sin(angle)

            # 將兩層文字錯開，避免重疊
            if dy_text:
                texts_html += f'<text x="{base_x}" y="{base_y - 10}" class="dynamic-num">{dy_text}</text>\n'
            if static_text:
                texts_html += f'<text x="{base_x}" y="{base_y + 10}" class="static-num">{static_text}</text>\n'

        if b64_image:
            image_html = f'<img src="data:image/png;base64,{b64_image}" class="bg-star" />'
        else:
            image_html = f'<circle cx="{center_x}" cy="{center_y}" r="150" fill="#2a2d4a" />'

        star_html = f"""
        <div class="star-container">
            <div class="visual-wrapper">
                {image_html}
                <svg class="overlay-svg" width="{svg_size}" height="{svg_size}" viewBox="0 0 {svg_size} {svg_size}">
                    <defs>
                        <filter id="glow">
                            <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
                            <feMerge>
                                <feMergeNode in="coloredBlur"/>
                                <feMergeNode in="SourceGraphic"/>
                            </feMerge>
                        </filter>
                    </defs>
                    {texts_html}
                    <circle cx="{center_x}" cy="{center_y}" r="20" fill="#000000" stroke="#E2E8F0" stroke-width="1.5"/>
                    <text x="{center_x}" y="{center_y}" class="center-text" dy="0.35em">T {current_t}</text>
                </svg>
            </div>
            <div class="stage-label">Phase {trans + 1}</div>
        </div>
        """
        stars_html += star_html

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600&family=Noto+Sans+TC:wght@500;700&display=swap" rel="stylesheet">
        <style>
            body {{
                background-color: #000000; 
                margin: 0; padding: 20px 0;
                display: flex; justify-content: flex-start; overflow-x: auto;
            }}
            .flex-wrapper {{ display: flex; gap: 30px; padding: 10px 20px; }}
            .star-container {{
                display: flex; flex-direction: column; align-items: center;
                background-color: #000000; 
                border-radius: 20px; padding: 20px;
                border: none; box-shadow: none; 
            }}
            .visual-wrapper {{
                position: relative; width: {svg_size}px; height: {svg_size}px;
            }}
            .bg-star {{
                position: absolute; 
                top: 18%; left: 18%;
                width: 64%; height: 64%; 
                object-fit: contain;
                filter: drop-shadow(0px 10px 15px rgba(0,0,0,0.8));
            }}
            .overlay-svg {{ position: absolute; top: 0; left: 0; z-index: 10; }}
            
            text {{ font-family: 'Fredoka', 'Noto Sans TC', sans-serif; text-anchor: middle; dominant-baseline: middle; }}
            .dynamic-num {{ fill: #FF6B6B; font-size: 16px; font-weight: 600; letter-spacing: 1px; filter: url(#glow); }}
            .static-num {{ fill: #F9E596; font-size: 18px; font-weight: 500; letter-spacing: 1px; }}
            
            .center-text {{ fill: #E2E8F0; font-size: 13px; font-weight: 600; letter-spacing: 1px; }}
            .stage-label {{ color: #A0AEC0; font-family: 'Fredoka', sans-serif; font-size: 18px; margin-top: 15px; letter-spacing: 2px; text-transform: uppercase; }}
            
            ::-webkit-scrollbar {{ height: 10px; }}
            ::-webkit-scrollbar-track {{ background: #000000; border-radius: 5px; }}
            ::-webkit-scrollbar-thumb {{ background: #4A5568; border-radius: 5px; }}
        </style>
    </head>
    <body><div class="flex-wrapper">{stars_html}</div></body>
    </html>
    """
    return full_html

# ==========================================
# 3. Streamlit 網頁 UI
# ==========================================
st.set_page_config(page_title="身體自覺五星術", layout="wide", page_icon="🌟")

st.markdown("""
<style>
    .stApp { background-color: #000000; color: #E2E8F0; }
    h1 { color: #F9E596; font-family: '微軟正黑體', sans-serif; }
    .stTextInput>div>div>input { background-color: #1A1C29; color: #F9E596; border: 1px solid #4A5568; }
</style>
""", unsafe_allow_html=True)

st.title("🌟 身體自覺五星術分析系統")

col1, col2 = st.columns([1, 3])

with col1:
    birthday = st.text_input("輸入生日 (YYYYMMDD)", value="19901020", max_chars=8)
    run_btn = st.button("開始分析與生成", type="primary", use_container_width=True)
    
    img_path = "STAR.jpg"
    if os.path.exists(img_path):
         st.success(" ")
    else:
         st.warning(f"⚠️ 找不到 `{img_path}`。請確保圖片與程式碼放在同一資料夾。")

if run_btn:
    if len(birthday) == 8 and birthday.isdigit():
        try:
            valid_date = datetime.strptime(birthday, "%Y%m%d")
            
            res, start_t, num_trans = calculate_star_type(birthday)
            counts = analyze_date_code(birthday)
            counts = modify_code(birthday, counts)
            
            with col1:
                st.markdown("### 📋 數據報告")
                for key, val in res.items():
                    st.info(f"**{key}**: {val}")
            
            with col2:
                st.markdown(" ")
                b64_img = get_image_as_base64(img_path)
                html_content = generate_stars_html(start_t, counts, num_trans, b64_img)
                components.html(html_content, height=750, scrolling=True)
                
        except ValueError:
            st.error("❌ 日期無效：請輸入真實存在的日期。")
    else:
        st.error("❌ 格式錯誤：請輸入 8 位數字的生日，例如 19851020")
