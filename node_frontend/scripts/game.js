"use strict";

import { removeChilds } from "./utils.js";

const socket = new WebSocket(
  `ws://127.0.0.1:8000/ws/game/game/?access_token=${localStorage.getItem(
    "access"
  )}&pk=${window.location.href.split("=")[1]}`
);

function getData(pkArg) {
  socket.onopen = function () {
    retrieveAction(pkArg);
  };
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
    console.log(response)
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

      startBtn.classList.add("hidden");
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
        });
      }
      if (response.data.status === 1) {
        endBtn.classList.remove("hidden");

        endBtn.addEventListener("click", function () {
          socket.send(
            JSON.stringify({
              action: "end_turn",
              request_id: new Date().getTime(),
              pk: pkArg,
            })
          );
        });

        if (!response.data.can_play) {
          console.log(2);
          for (const card of cards) {
            card.classList.add("disabled");
          }
          endBtn.classList.add("disabled");
        } else {
          for (const card of cards) {
            card.classList.remove("disabled");
          }
          endBtn.classList.remove("disabled");
        }
      } else if (response.status === 2) {
        endBtn.classList.add("hidden");
        for (const card of cards) {
          card.classList.add("disabled");
        }
      }
    } else {
      if (response.data.is_creator) {
        startBtn.classList.remove("hidden");
        startBtn.addEventListener("click", function () {
          socket.send(
            JSON.stringify({
              action: "start_game",
              request_id: new Date().getTime(),
              pk: pkArg,
            })
          );
        });
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
  getData(pk)
  becomeOperative(pk);
  becomeSpyMaster(pk);
  socketManager(pk);
}

main();
