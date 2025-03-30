// This file adds some debug functionality to help with GitHub Pages issues

document.addEventListener('DOMContentLoaded', function() {
    // Check if images are loading properly
    const allImages = document.querySelectorAll('img');
    
    allImages.forEach(img => {
        if (!img.complete || img.naturalHeight === 0) {
            console.error('Image failed to load:', img.src);
            
            // Add placeholder style to show where images should be
            img.style.border = '2px dashed red';
            img.style.backgroundColor = '#fee';
            img.style.padding = '30px';
            img.style.display = 'block';
            
            // Try to fix with absolute URL if running on GitHub Pages
            if (window.location.hostname.includes('github.io')) {
                const repoName = window.location.pathname.split('/')[1];
                const newSrc = `/${repoName}/${img.getAttribute('src').replace(/^\.\//, '')}`;
                console.log('Attempting to fix image path:', newSrc);
                img.setAttribute('src', newSrc);
            }
        } else {
            console.log('Image loaded successfully:', img.src);
        }
    });
    
    // Force animation application
    document.querySelectorAll('.hobby-image').forEach((img, index) => {
        // Force applying animations by re-adding the element to the DOM
        const parent = img.parentNode;
        const clone = img.cloneNode(true);
        parent.removeChild(img);
        
        // Add inline styles to force shapes and animations
        const shapes = [
            'border-radius: 40% 60% 70% 30% / 40% 50% 60% 50% !important;',
            'border-radius: 60% 40% 30% 70% / 50% 60% 40% 50% !important;',
            'border-radius: 50% 50% 35% 65% / 65% 35% 50% 50% !important;'
        ];
        
        const animations = [
            'animation: floatHobby1 7s ease-in-out infinite !important;',
            'animation: floatHobby2 8.5s ease-in-out infinite 0.5s !important;',
            'animation: floatHobby3 9s ease-in-out infinite 1s !important;'
        ];
        
        clone.style.cssText += shapes[index % 3] + animations[index % 3];
        setTimeout(() => parent.appendChild(clone), 100);
    });
});
