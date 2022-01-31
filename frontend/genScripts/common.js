"use strict";

function sendRefresh(refresh) {
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "http://127.0.0.1:8000/api/accounts/token/refresh/", true);

  //Send the proper header information along with the request
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

  xhr.onreadystatechange = function () {
    // Call a function when the state changes.
    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
      // Request finished. Do processing here.
    }
  };
  xhr.send(`refresh=${refresh}`);
  return xhr;
}

function getUserData() {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "http://127.0.0.1:8000/api/accounts/userdata/", true);

  xhr.setRequestHeader(
    "Authorization",
    "JWT " + localStorage.getItem("access")
  );

  xhr.send(null);
  return xhr;
}

if (localStorage.getItem("access")) {
  const XHR = getUserData();
  XHR.onload = function () {
    if (this.status === 403) {
      const xhr = sendRefresh(localStorage.getItem("refresh"));
      xhr.onload = function () {
        if (this.status === 403) {
          console.log(this.responseText);
          const jsonResponse = JSON.parse(this.responseText);
          localStorage.setItem("access", jsonResponse["access"]);
          localStorage.setItem("refresh", jsonResponse["refresh"]);
          window.location = "../lobby/lobby.html";
        } else {
          localStorage.removeItem("access");
          localStorage.removeItem("refresh");
          window.location = "../login/login.html";
        }
      };
    } else {
      window.location = "../lobby/lobby.html";
    }
  };
}
