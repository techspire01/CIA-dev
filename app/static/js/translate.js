/**
 * Global variables for translation management
 */
let isTranslateInitialized = false;
let currentLanguage = 'en';

/**
 * This function MUST be in the global scope so Google's script can call it.
 * It initializes the Google Translate widget.
 */
function googleTranslateElementInit() {
  console.log('Google Translate is initializing...');
  
  try {
    new google.translate.TranslateElement({
      pageLanguage: 'en',
      includedLanguages: 'en,ta', // English and Tamil
      layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
      autoDisplay: false,
      multilanguagePage: true
    }, 'google_translate_element');
    
    console.log('Google Translate widget created successfully');
    isTranslateInitialized = true;
    
    // Setup button listeners after widget is created
    setTimeout(setupTranslateButtons, 1000);
  } catch (error) {
    console.error('Error initializing Google Translate:', error);
  }
}

/**
 * Setup the translation button functionality
 */
function setupTranslateButtons() {
  console.log('Setting up translate buttons...');
  
  const btnEn = document.getElementById('translate-en');
  const btnTa = document.getElementById('translate-ta');
  
  if (!btnEn || !btnTa) {
    console.error('Translation buttons not found');
    return;
  }
  
  console.log('Translation buttons found, setting up click handlers...');
  
  // Check current language from cookie
  const currentLangFromCookie = getCookieLanguage();
  currentLanguage = currentLangFromCookie || 'en';
  updateButtonStates();
  
  // Remove existing event listeners to prevent duplicates
  btnEn.onclick = null;
  btnTa.onclick = null;
  
  // Tamil button click handler
  btnTa.onclick = function() {
    console.log('Tamil button clicked');
    if (currentLanguage !== 'ta') {
      translatePage('ta');
    } else {
      console.log('Already in Tamil, no action needed');
    }
  };
  
  // English button click handler
  btnEn.onclick = function() {
    console.log('English button clicked');
    if (currentLanguage !== 'en') {
      translatePage('en');
    } else {
      console.log('Already in English, no action needed');
    }
  };
  
  console.log('Translation buttons setup completed!');
}

/**
 * Get current language from Google Translate cookie
 */
function getCookieLanguage() {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    if (name === 'googtrans') {
      const match = value.match(/\/en\/(\w+)/);
      return match ? match[1] : 'en';
    }
  }
  return 'en';
}

/**
 * Set translation cookie and trigger translation
 */
function translatePage(targetLang) {
  console.log(`Translating page to: ${targetLang}`);
  
  try {
    // Set the Google Translate cookie
    const cookieValue = targetLang === 'en' ? '/en/en' : `/en/${targetLang}`;
    document.cookie = `googtrans=${cookieValue}; path=/; domain=${window.location.hostname}`;
    document.cookie = `googtrans=${cookieValue}; path=/`;
    
    // Update current language and button states
    currentLanguage = targetLang;
    updateButtonStates();
    
    console.log(`Translation cookie set for ${targetLang}, reloading page...`);
    
    // Reload the page to apply translation
    setTimeout(() => {
      window.location.reload();
    }, 100);
    
  } catch (error) {
    console.error('Error setting translation cookie:', error);
    window.location.reload();
  }
}

/**
 * Update button active states
 */
function updateButtonStates() {
  const btnEn = document.getElementById('translate-en');
  const btnTa = document.getElementById('translate-ta');
  
  if (btnEn && btnTa) {
    if (currentLanguage === 'ta') {
      btnTa.classList.add('active');
      btnEn.classList.remove('active');
      console.log('Tamil button set as active');
    } else {
      btnEn.classList.add('active');
      btnTa.classList.remove('active');
      console.log('English button set as active');
    }
  }
}

/**
 * Initialize translation when the page is ready
 */
function initializeTranslation() {
  console.log('Initializing translation system...');
  
  // Check if Google Translate element exists
  const translateElement = document.getElementById('google_translate_element');
  if (!translateElement) {
    console.error('Google Translate element not found in DOM');
    return;
  }
  
  // Check if buttons exist
  const btnEn = document.getElementById('translate-en');
  const btnTa = document.getElementById('translate-ta');
  
  if (!btnEn || !btnTa) {
    console.error('Translation buttons not found');
    return;
  }
  
  console.log('All required elements found, waiting for Google Translate to load...');
  
  // Set initial button states based on current language
  currentLanguage = getCookieLanguage();
  updateButtonStates();
  
  // If Google Translate is already initialized, setup buttons
  if (isTranslateInitialized) {
    setupTranslateButtons();
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeTranslation);
} else {
  initializeTranslation();
}

// Also try after window load as backup
window.addEventListener('load', function() {
  if (!isTranslateInitialized) {
    setTimeout(initializeTranslation, 2000);
  }
});

// Listen for page visibility changes to update button states
document.addEventListener('visibilitychange', function() {
  if (!document.hidden) {
    currentLanguage = getCookieLanguage();
    updateButtonStates();
  }
});

