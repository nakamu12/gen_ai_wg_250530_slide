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
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
}

function previousSlide() {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    showSlide(currentSlide);
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
