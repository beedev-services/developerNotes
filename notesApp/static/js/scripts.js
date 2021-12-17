function openStack(evt, openStack) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabContent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tabs");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(openStack).style.display = "block";
    evt.currentTarget.className += " active";
}
function copyCode() {
    var copyText = document.getElementById('copyCode')
    console.log(copyText)
    copyText.select()
    copyText.setSelectionRange(0, 99999)
    navigator.clipboard.writeText(copyText.value)
    alert("Copied the Code: " + copyText.value)
}
var modal = document.getElementById("theModal");
var img = document.getElementById("img");
var modalImg = document.getElementById("theImg");
img.onclick = function(){
    console.log(modalImg.src)
    modal.style.display = "block";
    modalImg.src = this.src;
}
var span = document.getElementsByClassName("close")[0];

span.onclick = function() { 
    modal.style.display = "none";
}