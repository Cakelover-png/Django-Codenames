"use strict";

function getData(pkArg) {
  const socket = new WebSocket(
    `ws://127.0.0.1:8000/ws/game/game/?access_token=${localStorage.getItem(
      "access"
    )}`
  );

  socket.onopen = function () {
    socket.send(
      JSON.stringify({
        action: "retrieve",
        request_id: new Date().getTime(),
        pk: pkArg,
      })
    );
  };

  socket.onmessage = function (event) {
    const response = JSON.parse(event.data);
    const spymaster1 = document.querySelector(".spymaster1");
    const spymaster2 = document.querySelector(".spymaster2");
    const cards = document.querySelectorAll(".card");
    const cardData = response.data.game_cards;
    const [operativeLabel1, operativeLabel2] =
      document.querySelectorAll(".operatives");

    console.log(operativeLabel1);

    console.log(response.data);
    console.log(response.data.spymasters);

    for (const spy of response.data.spymasters) {
      spy.team === 0
        ? (spymaster1.textContent = spy.player)
        : (spymaster2.textContent = spy.player);
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
    }

    for (const op of response.data.field_operatives) {
      const operative = document.createElement("p");
      operative.textContent = op.player;
      operative.id = op.id;
      if (op.team === 0) {
        console.log(op.team);
        operative.className = "operatives1";
        operativeLabel1.appendChild(operative);
      } else if (op.team === 1) {
        operative.className = "operatives2";
        operativeLabel2.appendChild(operative);
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
  const pk = window.location.href.split("=");
  getData(pk[1]);
}

main();
