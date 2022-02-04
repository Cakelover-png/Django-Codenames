"use strict";
import { postXHR, setOrRemoveTokens } from "./utils.js";
const form = document.getElementById("loginForm");

form.addEventListener("submit", function (event) {
  event.preventDefault();
  const XHR = postXHR(
    "http://127.0.0.1:8000/api/accounts/token/",
    [["Content-Type", "application/x-www-form-urlencoded"]],
    Object.fromEntries(new FormData(form).entries())
  );

  XHR.onload = function () {
    if (this.status == 200) {
      const jsonResponse = JSON.parse(this.responseText);
      // alert(jsonResponse["access"]);
      setOrRemoveTokens(false, jsonResponse["access"], jsonResponse["refresh"]);
      window.location.href = "../html/lobby.html";
    }
    // console.log(this.responseText);
  };
});
