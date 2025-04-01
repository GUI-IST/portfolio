/**
 * Image Loader for GitHub Pages
 * Ensures images load properly on first visit
 */

// Run both at DOMContentLoaded and window.load events 
document.addEventListener('DOMContentLoaded', initImageLoader);
window.addEventListener('load', finalizeImageLoading);

// Track the loading status
let allImagesLoaded = false;
let domContentLoaded = false;
let windowLoaded = false;

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
    
    // If window has already loaded, remove preloader
    if (windowLoaded) {
        removePreloader();
    }
}

// Final steps when window is fully loaded
function finalizeImageLoading() {
    windowLoaded = true;
    console.log('Window loaded event fired');
    
    // If all images are loaded, remove preloader
    if (allImagesLoaded) {
        removePreloader();
    } else {
        // Set a timeout to remove preloader even if some images are still loading
        setTimeout(removePreloader, 3000);
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
