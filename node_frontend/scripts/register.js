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
    console.error(error);
  }
}
form.addEventListener("submit", function (event) {
  event.preventDefault();
  registerUser();
});
