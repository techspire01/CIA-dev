/**
 * Simple Translation System for English and Tamil
 */

// Global variables
var currentLang = 'en';

/**
 * Google Translate initialization function
 */
function googleTranslateElementInit() {
  new google.translate.TranslateElement({
    pageLanguage: 'en',
    includedLanguages: 'en,ta',
    layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
    autoDisplay: false
  }, 'google_translate_element');
  
  console.log('Google Translate initialized');
  setupButtons();
}

/**
 * Setup translation buttons
 */
function setupButtons() {
  const btnEn = document.getElementById('translate-en');
  const btnTa = document.getElementById('translate-ta');
  
  if (!btnEn || !btnTa) {
    console.log('Translation buttons not found, retrying...');
    setTimeout(setupButtons, 1000);
    return;
  }
  
  // Check current language from URL or cookie
  currentLang = getCurrentLanguage();
  updateButtonStyles();
  
  // English button
  btnEn.onclick = function() {
    if (currentLang !== 'en') {
      translateTo('en');
    }
  };
  
  // Tamil button
  btnTa.onclick = function() {
    if (currentLang !== 'ta') {
      translateTo('ta');
    }
  };
  
  console.log('Translation buttons setup complete');
}

/**
 * Translate to specified language
 */
function translateTo(lang) {
  console.log('Translating to:', lang);
  
  // Set Google Translate cookie
  const cookieValue = lang === 'en' ? '/en/en' : '/en/' + lang;
  document.cookie = 'googtrans=' + cookieValue + '; path=/';
  
  currentLang = lang;
  updateButtonStyles();
  
  // Reload page to apply translation
  window.location.reload();
}

/**
 * Get current language from cookie
 */
function getCurrentLanguage() {
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
 * Update button styles based on current language
 */
function updateButtonStyles() {
  const btnEn = document.getElementById('translate-en');
  const btnTa = document.getElementById('translate-ta');
  
  if (!btnEn || !btnTa) return;
  
  if (currentLang === 'ta') {
    // Tamil active
    btnTa.className = 'px-3 py-1 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition';
    btnEn.className = 'px-3 py-1 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-100 transition';
  } else {
    // English active
    btnEn.className = 'px-3 py-1 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition';
    btnTa.className = 'px-3 py-1 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-100 transition';
  }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
  // Set initial button styles
  currentLang = getCurrentLanguage();
  updateButtonStyles();
});