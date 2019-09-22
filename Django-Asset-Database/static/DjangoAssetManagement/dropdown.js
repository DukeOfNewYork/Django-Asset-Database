function myFunction() {
var x = document.getElementById("navDemo");
    if (x.className.indexOf("show") == -1) {
        x.className += " show";
        console.log(x.className);
    } else {
        x.className = x.className.replace(" show", "");
        console.log(x.className);
    }
}