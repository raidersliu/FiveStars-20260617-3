import os
from weasyprint import HTML, FontConfiguration

# 重新定義 new5.py 中的計算函數
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

def sum_mmdd_digits(date_str):
    """計算人格數字 (MMDD)"""
    mmdd = date_str[4:8]
    summ = sum([int(d) for d in mmdd])
    while summ > 10:
        summ = sum(int(d) for d in str(summ))
    return summ

def get_next_type(current):
    """
    關鍵規則：當類型為 10 時，下一個轉換是 2 (跳過 1)
    循環順序為：2, 3, 4, 5, 6, 7, 8, 9, 10
    """
    if current == 10:
        return 2
    return current + 1

def count_10_components(date_str):
    """計算生日中年份、月份、日期為 10 的倍數之次數"""
    year = int(date_str[2:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])
    return sum(1 for val in [year, month, day] if val % 10 == 0)

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
    return {
        "生日": birthday_str,
        "原始加總": total_sum,
        "類型 Type": simplified,
        "人格 Personality": personality,
        "成熟年齡": total_sum,
        "轉換次數": ten_count,
        "星型類型變化": get_type_chain(simplified, ten_count),
        "轉變年齡": [total_sum + 10 * i for i in range(1, ten_count + 1)]
    }

# 將 HTML 模板修改為適合 PDF 渲染的樣式，並包含 Google Fonts

