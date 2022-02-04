"use strict";
import { setOrRemoveTokens, getXHR, postXHR, AUTHheader } from "./utils.js";

export function loginValidation() {
  if (localStorage.getItem("access")) {
    const XHR = getXHR("http://127.0.0.1:8000/api/accounts/userdata/", [
      AUTHheader,
    ]);
    XHR.onload = function () {
      if (this.status === 403) {
        const XHR = postXHR(
          "http://127.0.0.1:8000/api/accounts/token/refresh/",
          [["Content-Type", "application/x-www-form-urlencoded"]],
          {
            refresh: localStorage.getItem("refresh"),
          }
        );
        XHR.onload = function () {
          if (this.status === 200) {
            console.log(this.responseText);
            const jsonResponse = JSON.parse(this.responseText);
            setOrRemoveTokens(
              false,
              jsonResponse["access"],
              jsonResponse["refresh"]
            );
            window.location.href = "../html/lobby.html";
          } else {
            setOrRemoveTokens(true);
            window.location.href = "../html/login.html";
          }
        };
      } else if (this.status === 200) {
        window.location.href = "../html/lobby.html";
      }
    };
  }
}
