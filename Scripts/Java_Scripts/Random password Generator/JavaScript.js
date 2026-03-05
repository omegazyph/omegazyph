/************************************************************
 * PROJECT: Random Password Generator
 * FILE: JavaScript.js
 * DESCRIPTION: Logic for generating a random string of 
 * characters based on a user-defined length.
 * AUTHOR: [Your Name/GitHub Username]
 * DATE: March 24, 2018 (Updated Dec 2025)
 ************************************************************/

// The master list of characters the generator can choose from
var keylist = "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*";
var temp = '';

/**
 * Core Logic: Generates the random string
 * @param {number} plength - The length of the password requested
 */
function generatepass(plength) {
    temp = ''; // Reset the temporary string
    
    for (var i = 0; i < plength; i++) {
        /* Math.random() picks a number between 0 and 1.
           We multiply it by the length of our keylist and round down 
           using Math.floor to get a valid index number.
        */
        temp += keylist.charAt(Math.floor(Math.random() * keylist.length));
    }
    return temp;
}

/**
 * Interface Logic: Connects the HTML form to the generator
 * @param {string} enterlength - The value typed into the input box
 */
function populateform(enterlength) {
    // Converts the input into the 'output' box in the HTML form
    document.pgenerate.output.value = generatepass(enterlength);
}