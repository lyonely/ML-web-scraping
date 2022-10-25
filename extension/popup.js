let btn = document.createElement("button");

btn.innerHTML = "Go";

btn.onclick = function () {
    window.open('https://www.palantir.com/');
    alert("Button is clicked");

};

document.body.appendChild(btn);
