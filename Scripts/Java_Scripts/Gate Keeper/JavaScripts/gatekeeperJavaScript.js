/************************************************************
 * PROJECT: Gate Keeper
 * FILE: gatekeeperJavaScript.js
 * DESCRIPTION: Validates access by attempting to load a file
 * named after the user's password input.
 * AUTHOR: [Omeagzyph]
 * DATE: (updated December 2025)
 ************************************************************/

function goForit() {
    var location;
    var password;

    // Grabs the text from the input box in 'testform'
    password = this.document.testform.inputbox.value;
    
    // The password IS the filename (e.g., "Guest.html")
    location = password + ".html";
    
    fetch(location);
    
    // Closes the small pop-up window after submitting
    window.close();
}

function fetch(location) {
    var root;

    // Checks if the main "Start Page" (the opener) is still open
    if (opener.closed) {
        // If the main window was closed, open a brand new one
        root = window.open('', 'theKeepersGopher', 'toolbar=yes,location=yes,status=yes,menubar=yes,scrollbars=yes,resizable=yes,copyhistory=no');
        root.location.href = location;
    } else {
        // If the main window is still there, load the new page inside it
        opener.location.href = location;
    }
}