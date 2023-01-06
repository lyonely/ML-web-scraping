let btn2 = document.createElement("button");

btn2.innerHTML = "Single Product";
btn2.style.cssText = "border: 0; outline: 0; cursor: pointer; color: rgb(60, 66, 87);background-color: rgb(255, 255, 255);box-shadow: rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 12%) 0px 1px 1px 0px, rgb(60 66 87 / 16%) 0px 0px 0px 1px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(60 66 87 / 8%) 0px 2px 5px 0px;border-radius: 4px;font-size: 14px;font-weight: 500;padding: 0px 8px;display: inline-block;min-height: 28px;transition: background-color .24s,box-shadow .24s; margin: 0px 8px;";

const textOutput = document.querySelector("#showOutput");

document.getElementById("divForForm").append(btn2);

var label = "";

btn2.addEventListener("click", fetchHandler_two);

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

// showing loading
function displayLoading() {
    loader.classList.add("display");
}

// hiding loading
function hideLoading() {
    loader.classList.remove("display");
}

async function fetchHandler_two(event) {
  var queryOptions = { active: true, currentWindow: true };
  // `tab` will either be a `tabs.Tab` instance or `undefined`.
  var [tab] = await chrome.tabs.query(queryOptions);
  console.log(tab)

  displayLoading()
  var form = document.getElementById("form")
  label = document.getElementById("fname").value

  var resp = await fetch(tab.url).then(function (response) {
    // The API call was successful!
    return response.text();
  })

  const data = {
    url: tab.url,
    macro: label,
    html: resp,
  }

  console.log(data.url + " " + data.macro + " " + data.html)

  fetch('http://localhost:5000/one_macro_html', {
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
        let d = data["products_to_question"]
        console.log(d)
        let d1 = JSON.stringify(d)
        console.log(d1)
        var result_str = ""
        for (var key in d) {
          result_str += String(key) + ": " + String(d[key]) + "\n\n"
        }
        textOutput.innerText = result_str
      })
      .catch(error => console.error('Error:', error));

};
