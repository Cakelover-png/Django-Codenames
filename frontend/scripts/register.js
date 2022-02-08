"use strict";
import { locationHost } from "./utils.js";
import "regenerator-runtime/runtime";
import axios from "axios";
const form = document.getElementById("registerForm");

const instance = axios.create({ baseURL: `http://${locationHost}:8000` });

async function registerUser() {
  try {
    const response = await instance.post(
      "/api/accounts/register/",
      new FormData(form),
      {
        "Content-Type": "application/x-www-form-urlencoded",
      }
    );
    window.location.href = `http://${locationHost}:1234/login.html`;
    setOrRemoveTokens(true);
  } catch (error) {
    const userName = document.getElementById("user");
    const password = document.getElementById("pasw");
    const confirmPassword = document.getElementById("confirm");
    if (error.response.data.username) {
      userName.placeholder = error.response.data.username;
      userName.value = "";
    }
    if (error.response.data.password) {
      password.placeholder = error.response.data.password;
      password.value = "";
    }
    if (error.response.data.confirm_password) {
      confirmPassword.placeholder = error.response.data.confirm_password;
      confirmPassword.value = "";
    }
  }
}
form.addEventListener("submit", function (event) {
  event.preventDefault();
  registerUser();
});
