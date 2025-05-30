#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
from pathlib import Path

def extract_all_slides():
    """元のHTMLから全てのスライドを抽出してファイル作成"""
    
    base_dir = Path('/Users/nakamurar39/Desktop/codes/presentations/250530_gen_ai_wg')
    html_file = base_dir / 'index.html'
    pages_dir = base_dir / 'pages'
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # スライドの定義情報
    slides_data = [
        # (filename, title, slide_id, slide_number)
        ("01_cover.html", "カバー", "s01_cover", "1 / 18"),
        ("02_agenda.html", "アジェンダ", "s02_agenda", "2 / 18"),
        ("03_genai_definition.html", "生成AIとは", "s03_genai_definition", "3 / 18"),
        ("04_context_window.html", "コンテキストウィンドウ", "s04_context_window", "4 / 18"),
        ("05_llm.html", "LLM", "s05_llm", "5 / 18"),
        ("06_strength_weak.html", "得意・苦手", "s06_strength_weak", "6 / 18"),
        ("07_tools_overview.html", "ツール比較", "s07_tools_overview", "7 / 18"),
        ("08_chatgpt.html", "ChatGPT", "s08_chatgpt", "8 / 18"),
        ("09_gemini.html", "Gemini", "s09_gemini", "9 / 18"),
        ("10_claude.html", "Claude", "s10_claude", "10 / 18"),
        ("11_bolt.html", "Bolt", "s11_bolt", "11 / 18"),
        ("12_dify.html", "Dify", "s12_dify", "12 / 18"),
        ("13_change_3years.html", "過去3年の変化", "s13_change_3years", "13 / 18"),
        ("14_research.html", "AGI予測", "s14_research", "14 / 18"),
        ("15_catchup.html", "キャッチアップ", "s15_catchup", "15 / 18"),
        ("16_mastery_steps.html", "活用ステップ", "s16_mastery_steps", "16 / 18"),
        ("17_key_takeaway.html", "まとめ", "s17_key_takeaway", "17 / 18"),
        ("18_question.html", "質疑応答", "s18_question", "18 / 18")
    ]
    
    created_count = 0
    
    for filename, title, slide_id, slide_number in slides_data:
        output_path = pages_dir / filename
        
        # 既存ファイルがある場合はスキップ
        if output_path.exists():
            print(f"スキップ (既存): {filename}")
            continue
        
        # スライドコンテンツの抽出パターン
        if slide_id == "s01_cover":
            pattern = rf'<div class="slide active cover-slide" id="{slide_id}">(.*?)(?=<div class="slide-number">.*?</div>)'
        else:
            pattern = rf'<div class="slide" id="{slide_id}">(.*?)(?=<div class="slide-number">.*?</div>)'
        
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
        .reveal-content {{
            display: none;
        }}
        @keyframes slideDown {{
            from {{ transform: translateY(-30px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        @keyframes confetti-fall {{
            0% {{ transform: translateY(-10px) rotate(0deg); opacity: 1; }}
            100% {{ transform: translateY(100vh) rotate(360deg); opacity: 0; }}
        }}
    </style>
</head>
<body>
    <div class="slide{'cover-slide' if slide_id == 's01_cover' else ''}">
        {slide_content}
        <div class="slide-number">{slide_number}</div>
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
            
            createConfetti();
            createFireworks();
        }}
        
        function createConfetti() {{
            const confettiContainer = document.getElementById('confetti');
            if (!confettiContainer) return;
            
            for (let i = 0; i < 50; i++) {{
                const confettiPiece = document.createElement('div');
                confettiPiece.style.position = 'absolute';
                confettiPiece.style.width = '10px';
                confettiPiece.style.height = '10px';
                confettiPiece.style.backgroundColor = `hsl(${{Math.random() * 360}}, 100%, 50%)`;
                confettiPiece.style.left = Math.random() * 100 + 'vw';
                confettiPiece.style.top = '-10px';
                confettiPiece.style.borderRadius = '50%';
                confettiPiece.style.animation = `confetti-fall ${{Math.random() * 3 + 2}}s linear infinite`;
                confettiContainer.appendChild(confettiPiece);
                
                setTimeout(() => {{
                    confettiPiece.remove();
                }}, 5000);
            }}
        }}
        
        function createFireworks() {{
            console.log('Fireworks created!');
        }}
        
        // Chart initialization for change_3years slide
        if (document.getElementById('growthChart')) {{
            const ctx = document.getElementById('growthChart').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: ['GPT-1 (2018)', 'GPT-2 (2019)', 'GPT-3 (2020)', 'GPT-3.5 (2022)', 'GPT-4 (2023)', 'GPT-4o (2024)'],
                    datasets: [{{
                        label: 'パラメータ数 (億)',
                        data: [0.117, 1.5, 175, 175, 1760, 1800],
                        backgroundColor: [
                            'rgba(102, 126, 234, 0.8)',
                            'rgba(118, 75, 162, 0.8)',
                            'rgba(233, 69, 96, 0.8)',
                            'rgba(240, 147, 251, 0.8)',
                            'rgba(102, 126, 234, 0.9)',
                            'rgba(233, 69, 96, 0.9)'
                        ],
                        borderColor: [
                            'rgba(102, 126, 234, 1)',
                            'rgba(118, 75, 162, 1)',
                            'rgba(233, 69, 96, 1)',
                            'rgba(240, 147, 251, 1)',
                            'rgba(102, 126, 234, 1)',
                            'rgba(233, 69, 96, 1)'
                        ],
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{
                            display: false
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            type: 'logarithmic',
                            ticks: {{
                                color: 'rgba(255,255,255,0.8)'
                            }},
                            grid: {{
                                color: 'rgba(255,255,255,0.1)'
                            }}
                        }},
                        x: {{
                            ticks: {{
                                color: 'rgba(255,255,255,0.8)'
                            }},
                            grid: {{
                                color: 'rgba(255,255,255,0.1)'
                            }}
                        }}
                    }}
                }}
            }});
        }}
    </script>
</body>
</html>"""
            
            # ファイルに保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_template)
            
            print(f"作成しました: {filename}")
            created_count += 1
        else:
            print(f"パターンが見つかりませんでした: {filename} (id: {slide_id})")
    
    print(f"\\n合計 {created_count} 個の新しいスライドファイルを作成しました。")

if __name__ == "__main__":
    extract_all_slides()
