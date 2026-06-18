
import streamlit as st
import streamlit.components.v1 as components
import math
from datetime import datetime

# ==========================================
# 核心計算邏輯 (演算法保持嚴謹的數學邏輯)
# ==========================================
def split_and_sum(date_str):
    """計算生日數字總和，若為2開頭則加18"""
    digits = [int(ch) for ch in date_str if ch.isdigit()]
    total = sum(digits)
    if date_str[0] == '2':
        total += 18
    return digits, total

def reduce_to_single_digit(n):
    """將數字簡化至 1-10 之間"""
    while n > 10:
        n = sum(int(d) for d in str(n))
    return n

def get_next_type(current):
    """
    關鍵規則：當類型為 10 時，下一個轉換是 2 (跳過 1)
    循環順序為：2, 3, 4, 5, 6, 7, 8, 9, 10
    """
    if current == 10:
        return 2
    return current + 1

def get_type_chain(start_type, steps):
    """計算星型類型變化序列"""
    chain = []
    curr = start_type
    for _ in range(steps):
        curr = get_next_type(curr)
        chain.append(curr)
    return chain

def count_10_components(date_str):
    """計算生日中年份、月份、日期為 10 的倍數之次數"""
    year = int(date_str[2:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])
    return sum(1 for val in [year, month, day] if val % 10 == 0)

def sum_mmdd_digits(date_str):
    """計算人格數字 (MMDD)"""
    mmdd = date_str[4:8]
    summ = sum([int(d) for d in mmdd])
    while summ > 10:
        summ = sum(int(d) for d in str(summ))
    return summ

def analyze_date_code(date_str):
    """統計生日碼中各個數字出現次數 (1-10)"""
    yy, mm, dd = date_str[2:4], date_str[4:6], date_str[6:8]
    combined_digits = yy + mm + dd
    digit_count = {str(i): 0 for i in range(1, 11)}
    for ch in combined_digits:
        if ch in digit_count:
            digit_count[ch] += 1
    # 統計 10 的數量
    digit_count["10"] = sum(1 for x in [yy, mm, dd] if int(x) % 10 == 0)
    return digit_count

def modify_code(date_str, digit_count):
    """修正 1 的計數（若有 10 出現，需扣除誤算的 1）"""
    yy, mm, dd = int(date_str[2:4]), int(date_str[4:6]), int(date_str[6:8])
    aaa = sum(1 for v in [yy, mm, dd] if v == 10)
    digit_count["1"] = str(int(digit_count["1"]) - aaa)
    return digit_count

def calculate_star_type(birthday_str):
    """統整所有分析數據"""
    digits, total_sum = split_and_sum(birthday_str)
    simplified = reduce_to_single_digit(total_sum)
    ten_count = count_10_components(birthday_str)
    personality = sum_mmdd_digits(birthday_str)
    result = {
        "生日": birthday_str,
        "原始加總": total_sum,
        "轉換次數": ten_count,
        "類型 Type": simplified,
        "人格 Personality": personality,
        "星型類型變化": get_type_chain(simplified, ten_count)
    }
    return result, simplified, ten_count

