
function goForit()
{
    var location;
    var password;
    password = this.document.testform.inputbox.value;
    location = password + ".html";
    fetch(location);
    theKeeper = window.close();
}

function fetch(location)
{
    var root;
    if (opener.closed)
    {
        root = window.open('', 'theKeepersGopher', 'toolbar=yes,location=yes,status=yes,menubar=yes,scrollbars=yes,resizable=yes,copyhistory=no');
        root.location.href = location;
    }
    else
    {
        opener.location.href = location;
    }
}