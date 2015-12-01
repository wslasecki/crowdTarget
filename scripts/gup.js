function gup(name, defval) {
    name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    var regexS = "[\\?&]"+name+"=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(window.location.href);
    if(results == null) {
        //this isnt in the url, so return the defau;t value, if a default is not set return empty string ""
        defval = typeof defval !== 'undefined' ? defval : "";
        return defval;
    }
    else {
        return unescape(results[1]);
    }
}
