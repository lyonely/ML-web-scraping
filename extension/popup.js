let button = document.createElement("button");
let button2 = document.createElement("button");

button.innerHTML = "Single Product";
button.style.cssText = "border: 0; outline: 0; cursor: pointer; color: rgb(60, 66, 87);background-color: rgb(255, 255, 255);box-shadow: rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 12%) 0px 1px 1px 0px, rgb(60 66 87 / 16%) 0px 0px 0px 1px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(60 66 87 / 8%) 0px 2px 5px 0px;border-radius: 4px;font-size: 14px;font-weight: 500;padding: 0px 8px;display: inline-block;min-height: 28px;transition: background-color .24s,box-shadow .24s; margin: 0px 8px;";

button2.innerHTML = "List of Products";
button2.style.cssText = "border: 0; outline: 0; cursor: pointer; color: rgb(60, 66, 87);background-color: rgb(255, 255, 255);box-shadow: rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 12%) 0px 1px 1px 0px, rgb(60 66 87 / 16%) 0px 0px 0px 1px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(60 66 87 / 8%) 0px 2px 5px 0px;border-radius: 4px;font-size: 14px;font-weight: 500;padding: 0px 8px;display: inline-block;min-height: 28px;transition: background-color .24s,box-shadow .24s;";

const textOutput = document.querySelector("#showOutput");

document.getElementById("divForForm").append(button);
document.getElementById("divForForm").append(button2);

var label = "";

button.addEventListener("click", fetchHandler);
button2.addEventListener("click", fetchHandler_two);

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

async function fetchHandler(event) {
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

  fetch('http://34.89.147.237:5000/one_macro_html', {
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

async function fetchHandler_two(event) {
  let queryOptions = { active: true, currentWindow: true };
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

  const response = fetch(data.url).then(function (response) {
    // The API call was successful!
    return response.text();
  }).then(function (html) {
    // This is the HTML from our response as a text string
    console.log(html);
  }).catch(function (err) {
    // There was an error
    console.warn('Something went wrong.', err);
  });

  console.log(data.url + " " + data.macro)

  fetch('http://34.89.147.237:5000/macro', {
    method: 'POST',
    mode: 'cors',
    body: JSON.stringify(data),
    headers: {
      'Content-type': 'application/json'
    }
  })
    .then(function (response) {
      console.log(response)
      return response.json()
    })
    .then(function (data) {
      hideLoading()
      console.log(data)
      displayOutput()
      let d = data.products_to_question
      console.log(d)
      let d1 = JSON.stringify(d)
      var result_str = ""
      for (var key in d) {
        result_str += String(key) + ": " + String(d[key]) + "\n\n"
      }
      textOutput.innerText = result_str
    })
    .catch(error => console.error('Error:', error));

};
