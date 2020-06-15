"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
const endpoint = '/api/v1/';

let html_consumption, html_percentage, currentProgress, html_wave, html_goal, dailyGoal, user, html_user;

const updateView = function(progressInPercentage) {
  html_percentage.innerHTML = progressInPercentage;
  html_wave.style.transform = `translateY(${100 - progressInPercentage}%)`;
}

const listenToSocket = function () {
  socket.on("connect", function () {
    console.log("verbonden met socket webserver");
    socket.emit('F2B_dashboard');
  });

  socket.on("B2F_update_consumption", function (jsonObject) {
    console.log("Update consumption:", jsonObject);
    html_consumption.innerHTML = jsonObject.waarde;
    currentProgress = jsonObject.waarde;
    const progressInPercentage = Math.ceil((currentProgress / dailyGoal) * 100);
    console.log(`Huidig aantal ml gedronken is ${jsonObject.currentProgress}`);
    updateView(progressInPercentage);
    user = jsonObject.userid;
    getProcessData(user);
  });

  socket.on("B2F_update_user", function (jsonObject) {
    console.log("Update user:", jsonObject);
    html_user.innerHTML = jsonObject.waarde;
  })

  socket.on("B2F_update_goal", function (jsonObject) {
    console.log("Update goal:", jsonObject);
    html_goal.innerHTML = jsonObject.waarde+' ml';
    dailyGoal = jsonObject.waarde;
  });
};

const showTableData = function (data) {
  console.log(data)
  const table = document.querySelector(".js-table");
  let tableHTML = ``
  for(const row of data) {
      tableHTML += `
      <div class="o-layout o-layout--gutter-lg">
        <div class="o-layout__item">
            <div class="o-infoblock__white">
                <div class="o-textleft">
                    <h3>
                    ${row.Value} ml
                    </h3>
                </div>
                <div class="o-textright">
                    <span class="c-lead js-waterlevel">${row.HistoryDate}</span>
                </div>
            </div>
        </div>
      </div>`;
  }
  table.innerHTML = tableHTML;
};

const getProcessData = function(user) {
  handleData(`http://${lanIP}/${user}/consumption`, showTableData, null, "GET");
};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  html_consumption = document.querySelector('.js-consumption');
  html_wave = document.querySelector('.js-wave');
  html_percentage = document.querySelector('.js-percentage');
  html_goal = document.querySelector('.js-goal');
  html_user = document.querySelector('.js-nickname');
  listenToSocket();
});
