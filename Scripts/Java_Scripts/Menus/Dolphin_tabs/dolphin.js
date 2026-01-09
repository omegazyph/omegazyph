/*
-------------------------------------------------------------------------
PROJECT  : [Dolphin tabs]
FILE     : [dolphin.js]
AUTHOR   : omegazyph
CREATED  : 01-18-2007
UPDATED  : 12-31-2025
DESCRIPTION: 
    The JavaScript logic for the Dolphin Tabs menu. Manages the 
    showing/hiding of sub-content based on mouseover events.
-------------------------------------------------------------------------
*/

var dolphintabs = {
    subcontainers: [], 
    last_accessed_tab: null,

    // Shows the specific content linked to the hovered tab
    revealsubmenu: function(curtabref) {
        this.hideallsubs(); // Hide all open panels first
        
        if (this.last_accessed_tab != null) {
            this.last_accessed_tab.className = ""; // Remove highight from previous tab
        }
        
        // If there's a sub menu defined for this tab item (via rel attribute), show it
        if (curtabref.getAttribute("rel")) {
            document.getElementById(curtabref.getAttribute("rel")).style.display = "block";
        }
        
        curtabref.className = "current"; // Highlight the active tab
        this.last_accessed_tab = curtabref;
    },

    // Loops through the stored IDs and sets their display to none
    hideallsubs: function() {
        for (var i = 0; i < this.subcontainers.length; i++) {
            document.getElementById(this.subcontainers[i]).style.display = "none";
        }
    },

    // Sets up the menu by gathering all links and assigning event listeners
    init: function(menuId, selectedIndex) {
        var tabItems = document.getElementById(menuId).getElementsByTagName("a");
        
        for (var i = 0; i < tabItems.length; i++) {
            // Store the ID of the sub-menu div found in the 'rel' attribute
            if (tabItems[i].getAttribute("rel")) {
                this.subcontainers[this.subcontainers.length] = tabItems[i].getAttribute("rel");
            }
            
            // If this tab item should be selected by default (based on index)
            if (i == selectedIndex) {
                tabItems[i].className = "current";
                this.revealsubmenu(tabItems[i]);
            }
            
            // Trigger the reveal when the mouse moves over a tab
            tabItems[i].onmouseover = function() {
                dolphintabs.revealsubmenu(this);
            };
        } // END FOR LOOP
    }
};