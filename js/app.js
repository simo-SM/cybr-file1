
// Download functionality
function downloadCyberFile() {
  document.getElementById('download').scrollIntoView({ behavior: 'smooth' });
}

function downloadFile(type) {
  const progressDiv = document.getElementById('download-progress');
  const bar = document.getElementById('download-bar');
  const percent = document.getElementById('download-percent');
  const filename = document.getElementById('download-filename');
  const status = document.getElementById('download-status');
  
  progressDiv.classList.remove('hidden');
  
  const files = {
    exe: { name: 'cyberfile_v2.7.exe', size: '12.4 MB' },
    source: { name: 'cyber-file-v2.7.zip', size: '45 KB' }
  };
  
  const file = files[type];
  filename.textContent = `Downloading ${file.name} (${file.size})...`;
  
  let progress = 0;
  const interval = setInterval(() => {
    progress += Math.random() * 15;
    if (progress > 100) progress = 100;
    
    bar.style.width = progress + '%';
    percent.textContent = Math.floor(progress) + '%';
    
    if (progress < 30) status.textContent = 'Connecting to server...';
    else if (progress < 60) status.textContent = 'Downloading packages...';
    else if (progress < 90) status.textContent = 'Verifying checksum...';
    else status.textContent = 'Finalizing...';
    
    if (progress === 100) {
      clearInterval(interval);
      setTimeout(() => {
        showToast('Download Complete', `${file.name} saved to Downloads`);
        progressDiv.classList.add('hidden');
        bar.style.width = '0%';
        
        // Simulate actual file download
        const link = document.createElement('a');
        link.href = type === 'exe' 
          ? 'https://github.com/yourusername/cyber-file/releases/download/v2.7/cyberfile_v2.7.exe'
          : 'https://github.com/yourusername/cyber-file/archive/refs/tags/v2.7.zip';
        link.download = file.name;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }, 500);
    }
  }, 200);
}

// Toast notification
function showToast(title, message) {
  const toast = document.getElementById('toast');
  document.getElementById('toast-title').textContent = title;
  document.getElementById('toast-message').textContent = message;
  
  toast.classList.remove('hidden');
  setTimeout(() => {
    toast.classList.add('hidden');
  }, 3000);
}

// Matrix rain effect on background (subtle)
document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.createElement('canvas');
  canvas.style.position = 'fixed';
  canvas.style.top = '0';
  canvas.style.left = '0';
  canvas.style.width = '100%';
  canvas.style.height = '100%';
  canvas.style.pointerEvents = 'none';
  canvas.style.zIndex = '1';
  canvas.style.opacity = '0.03';
  document.body.appendChild(canvas);
  
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  
  const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
  const drops = [];
  const fontSize = 14;
  const columns = canvas.width / fontSize;
  
  for (let i = 0; i < columns; i++) {
    drops[i] = Math.random() * -100;
  }
  
  function draw() {
    ctx.fillStyle = 'rgba(10, 10, 15, 0.1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#00ff41';
    ctx.font = fontSize + 'px monospace';
    
    for (let i = 0; i < drops.length; i++) {
      const text = chars[Math.floor(Math.random() * chars.length)];
      ctx.fillText(text, i * fontSize, drops[i] * fontSize);
      
      if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
        drops[i] = 0;
      }
      drops[i]++;
    }
  }
  
  setInterval(draw, 50);
  
  window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  });
});

// Glitch effect randomizer
setInterval(() => {
  const glitches = document.querySelectorAll('.glitch');
  glitches.forEach(el => {
    if (Math.random() > 0.95) {
      el.style.animation = 'none';
      setTimeout(() => {
        el.style.animation = '';
      }, 100);
    }
  });
}, 3000);


// this code make in mobile menu toggle
const menuBtn = document.getElementById("menu-btn");
const mobileMenu = document.getElementById("mobile-menu");
const menuIcon = document.getElementById("menu-icon");

menuBtn.addEventListener("click", () => {

  mobileMenu.classList.toggle("hidden");

  if (mobileMenu.classList.contains("hidden")) {
    menuIcon.classList.remove("fa-xmark");
    menuIcon.classList.add("fa-bars");
  } else {
    menuIcon.classList.remove("fa-bars");
    menuIcon.classList.add("fa-xmark");
  }

});