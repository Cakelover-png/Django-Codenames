"use strict";
import { postXHR } from "./utils.js";
const form = document.getElementById("registerForm");
form.addEventListener("submit", function (event) {
  event.preventDefault();
  const XHR = postXHR(
    "http://127.0.0.1:8000/api/accounts/register/",
    [["Content-Type", "application/x-www-form-urlencoded"]],
    Object.fromEntries(new FormData(form).entries())
  );

  XHR.onload = function () {
    if (this.status == 201) {
      window.location.href = "../html/login.html";
    }
  };
});
