// let btn = document.createElement("button");

// btn.innerHTML = "Scrape list of products";
// btn.id = "x"

// btn.style.cssText = "border: 0; outline: 0; cursor: pointer; color: rgb(60, 66, 87);background-color: rgb(255, 255, 255);box-shadow: rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 12%) 0px 1px 1px 0px, rgb(60 66 87 / 16%) 0px 0px 0px 1px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(60 66 87 / 8%) 0px 2px 5px 0px;border-radius: 4px;font-size: 14px;font-weight: 500;padding: 0px 8px;display: inline-block;min-height: 28px;transition: background-color .24s,box-shadow .24s;";

// document.getElementById("divForForm").append(btn);

// const textOutput = document.querySelector("#showOutput");

// // btn.style.background = "#3dfe3a";

// document.body.appendChild(btn);
// var label = "";

// btn.addEventListener("click", fetchHandler);

// // selecting loading div
// const loader = document.querySelector("#loading");

// // showing loading
// function displayLoading() {
//     loader.classList.add("display");
// }

// // hiding loading 
// function hideLoading() {
//     loader.classList.remove("display");
// }

// async function fetchHandler(event) {
//   let queryOptions = { active: true, lastFocusedWindow: true };
//   // `tab` will either be a `tabs.Tab` instance or `undefined`.
//   let [tab] = await chrome.tabs.query(queryOptions);
//   console.log(tab)

//   displayLoading()
//   var form = document.getElementById("form")
//   label = document.getElementById("fname").value

//   const data = {
//     url: tab.url,
//     macro: label,
//   }

//   console.log(data.url + " " + data.macro)

//   fetch('http://34.107.31.3:5000/macro', {
//     method: 'POST',
//       mode: 'cors',
//       body: JSON.stringify(data),
//       headers: {
//         'Content-type': 'application/json'
//       }
//       })
//       .then(function(response) {
//         console.log(response)
//         return response.json()})
//       .then(function(data){
//         hideLoading()
//         console.log(data)
//         displayOutput()
//         let d = data.products_to_keyword
//         var result_str = ""
//         for (var key in d){
//           var link = document.createElement('a');
//           link.href = String(key);
//           link.innerHTML = String(key);
//           result_str += link + ": " +  String(d[key]) + "\n" + "\n"
//           console.log(result_str);
//           // result_str += String(key) + ": " +  String(d[key]) + "\n" + "\n"
//           // console.log(result_str);
//         }
//         textOutput.innerText = result_str
//       })
//       .catch(error => console.error('Error:', error));

// };

let btn = document.createElement("button");

let btn2 = document.createElement("button");

btn.innerHTML = "List of Products";
btn.style.cssText = "border: 0; outline: 0; cursor: pointer; color: rgb(60, 66, 87);background-color: rgb(255, 255, 255);box-shadow: rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 12%) 0px 1px 1px 0px, rgb(60 66 87 / 16%) 0px 0px 0px 1px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(60 66 87 / 8%) 0px 2px 5px 0px;border-radius: 4px;font-size: 14px;font-weight: 500;padding: 0px 8px;display: inline-block;min-height: 28px;transition: background-color .24s,box-shadow .24s;";

btn2.innerHTML = "Single Product";
btn2.style.cssText = "border: 0; outline: 0; cursor: pointer; color: rgb(60, 66, 87);background-color: rgb(255, 255, 255);box-shadow: rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 12%) 0px 1px 1px 0px, rgb(60 66 87 / 16%) 0px 0px 0px 1px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(0 0 0 / 0%) 0px 0px 0px 0px, rgb(60 66 87 / 8%) 0px 2px 5px 0px;border-radius: 4px;font-size: 14px;font-weight: 500;padding: 0px 8px;display: inline-block;min-height: 28px;transition: background-color .24s,box-shadow .24s; margin: 0px 8px;";

const textOutput = document.querySelector("#showOutput");

// btn.style.background = "#3dfe3a";

document.getElementById("divForForm").append(btn);
document.getElementById("divForForm").append(btn2);

var label = "";

btn.addEventListener("click", fetchHandler);

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

  fetch('http://34.116.140.226:5000/macro', {
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
          result_str += String(key) + ": " +  String(d[key]) + "\n\n"
        }
        textOutput.innerText = result_str
      })
      .catch(error => console.error('Error:', error));

};

async function fetchHandler_two(event) {
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

  fetch('http://34.159.89.241:5000/one_macro', {
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
        let d = data["products_to_keyword"]
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

