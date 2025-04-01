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
                img.style.width = '200px'; // Increased from 180px to 200px
                img.style.height = '200px'; // Increased from 180px to 200px
                img.style.maxWidth = '200px'; // Increased from 180px to 200px
                img.style.maxHeight = '200px'; // Increased from 180px to 200px
                img.style.objectFit = 'cover';
                img.setAttribute('width', '200'); // Increased from 180px to 200px
                img.setAttribute('height', '200'); // Increased from 180px to 200px
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
    
    // Enhanced function to ensure all hobby images have floating animations
    function applyHobbyImageAnimations() {
        document.querySelectorAll('.hobby-image').forEach((img, index) => {
            // Force remove any clip paths
            img.style.clipPath = 'none';
            
            // Set the border-radius for blob shape
            const borderRadiuses = [
                '40% 60% 70% 30% / 40% 50% 60% 50%',
                '60% 40% 30% 70% / 50% 60% 40% 50%',
                '50% 50% 35% 65% / 65% 35% 50% 50%'
            ];
            
            img.style.borderRadius = borderRadiuses[index % 3];
            
            // Apply the floating animations similar to profile image
            const animationNames = [
                'profileStyleFloat1 8s ease-in-out infinite',
                'profileStyleFloat2 9s ease-in-out infinite 0.5s',
                'profileStyleFloat3 7.5s ease-in-out infinite 1s'
            ];
            
            img.style.animation = animationNames[index % 3];
            
            // Ensure image is properly positioned for the animation
            img.style.position = 'absolute';
            img.style.top = '50%';
            img.style.left = '50%';
            img.style.transform = 'translate(-50%, -50%)';
            
            // Add shadow effects
            img.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.3), 0 0 15px rgba(255, 128, 171, 0.4)';
            
            // Ensure larger size
            img.style.width = '200px';
            img.style.height = '200px';
            img.style.maxWidth = '200px';
            img.style.maxHeight = '200px';
            
            console.log(`Applied larger size and floating animation to hobby image ${index + 1}`);
        });
    }
    
    // Run the animation function
    applyHobbyImageAnimations();
    
    // Force animation application and size constraints
    document.querySelectorAll('.hobby-image').forEach((img, index) => {
        // Force applying animations by re-adding the element to the DOM
        const parent = img.parentNode;
        const clone = img.cloneNode(true);
        
        // Remove any clip-path that might be making images look polygonal
        clone.style.clipPath = 'none';
        
        // Add width and height attributes
        clone.setAttribute('width', '200'); // Increased from 160px to 200px
        clone.setAttribute('height', '200'); // Increased from 160px to 200px
        
        // Add inline styles to force smooth shapes and animations
        const styles = [
            'width: 200px !important;', // Increased from 160px to 200px
            'height: 200px !important;', // Increased from 160px to 200px
            'max-width: 200px !important;', // Increased from 160px to 200px
            'max-height: 200px !important;', // Increased from 160px to 200px
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
        
        // Apply different animations to each hobby image - use profile-style floating
        const animations = [
            'animation: profileStyleFloat1 8s ease-in-out infinite !important;',
            'animation: profileStyleFloat2 9s ease-in-out infinite 0.5s !important;',
            'animation: profileStyleFloat3 7.5s ease-in-out infinite 1s !important;'
        ];
        
        clone.style.cssText += styles.join(' ') + shapes[index % 3] + animations[index % 3];
        
        // Replace the original with the clone
        if (parent) {
            parent.removeChild(img);
            
            // Adjust container size to be larger than the image's blob shape
            parent.style.width = '260px'; // Increased from 220px
            parent.style.height = '260px'; // Increased from 220px
            parent.style.maxWidth = '260px'; // Increased from 220px
            parent.style.maxHeight = '260px'; // Increased from 220px
            parent.style.overflow = 'visible';
            parent.style.position = 'relative';
            parent.style.margin = '0 auto 40px'; // Increased bottom margin
            parent.style.animation = 'none'; // Ensure no animation on containers
            
            setTimeout(() => parent.appendChild(clone), 100);
        }
    });
    
    // Add keyframes for profile-style floating animations if they don't exist
    const styleElement = document.createElement('style');
    styleElement.textContent = `
        @keyframes profileStyleFloat1 {
            0%, 100% {
                transform: translate(-50%, -50%) rotate(-2deg) translateY(0px);
            }
            25% {
                transform: translate(-48%, -55%) rotate(-1deg) translateY(-5px);
            }
            50% {
                transform: translate(-52%, -52%) rotate(1deg) translateY(-8px);
            }
            75% {
                transform: translate(-50%, -48%) rotate(-1deg) translateY(-3px);
            }
        }
        
        @keyframes profileStyleFloat2 {
            0%, 100% {
                transform: translate(-50%, -50%) rotate(0deg) translateY(0px);
            }
            30% {
                transform: translate(-53%, -52%) rotate(-2deg) translateY(-7px);
            }
            60% {
                transform: translate(-47%, -55%) rotate(2deg) translateY(-10px);
            }
            85% {
                transform: translate(-50%, -53%) rotate(-1deg) translateY(-5px);
            }
        }
        
        @keyframes profileStyleFloat3 {
            0%, 100% {
                transform: translate(-50%, -50%) rotate(0deg) translateY(0px);
            }
            20% {
                transform: translate(-48%, -53%) rotate(-1deg) translateY(-6px);
            }
            45% {
                transform: translate(-52%, -48%) rotate(1deg) translateY(-9px);
            }
            70% {
                transform: translate(-49%, -52%) rotate(0deg) translateY(-4px);
            }
            90% {
                transform: translate(-51%, -49%) rotate(-1deg) translateY(-2px);
            }
        }
    `;
    document.head.appendChild(styleElement);
    
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
    
    // Clear any existing animations from containers
    document.querySelectorAll('.hobby-image-container').forEach((container) => {
        container.style.animation = 'none';
        container.style.overflow = 'visible';
        container.style.position = 'relative';
        container.style.zIndex = '1';
        
        // Update container size to match the larger images
        container.style.width = '260px'; // Increased from 220px
        container.style.height = '260px'; // Increased from 220px
        container.style.maxWidth = '260px'; // Increased from 220px
        container.style.maxHeight = '260px'; // Increased from 220px
        
        console.log('Applied size adjustments to hobby image container');
    });
    
    // Ensure all hobby cards have NO animations but do have hover effects
    document.querySelectorAll('.hobby-card').forEach(card => {
        card.style.animation = 'none';
        card.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
        card.style.overflow = 'visible';
        card.style.padding = '45px 25px'; // Increased padding for larger images
    });
    
    console.log('Enhanced image fixes applied with larger sizes and profile-style floating');
    
    // Force animations on hobby images with larger size
    forceAnimationsOnHobbyImages();
});