# ==========================================
# 網頁視覺化生成器 (SVG 向量 + CSS 特效)
# ==========================================
def generate_stars_html(start_t, digit_count, ten_count):
    """生成帶有 3D 特效與自訂字體的 SVG HTML 程式碼"""
    
    # 準備數字計數資料
    numbers_with_counts = [(str(i), int(digit_count[str(i)])) for i in range(1, 11)]
    
    stars_svg = ""
    current_t = start_t
    
    # SVG 畫布設定
    svg_size = 460
    center_x, center_y = svg_size / 2, svg_size / 2
    radius_outer = 140
    radius_inner = 55
    label_offset = 35  # 數字偏移量

    for trans in range(ten_count + 1):
        if trans > 0:
            current_t = get_next_type(current_t)
            
        points = []
        # 計算五角星的十個頂點
        for i in range(5):
            outer_angle = math.radians(90 + i * 72)
            inner_angle = math.radians(90 + i * 72 + 36)
            points.append((center_x + radius_outer * math.cos(outer_angle),
                           center_y - radius_outer * math.sin(outer_angle)))
            points.append((center_x + radius_inner * math.cos(inner_angle),
                           center_y - radius_inner * math.sin(inner_angle)))

        polygons_html = ""
        # 繪製底層陰影
        shadow_pts = " ".join([f"{x+12},{y+12}" for x, y in points])
        polygons_html += f'<polygon points="{shadow_pts}" fill="#080910" filter="url(#drop-shadow)"/>\n'

        # 繪製 3D 光影切面 (受光與背光)
        for i in range(5):
            outer_idx = 2 * i
            inner_prev_idx = (2 * i - 1) % 10
            inner_next_idx = (2 * i + 1) % 10
            
            p_center = f"{center_x},{center_y}"
            p_outer = f"{points[outer_idx][0]},{points[outer_idx][1]}"
            p_prev = f"{points[inner_prev_idx][0]},{points[inner_prev_idx][1]}"
            p_next = f"{points[inner_next_idx][0]},{points[inner_next_idx][1]}"
            
            # 受光面 (亮金漸層)
            polygons_html += f'<polygon points="{p_center} {p_prev} {p_outer}" fill="url(#light-gold)" stroke="#FFF8DC" stroke-width="0.5"/>\n'
            # 背光面 (暗金漸層)
            polygons_html += f'<polygon points="{p_center} {p_outer} {p_next}" fill="url(#dark-gold)" stroke="#FFF8DC" stroke-width="0.5"/>\n'

        # 處理頂點上的雙層文字 (動態與靜態)
        texts_html = ""
        for idx, (px, py) in enumerate(points):
            number, count = numbers_with_counts[idx]
            static_text = ",".join([number] * count) if count > 0 else ""
            
            shift_idx = (idx - 1 + current_t) % 10
            number1, count1 = numbers_with_counts[shift_idx]
            dy_text = f"({','.join([number1] * count1)})" if count1 > 0 else ""

            angle = math.atan2(py - center_y, px - center_x)
            base_x = px + label_offset * math.cos(angle)
            base_y = py + label_offset * math.sin(angle)

            if dy_text:
                texts_html += f'<text x="{base_x}" y="{base_y - 12}" class="dynamic-num">{dy_text}</text>\n'
            if static_text:
                texts_html += f'<text x="{base_x}" y="{base_y + 12}" class="static-num">{static_text}</text>\n'

        # 組合單顆星星的 SVG
        star_svg = f"""
        <div class="star-container">
            <svg width="{svg_size}" height="{svg_size}" viewBox="0 0 {svg_size} {svg_size}">
                <defs>
                    <linearGradient id="light-gold" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#FFE87C;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#FFD700;stop-opacity:1" />
                    </linearGradient>
                    <linearGradient id="dark-gold" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#DAA520;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#B8860B;stop-opacity:1" />
                    </linearGradient>
                    <filter id="drop-shadow">
                        <feDropShadow dx="0" dy="5" stdDeviation="5" flood-opacity="0.5" />
                    </filter>
                    <filter id="glow">
                        <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
                        <feMerge>
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                </defs>
                
                {polygons_html}
                {texts_html}
                
                <circle cx="{center_x}" cy="{center_y}" r="30" fill="#1A1C29" stroke="#D4AF37" stroke-width="2" filter="url(#drop-shadow)"/>
                <text x="{center_x}" y="{center_y}" class="center-text" dy="0.35em">T {current_t}</text>
            </svg>
            <div class="stage-label">Phase {trans + 1}</div>
        </div>
        """
        stars_svg += star_svg

    # 包裝成完整的 HTML 進行左右滑動排版
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600&family=Noto+Sans+TC:wght@500;700&display=swap" rel="stylesheet">
        <style>
            body {{
                background-color: transparent;
                margin: 0;
                padding: 20px 0;
                display: flex;
                justify-content: flex-start;
                overflow-x: auto;
            }}
            .flex-wrapper {{
                display: flex;
                gap: 20px;
                padding: 10px 20px;
            }}
            .star-container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                background: linear-gradient(145deg, #181a2e, #131424);
                border-radius: 20px;
                padding: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                border: 1px solid #2a2d4a;
            }}
            text {{
                font-family: 'Fredoka', 'Noto Sans TC', sans-serif;
                text-anchor: middle;
                dominant-baseline: middle;
            }}
            .dynamic-num {{
                fill: #FF6B6B;
                font-size: 16px;
                font-weight: 600;
                letter-spacing: 1px;
                filter: url(#glow); /* 霓虹發光效果 */
            }}
            .static-num {{
                fill: #F9E596;
                font-size: 18px;
                font-weight: 500;
                letter-spacing: 1px;
            }}
            /* 調整：將中心的 T 數字縮小至 18px，讓整體比例更精緻 */
            .center-text {{
                fill: #D4AF37;
                font-size: 18px; 
                font-weight: 600;
                letter-spacing: 1px;
            }}
            .stage-label {{
                color: #A0AEC0;
                font-family: 'Fredoka', sans-serif;
                font-size: 18px;
                margin-top: 15px;
                letter-spacing: 2px;
                text-transform: uppercase;
            }}
            
            /* 自訂捲軸樣式 */
            ::-webkit-scrollbar {{ height: 10px; }}
            ::-webkit-scrollbar-track {{ background: #131424; border-radius: 5px; }}
            ::-webkit-scrollbar-thumb {{ background: #4A5568; border-radius: 5px; }}
            ::-webkit-scrollbar-thumb:hover {{ background: #718096; }}
        </style>
    </head>
    <body>
        <div class="flex-wrapper">
            {stars_svg}
        </div>
    </body>
    </html>
    """
    return full_html

# ==========================================
# Streamlit 網頁 UI
# ==========================================
st.set_page_config(page_title="身體自覺五星術", layout="wide", page_icon="🌟")

st.markdown("""
<style>
    .stApp { background-color: #0F101C; color: #E2E8F0; }
    h1 { color: #F9E596; font-family: '微軟正黑體', sans-serif; }
    .stTextInput>div>div>input { background-color: #1A1C29; color: #F9E596; border: 1px solid #D4AF37; }
</style>
""", unsafe_allow_html=True)

st.title("🌟 身體自覺五星術分析系統 (Web 3D 向量版)")

col1, col2 = st.columns([1, 3])

with col1:
    birthday = st.text_input("輸入生日 (YYYYMMDD)", value="19901020", max_chars=8)
    run_btn = st.button("開始分析與生成", type="primary", use_container_width=True)

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
                st.markdown("### 🎨 能量變化軌跡 (可向右滑動查看所有階段)")
                # 產生網頁 HTML
                html_content = generate_stars_html(start_t, counts, num_trans)
                
                # 使用 Streamlit 嵌入 HTML (支援橫向捲動，高度預留 600px 確保不被裁切)
                components.html(html_content, height=600, scrolling=True)
                
        except ValueError:
            st.error("❌ 日期無效：請輸入真實存在的日期 (例如不能輸入 13 月)。")
    else:
        st.error("❌ 格式錯誤：請輸入 8 位數字的生日，例如 19851020")
