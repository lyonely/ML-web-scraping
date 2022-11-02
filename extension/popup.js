let btn = document.createElement("button");

btn.innerHTML = "Go";

const tab = "";

var label;



btn.onclick = function () {

    var form = document.getElementById("form")
    label = document.getElementById("fname")

    chrome.tabs.query({active:true}, tabs=>{
        tab=tabs[0];
        alert("The URL of this page is:  " + tab.url + ". The label is: ") + label;
      }
    )

};

fetch('http://35.198.85.60/macro', {
  method: 'POST',
  body: JSON.stringify({
    url:tab.url,
    macro:label,

  }),
  headers: {
    'Content-type': 'application/json; charset=UTF-8',
  }
  })
  .then(function(response){ 
  return response.json()})
  .then(function(data)
  {console.log(data)
  body=document.getElementById("bd")
  body.innerHTML = data  
}).catch(error => console.error('Error:', error)); 

document.body.appendChild(btn);
