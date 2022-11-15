let btn = document.createElement("button");

btn.innerHTML = "Go";
btn.id = "x"

// btn.style.background = "#3dfe3a";

document.body.appendChild(btn);
var tab = "";
var label = "";

btn.onclick = function () {

  var form = document.getElementById("form")
  label = document.getElementById("fname").value


  chrome.tabs.query({active:true}, tabs=>{
      tab = tabs[0]
    }
  )

  const data = {
    url: tab.url,
    macro: label,
  }

  fetch('http://35.246.204.26:5000/macro', {
    method: 'POST',
      mode: 'cors',
      body: JSON.stringify(data),
      headers: {
        'Content-type': 'application/json'
      }
      })
      .then(function(response) {
        console.log(response)
        return response.json()})
      .then(function(data){
        console.log(data)
      })
      .catch(error => console.error('Error:', error));

};