// Create a dedicated function for forcing animations on hobby images
function forceAnimationsOnHobbyImages() {
    const hobbyImages = document.querySelectorAll('.hobby-image');
    
    // Make sure all containers are properly set up with larger sizes
    document.querySelectorAll('.hobby-image-container').forEach(container => {
        container.style.width = '260px'; // Increased from 220px
        container.style.height = '260px'; // Increased from 220px
        container.style.maxWidth = '260px'; // Increased from 220px
        container.style.maxHeight = '260px'; // Increased from 220px
        container.style.overflow = 'visible';
        container.style.position = 'relative';
        container.style.zIndex = '1';
        container.style.animation = 'none'; // No animation on container
    });
    
    // Define the animations inline to ensure they're applied - profile-style floating
    const animations = [
        `@keyframes profileFloatHobby1 {
            0%, 100% { transform: translate(-50%, -50%) rotate(-2deg) translateY(0px); }
            25% { transform: translate(-48%, -55%) rotate(-1deg) translateY(-5px); }
            50% { transform: translate(-52%, -52%) rotate(1deg) translateY(-8px); }
            75% { transform: translate(-50%, -48%) rotate(-1deg) translateY(-3px); }
        }`,
        `@keyframes profileFloatHobby2 {
            0%, 100% { transform: translate(-50%, -50%) rotate(0deg) translateY(0px); }
            30% { transform: translate(-53%, -52%) rotate(-2deg) translateY(-7px); }
            60% { transform: translate(-47%, -55%) rotate(2deg) translateY(-10px); }
            85% { transform: translate(-50%, -53%) rotate(-1deg) translateY(-5px); }
        }`,
        `@keyframes profileFloatHobby3 {
            0%, 100% { transform: translate(-50%, -50%) rotate(0deg) translateY(0px); }
            20% { transform: translate(-48%, -53%) rotate(-1deg) translateY(-6px); }
            45% { transform: translate(-52%, -48%) rotate(1deg) translateY(-9px); }
            70% { transform: translate(-49%, -52%) rotate(0deg) translateY(-4px); }
            90% { transform: translate(-51%, -49%) rotate(-1deg) translateY(-2px); }
        }`
    ];
    
    // Add these keyframes to the document
    const styleElement = document.createElement('style');
    styleElement.textContent = animations.join('\n');
    document.head.appendChild(styleElement);
    
    // Apply to each hobby image with individual settings and larger size
    hobbyImages.forEach((img, index) => {
        // Force the correct styling for floating and size
        const styles = {
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: '200px', // Increased from 160px/180px to 200px
            height: '200px', // Increased from 160px/180px to 200px
            maxWidth: '200px', // Increased from 160px/180px to 200px
            maxHeight: '200px', // Increased from 160px/180px to 200px
            objectFit: 'cover',
            borderRadius: [
                '40% 60% 70% 30% / 40% 50% 60% 50%',
                '60% 40% 30% 70% / 50% 60% 40% 50%',
                '50% 50% 35% 65% / 65% 35% 50% 50%'
            ][index % 3],
            animation: [
                'profileFloatHobby1 8s ease-in-out infinite',
                'profileFloatHobby2 9s ease-in-out infinite 0.5s',
                'profileFloatHobby3 7.5s ease-in-out infinite 1s'
            ][index % 3],
            clipPath: 'none',
            boxShadow: '0 10px 20px rgba(0, 0, 0, 0.3), 0 0 15px rgba(255, 128, 171, 0.4)'
        };
        
        // Apply all styles directly with !important
        Object.keys(styles).forEach(key => {
            img.style.setProperty(key, styles[key], 'important');
        });
        
        // Also set element attributes for extra reliability
        img.setAttribute('width', '200'); // Increased from 160px/180px to 200px
        img.setAttribute('height', '200'); // Increased from 160px/180px to 200px
        
        console.log(`Applied direct larger size and profile-style animation to hobby image ${index + 1}`);
    });
}

// Run image fixes again after full page load with larger sizes
window.addEventListener('load', function() {
    console.log('Running additional image fixes after page load with larger sizes');
    
    // Apply size constraints to all images - larger than before
    document.querySelectorAll('.hobby-image').forEach(img => {
        img.style.setProperty('width', '200px', 'important'); // Increased from 180px to 200px
        img.style.setProperty('height', '200px', 'important'); // Increased from 180px to 200px
        img.style.setProperty('max-width', '200px', 'important'); // Increased from 180px to 200px
        img.style.setProperty('max-height', '200px', 'important'); // Increased from 180px to 200px
        img.style.setProperty('object-fit', 'cover', 'important');
        img.setAttribute('width', '200'); // Increased from 180px to 200px
        img.setAttribute('height', '200'); // Increased from 180px to 200px
    });
    
    // Re-apply the animations to ensure they stick with larger sizes
    forceAnimationsOnHobbyImages();
    
    // Apply multiple times to make sure it sticks
    setTimeout(forceAnimationsOnHobbyImages, 500);
    setTimeout(forceAnimationsOnHobbyImages, 1000);
    setTimeout(forceAnimationsOnHobbyImages, 2000);
});
