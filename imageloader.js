/**
 * Image Loader for GitHub Pages
 * Coordinates with name animation to serve as preloader
 */

// Run both at DOMContentLoaded and window.load events 
document.addEventListener('DOMContentLoaded', initImageLoader);
window.addEventListener('load', finalizeImageLoading);

// Track the loading status
let allImagesLoaded = false;
let domContentLoaded = false;
let windowLoaded = false;
let nameAnimationCompleted = false;

// Main initialization
function initImageLoader() {
    domContentLoaded = true;
    console.log('DOM Content Loaded - Image loader initializing');
    
    // Fix GitHub Pages path issues
    fixGitHubImagePaths();
    
    // Start tracking all images
    const images = document.querySelectorAll('img');
    console.log(`Found ${images.length} images to track for loading`);
    
    // Set default dimensions on all images
    images.forEach(setDefaultImageDimensions);
    
    // Check if all images are already loaded
    checkImagesLoaded(images);
    
    // Listen for when the name animation completes
    // This is based on the CSS animation timing from the stylesheet (around 5.8s total)
    setTimeout(() => {
        nameAnimationCompleted = true;
        console.log('Name animation completed');
        tryRevealContent();
    }, 6000); // Set to match the end of the full name animation plus buffer
}

// Fix GitHub Pages path issues if necessary
function fixGitHubImagePaths() {
    if (window.location.hostname.includes('github.io')) {
        console.log('GitHub Pages detected - fixing image paths');
        const repoName = window.location.pathname.split('/')[1];
        
        // Only add the repo name if we're on a GitHub Pages domain
        if (repoName && repoName.length > 0) {
            const baseUrl = '/' + repoName + '/';
            console.log(`Using base URL: ${baseUrl}`);
            
            document.querySelectorAll('img').forEach(img => {
                const src = img.getAttribute('src');
                if (src && (src.startsWith('./') || (!src.startsWith('/') && !src.startsWith('http')))) {
                    const newSrc = baseUrl + src.replace(/^\.\//, '');
                    console.log(`Fixing image path: ${src} -> ${newSrc}`);
                    img.setAttribute('src', newSrc);
                }
            });
        }
    }
}

// Set default dimensions for images
function setDefaultImageDimensions(img) {
    if (img.classList.contains('hobby-image')) {
        img.style.width = '200px';
        img.style.height = '200px';
        img.style.maxWidth = '200px';
        img.style.maxHeight = '200px';
        img.setAttribute('width', '200');
        img.setAttribute('height', '200');
    } else if (img.classList.contains('profile-image')) {
        img.style.width = '260px';
        img.style.height = '260px';
        img.style.maxWidth = '260px';
        img.style.maxHeight = '260px';
        img.setAttribute('width', '260');
        img.setAttribute('height', '260');
    } else if (img.classList.contains('org-logo')) {
        img.style.height = '30px';
        img.setAttribute('height', '30');
    }
}

// Check if all images are loaded
function checkImagesLoaded(images) {
    let loadedCount = 0;
    const totalImages = images.length;
    
    // For already loaded images (from cache)
    images.forEach(img => {
        if (img.complete) {
            loadedCount++;
            img.classList.add('image-loaded');
        } else {
            // Set up event listeners for images still loading
            img.addEventListener('load', () => {
                loadedCount++;
                img.classList.add('image-loaded');
                
                // Update preloader if needed
                const preloaderText = document.querySelector('.loading-text');
                if (preloaderText) {
                    preloaderText.textContent = `Loading... ${Math.round((loadedCount / totalImages) * 100)}%`;
                }
                
                if (loadedCount === totalImages) {
                    console.log('All images loaded via events');
                    allImagesLoaded = true;
                    applyImageStyles();
                }
            });
            
            // Handle error state
            img.addEventListener('error', () => {
                loadedCount++;
                console.error(`Failed to load image: ${img.src}`);
                
                // Try with a different path
                if (img.src.startsWith('/')) {
                    const newSrc = img.src.substring(1); // Remove leading slash
                    console.log(`Trying alternative path: ${newSrc}`);
                    img.src = newSrc;
                }
                
                if (loadedCount === totalImages) {
                    console.log('All images processed (some with errors)');
                    allImagesLoaded = true;
                    applyImageStyles();
                }
            });
        }
    });
    
    // Check if all images were already loaded
    if (loadedCount === totalImages) {
        console.log('All images were already loaded');
        allImagesLoaded = true;
        applyImageStyles();
    }
}

// Apply styles and animations once images are loaded
function applyImageStyles() {
    forceHobbyImageAnimations();
    
    // Apply any additional styles that depend on images being loaded
    document.querySelectorAll('.hobby-image-container').forEach(container => {
        container.style.width = '260px';
        container.style.height = '260px';
        container.style.maxWidth = '260px';
        container.style.maxHeight = '260px';
        container.style.overflow = 'visible';
    });
    
    // Try to reveal content if the animation is also complete
    tryRevealContent();
}

// Final steps when window is fully loaded
function finalizeImageLoading() {
    windowLoaded = true;
    console.log('Window loaded event fired');
    
    // If all conditions are met, reveal content
    if (allImagesLoaded) {
        tryRevealContent();
    } else {
        // Force reveal after timeout even if some images aren't loaded
        setTimeout(() => {
            allImagesLoaded = true;
            tryRevealContent();
        }, 8000);
    }
}

// Remove the preloader
function removePreloader() {
    console.log('Removing preloader');
    document.body.classList.add('loaded');
    
    // Force a small delay so animations start after preloader
    setTimeout(() => {
        forceHobbyImageAnimations();
    }, 500);
}

// New function to handle the transition from preloader to content
function tryRevealContent() {
    // Check if both conditions are met:
    // 1. Name animation has completed
    // 2. Images are loaded (or timeout reached)
    if (nameAnimationCompleted && (allImagesLoaded || windowLoaded)) {
        console.log('Revealing content - animation done and images loaded');
        
        // Fade out loading indicator
        const loadingIndicator = document.querySelector('.loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
        
        // Reveal main content with slight delay after name animation
        setTimeout(() => {
            // Remove loading class from body
            document.body.classList.remove('loading');
            
            // Show content sections with staggered timing
            const contentReveal = document.querySelector('.content-reveal');
            if (contentReveal) {
                contentReveal.classList.add('visible');
            }
            
            // Show header with slight delay
            setTimeout(() => {
                const header = document.querySelector('header');
                if (header) {
                    header.style.opacity = '1';
                    header.style.pointerEvents = 'auto';
                    header.classList.add('visible');
                }
            }, 300);
            
            // Show scroll indicator with animation
            setTimeout(() => {
                const scrollIndicator = document.querySelector('.scroll-indicator');
                if (scrollIndicator) {
                    scrollIndicator.style.opacity = '1';
                }
            }, 600);
            
            // Apply hobby image animations after reveal
            setTimeout(forceHobbyImageAnimations, 800);
        }, 500);
    } else {
        console.log('Waiting for name animation or images to complete...');
    }
}
