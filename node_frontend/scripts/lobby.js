"use strict";

import {
  setOrRemoveTokens,
  AUTHheader,
  createGameListTags,
  removeChilds,
  locationHost,
} from "./utils.js";

import "regenerator-runtime/runtime";
import axios from "axios";
const instance = axios.create({ baseURL: `http://${locationHost}:8000` });

async function getUserName() {
  try {
    const response = await instance.get("/api/accounts/userdata/", {
      headers: {
        Authorization: AUTHheader,
      },
    });
    console.log(response);
    document.querySelector(".userName").textContent = response.data["username"];
  } catch (error) {
    console.error(error);
  }
}

async function logout() {
  try {
    const response = await instance.post(
      "/api/accounts/logout/",
      {},
      {
        headers: {
          Authorization: AUTHheader,
        },
      }
    );
    console.log(response);
    window.location.href = "./index.html";
    setOrRemoveTokens(true);
  } catch (error) {
    console.error(error);
  }
}

async function getGames() {
  try {
    const response = await instance.get("/api/games/games/", {
      headers: {
        Authorization: AUTHheader,
      },
    });
    console.log(response);
    for (const game of response.data) {
      createGameListTags(
        game["creator"],
        game["player_count_in_lobby"],
        game["status"],
        game["id"]
      );
    }
  } catch (error) {
    console.error(error);
  }
}

async function createGames() {
  try {
    const response = await instance.post(
      "/api/games/games/",
      {},
      {
        headers: {
          Authorization: AUTHheader,
        },
      }
    );
    console.log(response);
    window.location.href = `./game.html?id=${response.data.id}`;
  } catch (error) {
    console.error(error);
  }
}

function joinButton() {
  document.addEventListener("click", function (e) {
    if (e.target && e.target.id == "join") {
      const pk = e.target.href.split("=");
      const socket = new WebSocket(
        `ws://${locationHost}:8000/ws/game/game/?access_token=${
          AUTHheader.split(" ")[1]
        }&pk=${pk[1]}`
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
  logoutBTN.addEventListener("click", function (e) {
    e.preventDefault();
    logout();
  });
  getGames();
  const refreshBTN = document.querySelector(".refreshBtn");
  refreshBTN.addEventListener("click", function (e) {
    e.preventDefault();
    const gameSection = document.querySelector(".gameSection");
    removeChilds(gameSection);
    getGames();
  });
  const createBTN = document.querySelector(".createBTN");
  createBTN.addEventListener("click", function (e) {
    e.preventDefault();
    createGames();
  });
  joinButton();
}

main();
