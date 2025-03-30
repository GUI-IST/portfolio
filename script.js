document.addEventListener('DOMContentLoaded', function() {
    // Language switching functionality
    const langEN = document.getElementById('lang-en');
    const langPT = document.getElementById('lang-pt');
    
    // Set default language to English
    let currentLang = 'en';
    
    // Function to switch language
    function switchLanguage(lang) {
        currentLang = lang;
        
        // Update active state on buttons
        if (lang === 'en') {
            langEN.classList.add('active');
            langPT.classList.remove('active');
        } else {
            langPT.classList.add('active');
            langEN.classList.remove('active');
        }
        
        // Update all elements with data-en and data-pt attributes
        document.querySelectorAll('[data-en]').forEach(element => {
            if (lang === 'en') {
                element.textContent = element.getAttribute('data-en');
            } else {
                element.textContent     = element.getAttribute('data-pt');
            }
        });
        
        // Update form placeholders
        document.querySelectorAll('[data-en-placeholder]').forEach(element => {
            if (lang === 'en') {
                element.setAttribute('placeholder', element.getAttribute('data-en-placeholder'));
            } else {
                element.setAttribute('placeholder', element.getAttribute('data-pt-placeholder'));
            }
        });
        
        // Update HTML lang attribute
        document.documentElement.lang = lang;
        
        // Store language preference
        localStorage.setItem('preferredLanguage', lang);
    }
    
    // Event listeners for language buttons
    langEN.addEventListener('click', () => switchLanguage('en'));
    langPT.addEventListener('click', () => switchLanguage('pt'));
    
    // Check for stored language preference
    const storedLang = localStorage.getItem('preferredLanguage');
    if (storedLang) {
        switchLanguage(storedLang);
    }
    
    // Show header after orbital animation completes
    setTimeout(() => {
        document.querySelector('header').classList.add('visible');
    }, 4000); // Reduced from 6000 to match faster animation

    // Animate sections when they come into view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    document.querySelectorAll('.content-wrap').forEach(section => {
        if (section.parentElement.id !== 'hero') {
            section.classList.add('fade-down');
            observer.observe(section);
        }
    });

    // Smooth scrolling for navigation links and buttons
    const scrollToSection = (targetId) => {
        const targetSection = document.querySelector(targetId);
        window.scrollTo({
            top: targetSection.offsetTop,
            behavior: 'smooth'
        });
    };

    document.querySelectorAll('.nav-link, .nav-button').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            scrollToSection(targetId);
        });
    });

    // Header background change on scroll
    window.addEventListener('scroll', function() {
        const header = document.querySelector('header');
        if (window.scrollY > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Handle form submission
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;
            
            // Here you would normally send the data to a server
            // For now, we'll just log it and show an alert
            console.log('Form submitted:', { name, email, message });
            
            // Show alert based on current language
            if (currentLang === 'en') {
                alert('Message sent! Thank you for reaching out.');
            } else {
                alert('Mensagem enviada! Obrigado pelo contato.');
            }
            
            contactForm.reset();
        });
    }

    // Remove the old letter-by-letter animation since we now have a more complex CSS animation
    // const titleElement = document.querySelector('.animated-title');
    // if (titleElement) {
    //     const name = titleElement.textContent;
    //     titleElement.textContent = '';
    //     
    //     let delay = 0;
    //     for (let i = 0; i < name.length; i++) {
    //         const span = document.createElement('span');
    //         span.textContent = name[i];
    //         span.style.display = 'inline-block';
    //         span.style.opacity = '0';
    //         span.style.transform = 'translateY(50px)';
    //         span.style.animation = `revealTitle 0.5s ease ${delay}s forwards`;
    //         titleElement.appendChild(span);
    //         delay += 0.1;
    //     }
    // }

    // Improved parallax effect - background scrolls upward as user scrolls down
    window.addEventListener('scroll', function() {
        const background = document.getElementById('background');
        if (!background) return;
        
        const scrollPosition = window.pageYOffset;
        
        // Calculate the movement speed with the negative sign for upward movement
        const translateY = -scrollPosition / 2;
        
        // Apply transform to the background image
        background.style.transform = `translateY(${translateY}px)`;
        
        // Ensure the background container covers enough area
        const documentHeight = Math.max(
            document.body.scrollHeight,
            document.body.offsetHeight,
            document.documentElement.clientHeight,
            document.documentElement.scrollHeight,
            document.documentElement.offsetHeight
        );
        
        // Set background image height to ensure it's large enough
        const containerHeight = documentHeight + window.innerHeight;
        background.style.height = `${containerHeight}px`;
        background.parentElement.style.height = `${containerHeight}px`;
    });

    // Ensure 3D animations work well across devices
    function adjustNameSize() {
        const viewportWidth = window.innerWidth;
        const nameElements = document.querySelectorAll('.name-part, .assembled-name');
        
        if (viewportWidth < 768) {
            // Tablet and smaller screens
            nameElements.forEach(el => {
                el.style.fontSize = viewportWidth < 480 ? '2rem' : '2.8rem';
            });
        } else {
            // Desktop screens
            nameElements.forEach(el => {
                el.style.fontSize = '4rem';
            });
        }
    }
    
    // Adjust on load and resize
    adjustNameSize();
    window.addEventListener('resize', adjustNameSize);

    // Add this code to ensure consistent background appearance on page load
    const background = document.getElementById('background');
    if (background) {
        // Set the initial transform to match scroll position 0
        background.style.transform = 'translateY(0px)';
        
        // Set initial height
        const documentHeight = Math.max(
            document.body.scrollHeight,
            document.body.offsetHeight,
            document.documentElement.clientHeight,
            document.documentElement.scrollHeight,
            document.documentElement.offsetHeight
        );
        
        const containerHeight = documentHeight + window.innerHeight;
        background.style.height = `${containerHeight}px`;
        background.parentElement.style.height = `${containerHeight}px`;
    }
});
