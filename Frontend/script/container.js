"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
const endpoint = '/api/v1/';
var intervalID = window.setInterval(myCallback, 2000);

let html_temp, html_waterlevel;

function myCallback() {
  socket.emit("F2B_Check")
}

const listenToSocket = function () {
  socket.on("connect", function () {
    console.log("verbonden met socket webserver");
    socket.emit('F2B_container');
  });

  socket.on("B2F_update_temperature", function (jsonObject) {
    console.log("Update temperature:", jsonObject);
    console.log(html_temp)
    html_temp.innerHTML = jsonObject.waarde+' °C';
  });

  socket.on("B2F_update_waterlevel", function (jsonObject) {
    console.log("Update water level:", jsonObject);
    html_waterlevel.innerHTML = jsonObject.waarde+' %';
  });
};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  html_temp = document.querySelector('.js-temperature');
  html_waterlevel = document.querySelector('.js-waterlevel')
  listenToSocket();
});
