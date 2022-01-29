function toggleListExpand(el) {
    // Toggle collapse indicator
    var ci = el.getElementsByClassName("collapse-indicator")[0];
    if (ci.innerHTML == "[+]") {
        ci.innerHTML = "[-]";
    } else {
        ci.innerHTML = "[+]"
    }
    // Get list of sub-elements
    var sublist = el.nextElementSibling.children;
    var status;
    for (i=0; i<sublist.length; i++) {
        status = window.getComputedStyle(sublist[i]).display;
        if (status == "none") {
            sublist[i].style.display = "block";
        } else {
            sublist[i].style.display = "none"
        }
    }
}