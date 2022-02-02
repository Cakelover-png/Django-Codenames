"use strict";
import {
  getXHR,
  postXHR,
  setOrRemoveTokens,
  AUTHheader,
  createGameListTags,
  removeChilds,
} from "./utils.js";

function getUserName() {
  const XHR = getXHR("http://127.0.0.1:8000/api/accounts/userdata/", [
    AUTHheader,
  ]);

  XHR.onload = function () {
    const jsonResponse = JSON.parse(this.responseText);
    document.querySelector(".userName").textContent = jsonResponse["username"];
  };
}

function logout() {
  const XHR = postXHR(
    "http://127.0.0.1:8000/api/accounts/logout/",
    [AUTHheader],
    {}
  );
  XHR.onload = function () {
    setOrRemoveTokens(true);
    window.location = "../html/index.html";
  };
}

function getGames() {
  const XHR = getXHR("http://127.0.0.1:8000/api/games/games/", [AUTHheader]);

  XHR.onload = function () {
    const jsonResponse = JSON.parse(this.responseText);
    for (const game of jsonResponse) {
      createGameListTags(
        game["creator"],
        game["player_count_in_lobby"],
        game["status"]
      );
    }
  };
}

function createGames() {
  const XHR = postXHR(
    "http://127.0.0.1:8000/api/games/games/",
    [AUTHheader],
    {}
  );

  XHR.onload = function () {
    window.location = "../html/game.html?id=2";
  };
}

function main() {
  getUserName();
  const logoutBTN = document.querySelector(".logoutBtn");
  logoutBTN.addEventListener("click", function () {
    logout();
  });
  getGames();
  const refreshBTN = document.querySelector(".refreshBtn");
  refreshBTN.addEventListener("click", function () {
    removeChilds(document.querySelector(".main"));
    getGames();
  });
  const createBTN = document.querySelector(".createBTN");
  createBTN.addEventListener("click", function () {
    createGames();
  });
}
main();
