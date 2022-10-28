let btn = document.createElement("button");

btn.innerHTML = "Go";

btn.onclick = function () {
    // window.open('https://www.palantir.com/');

    chrome.tabs.query({active:true}, tabs=>{
        const tab=tabs[0];
        alert("The URL of this page is:  " + tab.url);
      }
    )

};

fetch('https://ml-web-scraping.herokuapp.com/')
  .then((response) => response.json())
  .then((data) => console.log(data));

document.body.appendChild(btn);
