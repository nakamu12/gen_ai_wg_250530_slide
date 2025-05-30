#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
from pathlib import Path

def create_slide_files():
    """各スライドのHTMLファイルを手動で作成"""
    
    base_dir = Path('/Users/nakamurar39/Desktop/codes/presentations/250530_gen_ai_wg')
    pages_dir = base_dir / 'pages'
    
    # 既存のファイルをクリーンアップ
    for file in pages_dir.glob("*.html"):
        if file.name.startswith(("01_", "02_", "03_", "04_", "05_", "06_", "07_", "08_", "09_", "10_", 
                                "11_", "12_", "13_", "14_", "15_", "16_", "17_", "18_", "19_")):
            file.unlink()
    
    # 元のHTMLファイルを読み込み
    with open(base_dir / 'index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 各スライドの情報を定義
    slides_info = [
        ("01_cover.html", "カバー", r'<div class="slide active cover-slide" id="s01_cover">(.*?)(?=<div class="slide-number">1 / 17</div>)', "1 / 18"),
        ("02_agenda.html", "アジェンダ", r'<div class="slide" id="s02_agenda">(.*?)(?=<div class="slide-number">2 / 17</div>)', "2 / 18"),
        ("03_genai_definition.html", "生成AIとは", r'<div class="slide" id="s03_genai_definition">(.*?)(?=<div class="slide-number">3 / 18</div>)', "3 / 18"),
        ("04_context_window.html", "コンテキストウィンドウ", r'<div class="slide" id="s04_context_window">(.*?)(?=<div class="slide-number">4 / 18</div>)', "4 / 18"),
        ("05_llm.html", "LLM", r'<div class="slide" id="s05_llm">(.*?)(?=<div class="slide-number">5 / 17</div>)', "5 / 18"),
        ("06_strength_weak.html", "得意・苦手", r'<div class="slide" id="s06_strength_weak">(.*?)(?=<div class="slide-number">5 / 17</div>)', "6 / 18"),
        ("07_tools_overview.html", "ツール比較", r'<div class="slide" id="s07_tools_overview">(.*?)(?=<div class="slide-number">6 / 17</div>)', "7 / 18"),
        ("08_chatgpt.html", "ChatGPT", r'<div class="slide" id="s08_chatgpt">(.*?)(?=<div class="slide-number">7 / 17</div>)', "8 / 18"),
        ("09_gemini.html", "Gemini", r'<div class="slide" id="s09_gemini">(.*?)(?=<div class="slide-number">8 / 17</div>)', "9 / 18"),
        ("10_claude.html", "Claude", r'<div class="slide" id="s10_claude">(.*?)(?=<div class="slide-number">9 / 17</div>)', "10 / 18"),
        ("11_bolt.html", "Bolt", r'<div class="slide" id="s11_bolt">(.*?)(?=<div class="slide-number">10 / 17</div>)', "11 / 18"),
        ("12_dify.html", "Dify", r'<div class="slide" id="s12_dify">(.*?)(?=<div class="slide-number">11 / 17</div>)', "12 / 18"),
        ("13_change_3years.html", "過去3年の変化", r'<div class="slide" id="s13_change_3years">(.*?)(?=<div class="slide-number">12 / 17</div>)', "13 / 18"),
        ("14_research.html", "AGI予測", r'<div class="slide" id="s14_research">(.*?)(?=<div class="slide-number">13 / 17</div>)', "14 / 18"),
        ("15_catchup.html", "キャッチアップ", r'<div class="slide" id="s15_catchup">(.*?)(?=<div class="slide-number">14 / 17</div>)', "15 / 18"),
        ("16_mastery_steps.html", "活用ステップ", r'<div class="slide" id="s16_mastery_steps">(.*?)(?=<div class="slide-number">15 / 17</div>)', "16 / 18"),
        ("17_key_takeaway.html", "まとめ", r'<div class="slide" id="s17_key_takeaway">(.*?)(?=<div class="slide-number">16 / 17</div>)', "17 / 18"),
        ("18_question.html", "質疑応答", r'<div class="slide" id="s18_question">(.*?)(?=<div class="slide-number">17 / 17</div>)', "18 / 18")
    ]
    
    for filename, title, pattern, slide_num in slides_info:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            slide_content = match.group(1).strip()
            
            # HTMLテンプレートを作成
            html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>生成AIが変える未来 - {title}</title>
    <link rel="stylesheet" href="../styles/main.css">
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
        }}
        .slide {{
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
        }}
        .slide-number {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            font-size: 1em;
            color: rgba(255,255,255,0.6);
        }}
    </style>
</head>
<body>
    <div class="slide">
        {slide_content}
        <div class="slide-number">{slide_num}</div>
    </div>
    
    <!-- Chart.js CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    
    <script>
        // revealSecret function for question slide
        function revealSecret() {{
            const revealContent = document.getElementById('revealContent');
            const confetti = document.getElementById('confetti');
            const fireworks = document.getElementById('fireworks');
            
            if (revealContent) {{
                revealContent.style.display = 'block';
                revealContent.style.animation = 'slideDown 0.5s ease-out';
            }}
            
            if (confetti) {{
                confetti.style.display = 'block';
                createConfetti();
            }}
            
            if (fireworks) {{
                fireworks.style.display = 'block';
                createFireworks();
            }}
        }}
        
        function createConfetti() {{
            console.log('Confetti created');
        }}
        
        function createFireworks() {{
            console.log('Fireworks created');
        }}
    </script>
</body>
</html>"""
            
            # ファイルに保存
            output_path = pages_dir / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_template)
            
            print(f"作成しました: {filename}")
        else:
            print(f"パターンが見つかりませんでした: {filename}")

if __name__ == "__main__":
    create_slide_files()
    print("\\nスライドファイルの作成が完了しました。")
