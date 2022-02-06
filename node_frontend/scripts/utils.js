"use strict";
// import "regenerator-runtime/runtime";
// import axios from "axios";

export const AUTHheader = "JWT " + localStorage.getItem("access");
export const locationHost = window.location.hostname;
// const instance = axios.create({ baseURL: "http://localhost:8000" });
// export async function getAUTHheader() {
//   const accessToken = "JWT " + localStorage.getItem("access");
//   try {
//     await instance.get("/api/accounts/userdata/", {
//       headers: {
//         Authorization: accessToken,
//       },
//     });
//     return accessToken;
//   } catch (error) {
//     console.error(error);
//     try {
//       const response = await instance.post("/api/accounts/token/refresh/", {
//         refresh: localStorage.getItem("refresh"),
//       });
//       setOrRemoveTokens(false, response.data.access, response.data.refresh);
//       return `JWT ${response.data.access}`;
//     } catch (error) {
//       console.error(error);
//     }
//   }
// }

export function setOrRemoveTokens(remove, access = null, refresh = null) {
  if (!remove) {
    if (!access) {
      localStorage.setItem("refresh", refresh);
    } else {
      localStorage.setItem("access", access);
      localStorage.setItem("refresh", refresh);
    }
  } else {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
  }
}

export function createGameListTags(creatorArg, count, status, id) {
  const gameSection = document.querySelector(".gameSection");

  const gameDiv = document.createElement("div");
  gameDiv.className = "game";
  const creator = document.createElement("p");
  creator.className = "creator";
  const playersCount = document.createElement("p");
  playersCount.className = "playerCount";
  const gameStatus = document.createElement("p");
  gameStatus.className = "gameStatus";

  const joinButton = document.createElement("a");
  joinButton.textContent = "Join";
  joinButton.className = "joinBtn";
  joinButton.id = "join";
  joinButton.href = `./game.html?id=${id}`;

  const gameInfo = document.createElement("div");
  gameInfo.className = "gameInfo";
  const joinGame = document.createElement("div");
  joinGame.className = "joinGame";

  let row = document.createElement("div");
  row.className = "row";
  if (!document.querySelector(".row")) {
    gameSection.appendChild(row);
  }

  row =
    document.querySelectorAll(".row")[
      document.querySelectorAll(".row").length - 1
    ];

  if (row.childElementCount < 3) {
    row.appendChild(gameDiv);
  } else if (row.childElementCount === 3) {
    row = document.createElement("div");
    row.className = "row";
    gameSection.appendChild(row);
    row.appendChild(gameDiv);
  }

  gameDiv.appendChild(gameInfo);
  gameDiv.appendChild(joinGame);
  gameInfo.appendChild(creator);
  gameInfo.appendChild(playersCount);
  gameInfo.appendChild(gameStatus);
  joinGame.appendChild(joinButton);

  creator.textContent = `Creator: ${creatorArg}`;
  playersCount.textContent = `Players: ${count}`;
  let str = "";
  if (status === 0) {
    str = "Not Started";
  } else if (status === 1) {
    str = "In Progress";
  } else {
    str = "Finished";
  }
  gameStatus.textContent = str;
}

export function removeChilds(parent) {
  while (parent.lastChild) {
    parent.removeChild(parent.lastChild);
  }
}
