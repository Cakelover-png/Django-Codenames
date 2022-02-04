"use strict";
export const AUTHheader = [
  "Authorization",
  "JWT " + localStorage.getItem("access"),
];
export function objToString(data) {
  let str = "";
  for (let [key, value] of Object.entries(data)) {
    str += `${key}=${value}&`;
  }
  console.log(str.substring(0, str.length - 1));
  return str.substring(0, str.length - 1);
}

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

export function getXHR(url, headers) {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", url, true);

  for (const header of headers) {
    xhr.setRequestHeader(header[0], header[1]);
  }

  xhr.send(null);
  return xhr;
}

export function postXHR(url, headers, data) {
  const xhr = new XMLHttpRequest();
  xhr.open("POST", url, true);

  //Send the proper header information along with the request
  for (const header of headers) {
    xhr.setRequestHeader(header[0], header[1]);
  }

  xhr.send(objToString(data));
  return xhr;
}

export function postFormXHR(url, headers, data) {
  const xhr = new XMLHttpRequest();
  xhr.open("POST", url, true);

  //Send the proper header information along with the request
  for (const header of headers) {
    xhr.setRequestHeader(header[0], header[1]);
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
  joinButton.href = `../html/game.html?id=${id}`;

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

  gameDiv.appendChild(creator);
  gameDiv.appendChild(playersCount);
  gameDiv.appendChild(gameStatus);
  gameDiv.appendChild(joinButton);

  creator.textContent = creatorArg;
  playersCount.textContent = count;
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
