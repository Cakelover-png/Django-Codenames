"use strict";

import { removeChilds, locationHost } from "./utils.js";

const socket = new WebSocket(
  `ws://${locationHost}:8000/ws/game/game/?access_token=${localStorage.getItem(
    "access"
  )}&pk=${window.location.href.split("=")[1]}`
);

function getData(pkArg) {
  socket.onopen = function () {
    retrieveAction(pkArg);
  };
}

function notifyUsers(pkArg) {
  socket.send(
    JSON.stringify({
      action: "notify_users",
      request_id: new Date().getTime(),
      pk: pkArg,
    })
  );
}

function becomeSpyMaster(pkArg) {
  const [redTeamSpy, blueTeamSpy] = document.querySelectorAll(".spyBtn");
  redTeamSpy.addEventListener("click", function () {
    socket.send(
      JSON.stringify({
        action: "become_spymaster",
        request_id: new Date().getTime(),
        pk: pkArg,
        team: 0,
      })
    );
    notifyUsers(pkArg);
  });

  blueTeamSpy.addEventListener("click", function () {
    socket.send(
      JSON.stringify({
        action: "become_spymaster",
        request_id: new Date().getTime(),
        pk: pkArg,
        team: 1,
      })
    );
    notifyUsers(pkArg);
  });
}

function becomeOperative(pkArg) {
  const [redTeamCop, blueTeamCop] = document.querySelectorAll(".opBtn");
  redTeamCop.addEventListener("click", function () {
    socket.send(
      JSON.stringify({
        action: "become_field_operative",
        request_id: new Date().getTime(),
        pk: pkArg,
        team: 0,
      })
    );
    notifyUsers(pkArg);
  });

  blueTeamCop.addEventListener("click", function () {
    socket.send(
      JSON.stringify({
        action: "become_field_operative",
        request_id: new Date().getTime(),
        pk: pkArg,
        team: 1,
      })
    );
    notifyUsers(pkArg);
  });
}

function retrieveAction(pkArg) {
  console.log("set");
  socket.send(
    JSON.stringify({
      action: "retrieve",
      request_id: new Date().getTime(),
      pk: pkArg,
    })
  );
}

function socketManager(pkArg) {
  socket.onmessage = function (event) {
    const response = JSON.parse(event.data);
    console.log(response);
    console.log(response.data);
    console.log(response.action);
    if (response.action === "notify_users") {
      retrieveAction(pkArg);
    } else if (response.action === "retrieve") {
      const spymaster1 = document.querySelector(".spymaster1");
      const spymaster2 = document.querySelector(".spymaster2");
      const [operativeLabel1, operativeLabel2] =
        document.querySelectorAll(".operatives");
      const startBtn = document.querySelector(".startGameBtn");

      removeChilds(operativeLabel1);
      removeChilds(operativeLabel2);

      spymaster1.textContent = "-";
      spymaster2.textContent = "-";

      for (const spy of response.data.spymasters) {
        spy.team === 0
          ? (spymaster1.textContent = spy.player)
          : (spymaster2.textContent = spy.player);
      }

      for (const op of response.data.field_operatives) {
        const operative = document.createElement("p");
        operative.textContent = op.player;
        operative.id = op.id;
        if (op.team === 0) {
          operative.className = "operatives1";
          operativeLabel1.appendChild(operative);
        } else if (op.team === 1) {
          operative.className = "operatives2";
          operativeLabel2.appendChild(operative);
        }
      }

      if (response.data.status >= 1) {
        const cards = document.querySelectorAll(".card");
        const cardData = response.data.game_cards;
        const endBtn = document.querySelector(".endTurnBtn");
        const scoreRed = document.querySelector(".lefToGuessRed");
        const scoreBlue = document.querySelector(".lefToGuessBlue");

        scoreRed.textContent = response.data.left_red_card_count;
        scoreBlue.textContent = response.data.left_blue_card_count;

        startBtn.classList.add("none");
        for (const btn of [
          ...document.querySelectorAll(".spyBtn"),
          ...document.querySelectorAll(".opBtn"),
        ]) {
          btn.disabled = true;
        }

        for (let i = 0; i < cards.length; ++i) {
          cards[i].textContent = cardData[i].name;
          if (cardData[i].team === 0) {
            cards[i].classList.add("red");
          } else if (cardData[i].team === 1) {
            cards[i].classList.add("blue");
          }
          if (cardData[i].is_assassin) {
            cards[i].classList.add("killer");
          }
          cards[i].id = cardData[i].id;
          if (cardData[i].is_guessed) {
            cards[i].classList.add("bright");
            cards[i].classList.add("disabled");
          }
        }

        for (const card of cards) {
          card.addEventListener("click", function () {
            socket.send(
              JSON.stringify({
                action: "play",
                request_id: new Date().getTime(),
                pk: pkArg,
                game_card_pk: card.id,
              })
            );
            notifyUsers(pkArg);
          });
        }
        if (response.data.status === 1) {
          endBtn.classList.remove("hidden");
          const [info1, info2] = document.querySelectorAll(".info");
          const spyOpBtns = [
            ...document.querySelectorAll(".spyBtn"),
            ...document.querySelectorAll(".opBtn"),
          ];

          for (const btn of spyOpBtns) {
            btn.classList.add("none");
          }
          if (response.data.last_turn === 1) {
            console.log("s");
            info2.classList.add("brightDiv");
            info1.classList.remove("brightDiv");
          } else {
            info2.classList.remove("brightDiv");
            info1.classList.add("brightDiv");
          }
          endBtn.addEventListener("click", function () {
            socket.send(
              JSON.stringify({
                action: "end_turn",
                request_id: new Date().getTime(),
                pk: pkArg,
              })
            );
            notifyUsers(pkArg);
          });

          if (!response.data.can_play) {
            for (let i = 0; i < cards.length; ++i) {
              if (!cardData[i].is_guessed) {
                cards[i].classList.add("disabled");
              }
            }
            endBtn.classList.add("disabled");
          } else {
            for (let i = 0; i < cards.length; ++i) {
              if (!cardData[i].is_guessed) {
                cards[i].classList.remove("disabled");
              }
            }
            endBtn.classList.remove("disabled");
          }
        } else if (response.data.status === 2) {
          const spyOpBtns = [
            ...document.querySelectorAll(".spyBtn"),
            ...document.querySelectorAll(".opBtn"),
          ];
          const parent = document.querySelector(".header");
          const winner = document.createElement("p");
          winner.classList.add("winner");
          endBtn.classList.add("hidden");
          for (const card of cards) {
            card.classList.add("disabled");
          }

          for (const btn of spyOpBtns) {
            btn.classList.add("none");
          }

          if (response.data.last_turn === 0) {
            winner.textContent = "Red Team Won!";
          } else {
            winner.textContent = "Blue Team Won!";
          }

          const winnerSelected = document.querySelectorAll(".winner");

          if (winnerSelected.length === 1) {
            console.log("delete");
            parent.removeChild(winnerSelected[0]);
          }

          console.log("add");
          document.querySelector(".header").appendChild(winner);
        }
      } else {
        if (response.data.is_creator) {
          startBtn.classList.remove("none");
          startBtn.classList.remove("hidden");
          startBtn.addEventListener("click", function () {
            socket.send(
              JSON.stringify({
                action: "start_game",
                request_id: new Date().getTime(),
                pk: pkArg,
              })
            );
            notifyUsers(pkArg);
          });
        }
      }
    }
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

function main() {
  const pk = window.location.href.split("=")[1];
  getData(pk);
  becomeOperative(pk);
  becomeSpyMaster(pk);
  socketManager(pk);
}

main();
