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
    window.location.href = "../html/index.html";
    setOrRemoveTokens(true);
  };
}

function getGames() {
  const XHR = getXHR("http://127.0.0.1:8000/api/games/games/", [AUTHheader]);
  const buttons = [];

  XHR.onload = function () {
    const jsonResponse = JSON.parse(this.responseText);
    for (const game of jsonResponse) {
      createGameListTags(
        game["creator"],
        game["player_count_in_lobby"],
        game["status"],
        game["id"]
      );
    }
  };
  return buttons;
}

function createGames() {
  const XHR = postXHR(
    "http://127.0.0.1:8000/api/games/games/",
    [AUTHheader],
    {}
  );

  XHR.onload = function () {
    window.location.href = "../html/game.html?id=2";
  };
}

function joinButton() {
  document.addEventListener("click", function (e) {
    if (e.target && e.target.id == "join") {
      const pk = e.target.href.split("=");
      const socket = new WebSocket(
        `ws://127.0.0.1:8000/ws/game/game/?access_token=${localStorage.getItem(
          "access"
        )}`
      );
      socket.onopen = function () {
        socket.send(
          JSON.stringify({
            action: "join_game",
            request_id: new Date().getTime(),
            pk: pk[1],
          })
        );
      };

      socket.onmessage = function (event) {
        alert(`[message] Data received from server: ${event.data}`);
      };

      socket.onclose = function (event) {
        if (event.wasClean) {
          alert(
            `[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`
          );
        } else {
          // e.g. server process killed or network down
          // event.code is usually 1006 in this case
          alert("[close] Connection died");
        }
      };

      socket.onerror = function (error) {
        alert(`[error] ${error.message}`);
      };
    }
  });
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
    const gameSection = document.querySelector(".gameSection");
    removeChilds(gameSection);
    getGames();
  });
  const createBTN = document.querySelector(".createBTN");
  createBTN.addEventListener("click", function () {
    createGames();
  });
  joinButton();
}
main();
