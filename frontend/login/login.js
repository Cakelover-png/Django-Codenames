"use strict";
window.addEventListener("load", function () {
  function sendData(url) {
    const XHR = new XMLHttpRequest();

    // Bind the FormData object and the form element
    const FD = new FormData(form);

    // Set up our request
    XHR.open("POST", url);
    // The data sent is what the user provided in the form
    XHR.send(FD);

    return XHR;
  }
  // Access the form element...
  const form = document.getElementById("loginForm");
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const xhr = sendData("http://127.0.0.1:8000/api/accounts/token/");

    xhr.addEventListener("load", function (event) {
      const data = event.target.responseText;
      const jsonResponse = JSON.parse(data);
      alert(data);
      localStorage.setItem("access", jsonResponse["access"]);
      localStorage.setItem("refresh", jsonResponse["refresh"]);
    });
    console.log(event.target.responseText);
  });
});
