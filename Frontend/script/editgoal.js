"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
const endpoint = '/api/v1/';
const dailyGoal = 2000;

let html_button, html_goal, addButton;

const listenToSocket = function () {
  socket.on("connect", function () {
    console.log("verbonden met socket webserver");
    socket.emit('F2B_editgoal')
  });

  socket.on("B2F_update_goal", function (jsonObject) {
    console.log("Update total:", jsonObject);
    html_goal.innerHTML = jsonObject.waarde+' ml';
  });
};

const callbackAddedGoal = function(jsonObject){
    console.log(jsonObject);
  };

const listenToChangeGoal = function(){
  addButton.addEventListener("click", function(){
    const newGoal = document.querySelector(".js-change-goal");
    socket.emit("F2B_change_goal", {goal: newGoal.value});
  });
};

const init = function () {
    console.log("init initiated!");
    html_goal = document.querySelector('.js-goal');
    addButton = document.querySelector(".js-button-change-goal");
    listenToSocket();
    listenToChangeGoal();
};
  
document.addEventListener("DOMContentLoaded", init);
  