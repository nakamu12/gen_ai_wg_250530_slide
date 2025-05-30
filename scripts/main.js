let currentSlide = 0;
let slides, totalSlides;

function initializeSlides() {
    slides = document.querySelectorAll('.slide');
    totalSlides = slides.length;
    console.log(`Found ${totalSlides} slides`);
    
    if (totalSlides === 0) {
        console.error('No slides found!');
        return false;
    }
    return true;
}

function showSlide(index) {
    if (!slides || !slides.length) {
        console.error('Slides not initialized');
        return;
    }
    
    slides.forEach(slide => slide.classList.remove('active'));
    slides[index].classList.add('active');
    updateProgress();
    
    // Initialize chart when slide 12 is shown
    if (index === 11 && !window.chartInitialized) {
        initializeChart();
        window.chartInitialized = true;
    }
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
}

function previousSlide() {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    showSlide(currentSlide);
}

function updateProgress() {
    const progress = ((currentSlide + 1) / totalSlides) * 100;
    document.getElementById('progress').style.width = progress + '%';
}

function initializeChart() {
    const ctx = document.getElementById('growthChart').getContext('2d');
    
    // Create gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(102, 126, 234, 0.8)');
    gradient.addColorStop(1, 'rgba(233, 69, 96, 0.8)');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['GPT-2\\n2019', 'GPT-3\\n2020', 'LLaMA\\n2023', 'GPT-4\\n2023', 'Gemini Ultra\\n2024', 'Claude 3\\n2024', 'DeepSeek-R1\\n2025'],
            datasets: [{
                label: 'パラメータ数（10億）',
                data: [1.5, 175, 70, 1760, 1800, null, 671],
                backgroundColor: gradient,
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 2,
                borderRadius: 10,
                barPercentage: 0.7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'LLMパラメータ数の指数関数的成長',
                    color: '#ffffff',
                    font: {
                        size: 24,
                        weight: 'bold'
                    },
                    padding: {
                        bottom: 30
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += context.parsed.y + 'B';
                                
                                // Add notes
                                if (context.label.includes('GPT-4')) {
                                    label += ' (推定値)';
                                } else if (context.label.includes('Claude')) {
                                    label = 'Claude 3: パラメータ数非公開';
                                } else if (context.label.includes('DeepSeek')) {
                                    label += ' (MoE: 37B活性)';
                                }
                            }
                            return label;
                        },
                        title: function(context) {
                            return context[0].label.replace('\\n', ' - ');
                        }
                    },
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleFont: {
                        size: 16
                    },
                    bodyFont: {
                        size: 14
                    },
                    padding: 12,
                    displayColors: false
                }
            },
            scales: {
                y: {
                    type: 'logarithmic',
                    beginAtZero: false,
                    min: 1,
                    max: 10000,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#ffffff',
                        font: {
                            size: 14
                        },
                        callback: function(value) {
                            if (value === 1) return '1B';
                            if (value === 10) return '10B';
                            if (value === 100) return '100B';
                            if (value === 1000) return '1T';
                            if (value === 10000) return '10T';
                            return value + 'B';
                        }
                    },
                    title: {
                        display: true,
                        text: 'パラメータ数（対数スケール）',
                        color: '#ffffff',
                        font: {
                            size: 16
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#ffffff',
                        font: {
                            size: 12
                        },
                        maxRotation: 0
                    }
                }
            },
            animation: {
                duration: 2000,
                easing: 'easeInOutQuart',
                delay: (context) => {
                    return context.dataIndex * 200;
                }
            },
            onComplete: function() {
                // Add value labels on top of bars
                const chart = this;
                const ctx = chart.ctx;
                ctx.font = 'bold 16px Arial';
                ctx.fillStyle = '#ffffff';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'bottom';
                
                chart.data.datasets.forEach((dataset, i) => {
                    const meta = chart.getDatasetMeta(i);
                    meta.data.forEach((bar, index) => {
                        if (dataset.data[index] !== null) {
                            const data = dataset.data[index];
                            let label = data >= 1000 ? (data/1000).toFixed(1) + 'T' : data + 'B';
                            if (chart.data.labels[index].includes('Claude')) {
                                label = '非公開';
                            }
                            ctx.fillText(label, bar.x, bar.y - 5);
                        }
                    });
                });
            }
        }
    });
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') nextSlide();
    if (e.key === 'ArrowLeft') previousSlide();
    if (e.key === 'f' || e.key === 'F') toggleFullscreen();
    if (e.key === 'Escape' && document.fullscreenElement) {
        document.exitFullscreen();
    }
});

// Fullscreen toggle
function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        }
    }
}

// Reveal secret function
function revealSecret() {
    const revealContent = document.getElementById('revealContent');
    const button = document.querySelector('.reveal-button');
    
    // Hide button with animation
    button.style.transform = 'scale(0) rotate(180deg)';
    button.style.opacity = '0';
    
    setTimeout(() => {
        button.style.display = 'none';
        
        // Reveal content with animation
        revealContent.classList.add('revealed');
        
        // Add confetti
        createConfetti();
        
        // Add fireworks
        createFireworks();
    }, 500);
}

function createConfetti() {
    const confettiContainer = document.getElementById('confetti');
    const colors = ['#667eea', '#764ba2', '#e94560', '#00dbde', '#fc00ff', '#FFD700', '#FF69B4', '#00CED1'];
    
    for (let i = 0; i < 100; i++) {
        setTimeout(() => {
            const confettiPiece = document.createElement('div');
            confettiPiece.className = 'confetti-piece';
            confettiPiece.style.left = Math.random() * 100 + '%';
            confettiPiece.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confettiPiece.style.animationDelay = Math.random() * 0.5 + 's';
            confettiPiece.style.animationDuration = (2 + Math.random() * 2) + 's';
            confettiPiece.style.width = (5 + Math.random() * 10) + 'px';
            confettiPiece.style.height = confettiPiece.style.width;
            confettiContainer.appendChild(confettiPiece);
            
            setTimeout(() => confettiPiece.remove(), 4000);
        }, i * 20);
    }
}

function createFireworks() {
    const container = document.getElementById('fireworks');
    
    for (let i = 0; i < 5; i++) {
        setTimeout(() => {
            const x = Math.random() * window.innerWidth;
            const y = Math.random() * window.innerHeight / 2;
            createFirework(x, y);
        }, i * 800);
    }
}

function createFirework(x, y) {
    const colors = ['#667eea', '#764ba2', '#e94560', '#FFD700'];
    const color = colors[Math.floor(Math.random() * colors.length)];
    
    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.className = 'firework';
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.backgroundColor = color;
        particle.style.boxShadow = `0 0 6px ${color}`;
        
        const angle = (Math.PI * 2 / 30) * i;
        const velocity = 2 + Math.random() * 4;
        const vx = Math.cos(angle) * velocity;
        const vy = Math.sin(angle) * velocity;
        
        document.getElementById('fireworks').appendChild(particle);
        
        let posX = 0;
        let posY = 0;
        let opacity = 1;
        
        const animateParticle = () => {
            posX += vx;
            posY += vy + 0.5; // gravity
            opacity -= 0.02;
            
            particle.style.transform = `translate(${posX}px, ${posY}px)`;
            particle.style.opacity = opacity;
            
            if (opacity > 0) {
                requestAnimationFrame(animateParticle);
            } else {
                particle.remove();
            }
        };
        
        requestAnimationFrame(animateParticle);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    if (initializeSlides()) {
        showSlide(0);
    } else {
        console.error('Failed to initialize slides');
    }
});
