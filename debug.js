// This file adds debug functionality to help with GitHub Pages issues

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
            
            // Apply size constraints even for successfully loaded images
            if (img.classList.contains('hobby-image')) {
                img.style.width = '180px';
                img.style.height = '180px';
                img.style.maxWidth = '180px';
                img.style.maxHeight = '180px';
                img.style.objectFit = 'cover';
                img.setAttribute('width', '180');
                img.setAttribute('height', '180');
            } else if (img.classList.contains('profile-image')) {
                img.style.width = '280px';
                img.style.height = '280px';
                img.style.maxWidth = '280px';
                img.style.maxHeight = '280px';
                img.style.objectFit = 'cover';
                img.setAttribute('width', '280');
                img.setAttribute('height', '280');
            }
        }
    });
    
    // Force animation application and size constraints
    document.querySelectorAll('.hobby-image').forEach((img, index) => {
        // Force applying animations by re-adding the element to the DOM
        const parent = img.parentNode;
        const clone = img.cloneNode(true);
        
        // Remove any clip-path that might be making images look polygonal
        clone.style.clipPath = 'none';
        
        // Add width and height attributes
        clone.setAttribute('width', '160');
        clone.setAttribute('height', '160');
        
        // Add inline styles to force smooth shapes and animations
        const styles = [
            'width: 160px !important;',
            'height: 160px !important;',
            'max-width: 160px !important;',
            'max-height: 160px !important;',
            'object-fit: cover !important;',
            'position: absolute !important;',
            'top: 50% !important;',
            'left: 50% !important;',
            'transform: translate(-50%, -50%) !important;',
            'box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3), 0 0 15px rgba(255, 128, 171, 0.4) !important;'
        ];
        
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
        
        clone.style.cssText += styles.join(' ') + shapes[index % 3] + animations[index % 3];
        
        // Replace the original with the clone
        if (parent) {
            parent.removeChild(img);
            
            // Adjust container size to be larger than the image's blob shape
            parent.style.width = '220px';
            parent.style.height = '220px';
            parent.style.maxWidth = '220px';
            parent.style.maxHeight = '220px';
            parent.style.overflow = 'visible';
            parent.style.position = 'relative';
            parent.style.margin = '0 auto 30px';
            
            setTimeout(() => parent.appendChild(clone), 100);
        }
    });
    
    // Fix the profile image - make sure it's not polygonal but a smooth blob
    const profileImg = document.querySelector('.profile-image');
    if (profileImg) {
        // Remove any clip-path properties
        profileImg.style.clipPath = 'none';
        
        profileImg.style.width = '260px';
        profileImg.style.height = '260px';
        profileImg.style.maxWidth = '260px';
        profileImg.style.maxHeight = '260px';
        profileImg.style.objectFit = 'cover';
        profileImg.setAttribute('width', '260');
        profileImg.setAttribute('height', '260');
        profileImg.style.position = 'absolute';
        profileImg.style.top = '50%';
        profileImg.style.left = '50%';
        profileImg.style.transform = 'translate(-50%, -50%)';
        
        // Keep the smooth border-radius for blob shape
        profileImg.style.borderRadius = '40% 60% 70% 30% / 40% 50% 60% 50%';
        profileImg.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 128, 171, 0.5)';
        
        // Adjust the container
        const profileContainer = profileImg.closest('.floating-profile');
        if (profileContainer) {
            profileContainer.style.width = '320px';
            profileContainer.style.height = '320px';
            profileContainer.style.maxWidth = '320px';
            profileContainer.style.maxHeight = '320px';
            profileContainer.style.overflow = 'visible';
            profileContainer.style.position = 'relative';
        }
    }
    
    console.log('Enhanced image fixes applied');
});

// Run image fixes again after full page load to catch any lazy-loaded images
window.addEventListener('load', function() {
    console.log('Running additional image fixes after page load');
    
    // Apply size constraints to all images
    document.querySelectorAll('.hobby-image').forEach(img => {
        img.style.width = '180px';
        img.style.height = '180px';
        img.style.maxWidth = '180px';
        img.style.maxHeight = '180px';
        img.style.objectFit = 'cover';
    });
    
    const profileImg = document.querySelector('.profile-image');
    if (profileImg) {
        profileImg.style.width = '280px';
        profileImg.style.height = '280px';
        profileImg.style.maxWidth = '280px';
        profileImg.style.maxHeight = '280px';
        profileImg.style.objectFit = 'cover';
    }
});
