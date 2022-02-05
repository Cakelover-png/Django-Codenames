"use strict";
import "regenerator-runtime/runtime";
import axios from "axios";
const form = document.getElementById("registerForm");

const instance = axios.create({ baseURL: "http://localhost:8000" });

async function registerUser() {
  try {
    const response = await instance.post(
      "/api/accounts/register/",
      new FormData(form),
      {
        "Content-Type": "application/x-www-form-urlencoded",
      }
    );
    console.log(response);
    window.location.href = "http://localhost:1234/login.html";
    setOrRemoveTokens(true);
  } catch (error) {
    console.error(error);
  }
}
form.addEventListener("submit", function (event) {
  event.preventDefault();
  registerUser();
});
