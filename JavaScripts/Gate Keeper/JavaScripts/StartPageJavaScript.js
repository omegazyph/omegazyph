/************************************************************
 * PROJECT: Gate Keeper
 * FILE: StartPageJavaScript.js
 * DESCRIPTION: Launches the secure popup challenge window.
 * AUTHOR: [Omegazyph]
 * DATE: (updated December 2025)
 ************************************************************/

var nifty_little_window = null;

function gateKeeper() {
    // Opens a new specialized window for the password entry
    nifty_little_window = window.open('gatekeep.html', 'theKeeper', 'width=350,height=200,resizable=1');
}