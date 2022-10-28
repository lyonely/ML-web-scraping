let btn = document.createElement("button");

btn.innerHTML = "Go";

btn.onclick = function () {
    window.open('https://www.palantir.com/');
    //alert("Button is clicked");

};

fetch('https://ml-web-scraping.herokuapp.com/')
  .then((response) => response.json())
  .then((data) => console.log(data));

document.body.appendChild(btn);
