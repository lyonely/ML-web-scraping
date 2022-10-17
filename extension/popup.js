let btn = document.createElement("button");

btn.innerHTML = "Subscribe";

btn.onclick = function () {
    window.open('https://www.palantir.com/');
    alert("Button is clicked");

};

document.body.appendChild(btn);
