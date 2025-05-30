#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
from pathlib import Path

def extract_slides_from_html(html_content):
    """元のHTMLからスライドコンテンツを抽出"""
    # スライドパターンにマッチする正規表現
    slide_pattern = r'<div class="slide[^>]*?id="([^"]+)"[^>]*?>(.*?)(?=<div class="slide|<\/div>\s*<div class="controls">)'
    
    matches = re.findall(slide_pattern, html_content, re.DOTALL)
    return matches

def create_slide_html(slide_id, content, slide_number):
    """個別のスライドHTMLファイルを生成"""
    template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>生成AIが変える未来 - {slide_id}</title>
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
        {content.strip()}
    </div>
    
    <!-- Chart.js CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    
    <!-- スライド固有のスクリプト -->
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
            // Confetti animation logic
            console.log('Confetti created');
        }}
        
        function createFireworks() {{
            // Fireworks animation logic  
            console.log('Fireworks created');
        }}
    </script>
</body>
</html>"""
    return template

def main():
    # 元のHTMLファイルを読み込み
    base_dir = Path('/Users/nakamurar39/Desktop/codes/presentations/250530_gen_ai_wg')
    html_file = base_dir / 'index.html'
    pages_dir = base_dir / 'pages'
    
    # pagesディレクトリが存在しない場合は作成
    pages_dir.mkdir(exist_ok=True)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # スライドを抽出
    slides = extract_slides_from_html(html_content)
    
    # 各スライドファイルを作成
    for i, (slide_id, content) in enumerate(slides, 1):
        # ファイル名を生成（例: 01_cover.html）
        clean_id = slide_id.replace('s' + str(i).zfill(2) + '_', '')
        filename = f"{str(i).zfill(2)}_{clean_id}.html"
        
        # HTMLコンテンツを生成
        html_content = create_slide_html(slide_id, content, i)
        
        # ファイルに書き込み
        output_file = pages_dir / filename
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"作成しました: {filename}")
    
    print(f"\\n合計 {len(slides)} 個のスライドファイルを作成しました。")

if __name__ == "__main__":
    main()