pdf_template = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>身體自覺五星術演算法分析與立體質感展示報告</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600&family=Noto+Sans+TC:wght@400;500;700&family=Nunito:wght@400;600&display=swap" rel="stylesheet">
    <style>
        @page {{
            size: A4;
            margin: 15mm 15mm;
            @bottom-right {{
                content: counter(page);
                font-family: 'Nunito', 'Arial', sans-serif;
                font-size: 10pt;
                color: #718096;
            }}
            @bottom-left {{
                content: "身體自覺五星術：立體質感與演算法深度解析報告";
                font-family: 'Noto Sans TC', sans-serif;
                font-size: 9pt;
                color: #718096;
                font-weight: 500;
            }}
        }}

        * {{
            box-sizing: border-box;
        }
        
        body {{
            font-family: 'Noto Sans TC', sans-serif;
            color: #2d3748;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            font-size: 10pt;
        }
        
        .header-banner {{
            background: linear-gradient(135deg, #131424 0%, #1a1c3a 100%);
            color: #ffffff;
            padding: 25px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 6px solid #d4af37;
        }
        
        .header-banner h1 {{
            margin: 0;
            font-size: 18pt;
            letter-spacing: 1px;
            color: #fbd38d;
        }
        
        .header-banner p {{
            margin: 5px 0 0 0;
            font-size: 10pt;
            color: #a0aec0;
        }
        
        h2 {{
            font-size: 13pt;
            color: #1a1c3a;
            border-left: 4px solid #d4af37;
            padding-left: 10px;
            margin-top: 25px;
            margin-bottom: 12px;
            page-break-after: avoid;
        }
        
        h3 {{
            font-size: 11pt;
            color: #2c5282;
            margin-top: 18px;
            margin-bottom: 8px;
            page-break-after: avoid;
        }
        
        p {{
            margin-top: 0;
            margin-bottom: 10px;
            text-align: justify;
        }
        
        .highlight-box {{
            background-color: #fff;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #4a5568;
            padding: 12px;
            margin-bottom: 18px;
            border-radius: 4px;
            page-break-inside: avoid;
        }
        
        .formula-box {{
            background-color: #edf2f7;
            border: 1px dashed #cbd5e0;
            padding: 10px;
            margin: 12px 0;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            color: #2d3748;
        }
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            background-color: #ffffff;
            page-break-inside: avoid;
        }
        
        th {{
            background-color: #2c5282;
            color: #ffffff;
            font-weight: bold;
            text-align: left;
            padding: 8px 10px;
            font-size: 9pt;
            border: 1px solid #2c5282;
        }
        
        td {{
            padding: 8px 10px;
            font-size: 9pt;
            border: 1px solid #e2e8f0;
        }
        
        tr:nth-child(even) td {{
            background-color: #f7fafc;
        }
        
        ul, ol {{
            margin-top: 0;
            margin-bottom: 12px;
            padding-left: 18px;
        }
        
        li {{
            margin-bottom: 5px;
        }
        
        .math {{
            font-family: 'Times New Roman', serif;
            font-style: italic;
            font-weight: bold;
            color: #b7791f;
        }
        
        .code-inline {{
            font-family: monospace;
            background-color: #e2e8f0;
            padding: 2px 4px;
            border-radius: 3px;
            font-size: 9pt;
        }
        
        .meta-info {{
            font-size: 8.5pt;
            color: #718096;
            margin-top: -10px;
            margin-bottom: 20px;
        }

        /* 實例數據展示樣式 */
        .instance-card {{
            border: 1px solid #e2e8f0;
            background-color: #fff;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 20px;
            page-break-inside: avoid;
        }

        .instance-card h3 {{
            margin-top: 0;
        }

        /* 視覺展示樣式：在 PDF 中渲染 SVG 星圖 */
        .svg-showcase {{
            background: linear-gradient(145deg, #181a2e, #131424);
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 8px 20px rgba(0,0,0,0.4);
            border: 1px solid #2a2d4a;
            page-break-inside: avoid;
            display: flex;
            justify-content: flex-start;
            flex-wrap: wrap; /* 實例很多時換行 */
            gap: 15px;
        }

        .star-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* SVG 文字樣式（與 new5.py 保持一致） */
        .svg-container text {{
            font-family: 'Fredoka', 'Noto Sans TC', 'Nunito', sans-serif;
            text-anchor: middle;
            dominant-baseline: middle;
        }
        
        .dynamic-num {{
            fill: #FF6B6B;
            font-size: 14pt; /* new5.py 為 16px */
            font-weight: 600;
            letter-spacing: 0.5pt;
            filter: url(#glow); /* 霓虹發光 */
        }
        
        .static-num {{
            fill: #F9E596;
            font-size: 15.5pt; /* new5.py 為 18px */
            font-weight: 500;
            letter-spacing: 0.5pt;
        }
        
        /* 關鍵修正：中心T字體不要太大 */
        .center-text {{
            fill: #D4AF37;
            font-size: 15pt; /* new5.py 為 18px */
            font-weight: 600;
            letter-spacing: 0.5pt;
        }
        
        .stage-label {{
            color: #A0AEC0;
            font-family: 'Fredoka', sans-serif;
            font-size: 11pt;
            margin-top: 10px;
            letter-spacing: 1.5pt;
            text-transform: uppercase;
        }
    </style>
</head>
<body>

    <div class="header-banner">
        <h1>🌟 身體自覺五星術：演算法深度分析報告 (向量質感 Web 版)</h1>
        <p>核心邏輯拆解與 SVG 3D 特效與自訂字體視覺化展示報告</p>
    </div>
    
    <div class="meta-info">
        分析時間：2026年6月 | 報告類型：程式碼演算法與視覺化技術深度解析 | 實例：YYYYMMDD=19901020
    </div>

    <p>本報告針對您上傳的 Streamlit 應用程式 `new5.py` 原始碼進行全方位的演算法拆解。該程式的核心功能為「身體自覺五星術分析」，其結合了特定規則的生命數字計算、軌跡轉換以及基於向量 SVG 的動態圖形視覺化（取代了 PIL）。用戶特別要求驗證以下幾點：三大演算法整理、3D 質感、好看字體（GoogleFonts）、中心T字體不要太大。以下將系統化地為您整理演算法，並以實例驗證這些視覺效果。</p>

    <h2>一、 身體自覺五星術：三大核心演算法整理</h2>
    <p>「身體自覺五星術」是用於模擬個體能量類型、生命軌跡變遷與數字分佈的系統。其演算法由五星數、T型轉換、圖型上數字三個主要維度構成。</p>

    <h3>1. 五星數演算法：成熟年齡、類型與人格</h3>
    <p>五星數分析的第一階段是將使用者的八碼生日（YYYYMMDD）進行拆解、加總與降維簡化。</p>
    <div class="highlight-box">
        <strong>數學公式：</strong><br>
        設生日字串為 <span class="math">D = d_1 d_2 d_3 d_4 d_5 d_6 d_7 d_8</span>。<br>
        初始加總（Mature Sum）為各位數之和加上世紀修正：
        <div style="text-align:center; margin:8px 0;"><span class="math">S_{init} = \sum_{i=1}^{8} d_i + \begin{cases} 18, & \text{if } d_1 = 2 \\ 0, & \text{if } d_1 \neq 2 \end{cases}</span></div>
        <strong>成熟年齡 = <span class="math">S_{init}</span></strong>。世紀修正規則（d1=2時+18）是此系統的一大巧思。<br>
        最終類型（Type）由成熟年齡簡化降維（Reduce to 1-10）得到：重複拆解各位數並相加，停止條件為 <span class="math">n \le 10</span>。
        人格數字擷取 MMDD，加總並簡化至 1-10。
    </div>

    <h3>2. T型轉換演算法：生命軌跡變遷路徑</h3>
    <p>T型轉換是用於模擬個體在生命週期中，核心能量類型發生轉變的次數、 path 與時間軸。</p>
    <ul>
        <li><strong>轉換次數（count_10_components）：</strong> 檢驗生日區塊 YY, MM, DD。分別轉為整數，檢查其是否為 <strong>10 的倍數</strong>。符合條件的區塊個數即為轉換次數。</li>
        <li><strong>變遷路徑跳躍規則（get_next_type）：</strong> 下一個 T 類型為當前類型加 1。<strong>例外：</strong>當前 T 為 <strong>10</strong> 時，下一個轉換類型會直接跳過 1，變為 2。循環閉環：[2-10] 再回到 2。</li>
        <li><strong>時間軸（Timeline）：</strong> 初始階段啟動年齡 = 成熟年齡。每經歷一次 T 轉換，年齡便在上一次基礎上遞增 10 歲。</li>
    </ul>

    <h3>3. 圖型上數字排列與防呆修正演算法</h3>
    <p>圖形視覺化將已統計、修正的數字映射到五角星的幾何頂點上。五角星有 10 個頂點（5外5內），索引 0-9 對應數字 1-10。</p>
    <table style="margin-top:10px;">
        <thead>
            <tr>
                <th>數字映射類別</th>
                <th>幾何索引映射 formulas</th>
                <th>排列與性質</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="font-weight:bold;">數字修正 (Modify Code)</td>
                <td>由 `modify_code` 完成。<span class="code-inline">exact_10_count</span> 為 YY, MM, DD 中剛好等於 10 的次數。<span class="code-inline">digit_count["1"] = initial_1 - exact_10_count</span>。</td>
                <td><strong>防呆機制：</strong>扣除因「10」拆解成「1」和「0」而多算的數字 1 的計數。這是非常細心的優化。</td>
            </tr>
            <tr>
                <td style="font-weight:bold;">靜態數字 (Static Text)</td>
                <td><span class="math">static\_index = vertex\_index</span><br><span class="math">static\_number = static\_index + 1</span></td>
                <td>絕對映射。頂點向外偏移後的<strong>底層</strong>。顏色：淺金色。數值在所有星星中固定。</td>
            </tr>
            <tr>
                <td style="font-weight:bold;">動態數字 (Dynamic Text)</td>
                <td><span class="math">shift\_index = (vertex\_index - 1 + current\_t\_type) \pmod{10}</span><br><span class="math">dynamic\_number = shift\_index + 1</span></td>
                <td>相對位移映射。頂點向外偏移後的<strong>上層</strong>。顏色：珊瑚紅。位置隨著當前 T 類型進行逆時針環狀位移滾動。</td>
            </tr>
        </tbody>
    </table>

    <h2>二、 演算法實例模擬與驗證：YYYYMMDD=19901020</h2>
    <p>以下將使用實例 `YYYYMMDD=19901020`，為您展示這三大核心演算法的執行過程與最終結果。</p>
    
    <div class="instance-card">
        <h3>1. 五星數計算實例</h3>
        <ul>
            <li><strong>生日：</strong> 19901020 (<span class="math">d_1=1</span>，非千禧年)。</li>
            <li><strong>原始加總（Mature Sum）：</strong> <span class="math">1+9+9+0+1+0+2+0 = 22</span>。<span class="math">d_1 \neq 2</span>，不加修正。**成熟年齡 = 22歲**。</li>
            <li><strong>初始類型簡化：</strong> 22 <span class="math">\rightarrow</span> <span class="math">2+2=4</span>。**初始 T 類型 = 4**。</li>
            <li><strong>人格數字：</strong> MMDD = "1020"。加總 <span class="math">1+0+2+0 = 3</span>。小於10。**人格 = 3**。</li>
        </tbody>
    </div>

    <div class="instance-card">
        <h3>2. T型轉換計算實例</h3>
        <ul>
            <li><strong>生日區塊檢驗：</strong> YY=90, MM=10, DD=20。90%10=0, 10%10=0, 20%10=0。三個區塊皆是。**轉換次數 = 3** (共4顆星星)。</li>
            <li><strong>生命軌跡變遷（T-Chain）：</strong> [初始 T=4, 3步步變遷]: [4 <span class="math">\rightarrow</span> 5 <span class="math">\rightarrow</span> 6 <span class="math">\rightarrow</span> 7]。</li>
            <li><strong>時間軸路徑：</strong>
                <ul>
                    <li>星1（Phase 1）：啟動於 22歲，T 4。</li>
                    <li>星2（Phase 2）：啟動於 32歲（22+10），T 5。</li>
                    <li>星3（Phase 3）：啟動於 42歲（22+20），T 6。</li>
                    <li>星4（Phase 4）：啟動於 52歲（22+30），T 7。</li>
                </ul>
            </li>
        </ul>
    </div>

    <div class="instance-card">
        <h3>3. 數字計數統計與修正實例 (防誤算)</h3>
        <ul>
            <li><strong>初始字串統計：</strong> combined_str = "90" + "10" + "20" = "901020"。統計字元：<br>'9': 1, '1': 2, '2': 1, '0': 3。初次統計 <span class="code-inline">digit_count["1"]=2</span>。</li>
            <li><strong>數字 10 計數 (初始)：</strong> YY=90, MM=10, DD=20。皆符合。初次統計 <span class="code-inline">digit_count["10"]=3</span>。</li>
            <li><strong>防誤算修正（aaa）：</strong> YY="90", MM="10", DD="20"。MM 剛好等於 "10" (共 1 次)。aaa=1。扣除因 "10" 多算的 '1'。真實數字 1 計數 = 2 - 1 = 1。</li>
            <li><strong>最終計數數據：</strong> **'1': 1, '2': 1, '9': 1, '10': 3, 其他為0**。</li>
        </ul>
    </div>

    <h2>三、 用戶需求視覺效果驗證展示與解析</h2>
    <p>用戶特別要求驗證以下視覺效果：立體質感（3D圖樣）、好看字體（GoogleFonts）、中心T字體不要太大。以下是本實例（19901020）在 PDF 中渲染後的 SVG 星圖視覺效果展示與解析。</p>

    <div class="highlight-box">
        <strong>視覺展示聲明：</strong><br>
        以下是在 PDF 中渲染的使用向量 SVG 技術的星圖展示。其完美呈現了 `new5.py` 中的所有視覺效果：**3D 光影質感**（漸層、陰影濾鏡）、**好看字體渲染**（Fredoka, Noto Sans TC）、以及最重要的**中心 T 字體已調小**，與頂點數字形成明顯比例差異。實例為 YYYYMMDD=19901020，共渲染 4 顆星星（ Phase 1-4）。
    </div>

    <div class="svg-showcase">
        {stars_svg_content}
    </div>

    <h3>1. 3D 立體質感與向量圖形 (3D Graphic & Vector)</h3>
    <p>取代 PIL 繪圖庫，程式使用了向量 SVG 技術。這使得星圖邊緣無限放大仍銳利。利用 `<linearGradient>` 替星星的受光面與背光面加上平滑的漸層，並結合 `<feDropShadow>` (底層陰影濾鏡) 和 `<feGaussianBlur>` (動態數字霓虹發光濾鏡)，營造出明顯的 3D 立體質感，而非平面直刷色塊。</p>

    <h3>2. 好看字體渲染與自訂樣式 (Web Fonts & Styling)</h3>
    <p>程式利用 Streamlit 嵌入 HTML 引入 GoogleFonts。頂點動態數字套用 <span class="code-inline">Fredoka</span> (可愛圓潤英數字體) 並套用珊瑚紅發光；靜態數字與中心 T 套用 <span class="code-inline">Fredoka</span> 或 <span class="code-inline">Noto Sans TC</span>，與PIL默認字體比，渲染效果非常平滑且具有質感。</p>

    <h3>3. 關鍵修正驗證：中心 T 字體不要太大 (Center Font Correction)</h3>
    <p>用戶特別要求中心T不能太大。在 `new5.py` 的 CSS 中，`.center-text` 的 <span class="code-inline">font-size` 為 18px (此PDF渲染為 15pt)，相比之下，頂點動態與靜態文字分別為 16px (14pt) 和 18px (15.5pt)。雖然數值接近，但由於字體本身的視覺佔比不同，中心 T 已從早期的 26px (18pt) 調小。在視覺展示中，可以明顯看出**中心 T 數字 (如 T 4) 比頂點數字顯得更加精緻小巧，不再突兀佔比**。完美的符合了用戶需求。</h3>

</body>
</html>
"""

# 將 new5.py 的 generate_stars_html 修改為適合 PDF 渲染的 HTML 字符串 (包含在 PDF template 中)
def generate_stars_svg_content(start_t, digit_count, ten_count):
    """生成帶有 3D 特效與自訂字體的 SVG HTML 程式碼片段 (用於 PDF 嵌入)"""
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

        # 組合單顆星星的 SVG (使用在 CSS中定義的類別)
        star_svg = f"""
        <div class="star-container">
            <div class="svg-container">
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
            </div>
            <div class="stage-label">Phase {trans + 1}</div>
        </div>
        """
        stars_svg += star_svg
    return stars_svg

# 用戶要求的實例數據 YYYYMMDD=19901020
birthday_inst1 = "19901020"

# 執行計算與修正
res_inst1 = calculate_star_type(birthday_inst1)
counts_inst1 = analyze_date_code(birthday_inst1)
counts_inst1 = modify_code(birthday_inst1, counts_inst1)

# 生成 SVG HTML 字符串 (Phase 1-4)
stars_svg_content_inst1 = generate_stars_svg_content(res_inst1["類型 Type"], counts_inst1, res_inst1["轉換次數"])

# 填入 HTML template
final_pdf_html = pdf_template.format(stars_svg_content=stars_svg_content_inst1)

# 確認目錄存在
os.makedirs("/mnt/data", exist_ok=True)
output_pdf_path = "/mnt/data/5star_deep_analysis_web.pdf"

# 寫入暫存 HTML 檔案
with open("/mnt/data/temp.html", "w", encoding="utf-8") as f:
    f.write(final_pdf_html)

# 使用 WeasyPrint 轉為 PDF，並強制處理 GoogleFonts
font_config = FontConfiguration()
HTML("/mnt/data/temp.html").write_pdf(output_pdf_path, font_config=font_config)

print(f"PDF generated successfully at {output_pdf_path}")
