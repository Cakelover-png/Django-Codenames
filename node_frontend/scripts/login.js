"use strict";
import { setOrRemoveTokens, locationHost } from "./utils.js";
import "regenerator-runtime/runtime";
import axios from "axios";
const form = document.getElementById("loginForm");

const instance = axios.create({ baseURL: `http://${locationHost}:8000` });
async function loginUser() {
  try {
    const response = await instance.post(
      "/api/accounts/token/",
      new FormData(form),
      {
        "Content-Type": "application/x-www-form-urlencoded",
      }
    );
    window.location.href = `http://${locationHost}:1234/lobby.html`;
    setOrRemoveTokens(false, response.data.access, response.data.refresh);
  } catch (error) {
    console.error(error);
  }
}

form.addEventListener("submit", function (event) {
  event.preventDefault();
  loginUser();
});
