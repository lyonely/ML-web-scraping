let btn = document.createElement("button");

btn.innerHTML = "Go";

var tab = "";

var label;


document.body.appendChild(btn);

var get = fetch('http://35.198.85.60/macro');

console.log(get)

btn.onclick = function () {

    var form = document.getElementById("form")
    label = document.getElementById("fname").value

    chrome.tabs.query({active:true}, tabs=>{
        tab=tabs[0];
        alert("The URL of this page is:  " + tab.url + ". The label is: " + label);
      }
    )

    const data = {
      url: tab.url,
      macro: label,
      requested_amt: 1
    }

  fetch('http://35.198.85.60/macro', {
    method: 'POST',
      mode: 'cors',
      body: JSON.stringify(data),
      headers: {
        'Content-type': 'application/json'
      }
      })
      .then(function(response){
        console.log(response)
      return response.json()})
      .then(function(data)
      {console.log(data)
      body=document.getElementById("bd")
      body.innerHTML = data
    }).catch(error => console.error('Error:', error));

};
