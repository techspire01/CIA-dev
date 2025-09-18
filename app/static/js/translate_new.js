/**
 * Simple Google Translate Integration
 */

// Global variable to track initialization
var translateInitialized = false;

/**
 * This function MUST be in the global scope so Google's script can call it.
 */
function googleTranslateElementInit() {
  console.log('Initializing Google Translate...');
  
  new google.translate.TranslateElement({
    pageLanguage: 'en',
    includedLanguages: 'en,ta', // English and Tamil
    layout: google.translate.TranslateElement.InlineLayout.SIMPLE
  }, 'google_translate_element');
  
  translateInitialized = true;
  console.log('Google Translate initialized successfully');
}

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM loaded, Google Translate should initialize soon...');
});