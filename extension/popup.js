let btn = document.createElement("button");

btn.innerHTML = "Go";
btn.id = "x"

const textOutput = document.querySelector("#showOutput");

// btn.style.background = "#3dfe3a";

document.body.appendChild(btn);
var label = "";

btn.addEventListener("click", fetchHandler);

// showing output
function displayOutput() {
  loader.classList.add("visible");
  // to stop loading after some time
}

// hiding output 
function hideOutput() {
  loader.classList.remove("visible");
}

// selecting loading div
const loader = document.querySelector("#loading");
// const loader2 = document.querySelector(".fetchingResult");

// showing loading
function displayLoading() {
    loader.classList.add("display");
    // loader2.classList.add("display");
}

// hiding loading 
function hideLoading() {
    loader.classList.remove("display");
    // loader2.classList.remove("display");
}

async function fetchHandler(event) {
  let queryOptions = { active: true, lastFocusedWindow: true };
  // `tab` will either be a `tabs.Tab` instance or `undefined`.
  let [tab] = await chrome.tabs.query(queryOptions);
  console.log(tab)

  displayLoading()
  var form = document.getElementById("form")
  label = document.getElementById("fname").value

  const data = {
    url: tab.url,
    macro: label,
  }

  console.log(data.url + " " + data.macro)

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
        hideLoading()
        console.log(data)
        displayOutput()
        let d = data.products_to_keyword
        console.log(d)
        let d1 = JSON.stringify(d)
        var result_str = ""
        for (var key in d){
          result_str += String(key) + ": " +  String(d[key]) + "\n" + "\n"
        }
        textOutput.innerText = result_str
      })
      .catch(error => console.error('Error:', error));

};

