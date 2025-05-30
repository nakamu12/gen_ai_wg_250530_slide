#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// 元のindex.htmlを読み込み
const originalContent = fs.readFileSync('/Users/nakamurar39/Desktop/codes/presentations/250530_gen_ai_wg/index.html', 'utf8');

// スライドごとに分割するための正規表現
const slideRegex = /<div class="slide[^>]*" id="([^"]+)">([\s\S]*?)(?=<div class="slide|<\/div>\s*<div class="controls">)/g;

let matches;
const slides = [];

while ((matches = slideRegex.exec(originalContent)) !== null) {
    slides.push({
        id: matches[1],
        content: matches[2].trim()
    });
}

// 各スライドのHTMLファイルを生成
slides.forEach((slide, index) => {
    const slideNumber = String(index + 1).padStart(2, '0');
    const fileName = `${slideNumber}_${slide.id.replace('s\\d+_', '')}.html`;
    
    // スライド番号を調整
    const slideNumberMatch = slide.content.match(/<div class="slide-number">([^<]+)<\/div>/);
    const currentSlideNumber = slideNumberMatch ? slideNumberMatch[1] : `${index + 1} / 18`;
    
    const template = `<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>生成AIが変える未来 - ${slide.id}</title>
    <link rel="stylesheet" href="../styles/main.css">
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
        .slide {
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
        }
        .slide-number {
            position: absolute;
            bottom: 20px;
            right: 20px;
            font-size: 1em;
            color: rgba(255,255,255,0.6);
        }
    </style>
</head>
<body>
    <div class="slide">
        ${slide.content}
    </div>
    
    <!-- Chart.js CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    
    <!-- スライド固有のスクリプト -->
    <script>
        // revealSecret function for question slide
        function revealSecret() {
            const revealContent = document.getElementById('revealContent');
            const confetti = document.getElementById('confetti');
            const fireworks = document.getElementById('fireworks');
            
            if (revealContent) {
                revealContent.style.display = 'block';
                revealContent.style.animation = 'slideDown 0.5s ease-out';
            }
            
            if (confetti) {
                confetti.style.display = 'block';
                createConfetti();
            }
            
            if (fireworks) {
                fireworks.style.display = 'block';
                createFireworks();
            }
        }
        
        function createConfetti() {
            // Confetti animation logic
            console.log('Confetti created');
        }
        
        function createFireworks() {
            // Fireworks animation logic
            console.log('Fireworks created');
        }
    </script>
</body>
</html>`;

    const outputPath = path.join('/Users/nakamurar39/Desktop/codes/presentations/250530_gen_ai_wg/pages', fileName);
    fs.writeFileSync(outputPath, template);
    console.log(`Created: ${fileName}`);
});

console.log(`Successfully created ${slides.length} slide files.`);
