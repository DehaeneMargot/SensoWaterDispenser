"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
const endpoint = '/api/v1/';
const dailyGoal = 2000;

let html_nickname, html_new_user, addButton;

const listenToSocket = function () {
  socket.on("connect", function () {
    console.log("verbonden met socket webserver");
    socket.emit('F2B_onboarding')
  });

  socket.on("B2F_user", function (jsonObject) {
    console.log("User:", jsonObject);
    let nicknameHTML = ``
    nicknameHTML += `
      <div class="o-layout__item">
        <h7>
          Welcome <span class="c-lead">${jsonObject.waarde}</span>
        </h7>
      </div>
      <div class="o-layout__item">
        <h3>
          If this is you, press next to continue
        </h3>
      </div>
      <div class="o-layout__item">
        <a href="dashboard.html" class="c-cta-button">
          NEXT
        </a>
      </div>`
  if (html_nickname) {
    html_nickname.innerHTML = nicknameHTML;
  }
  });


  socket.on("B2F_new_user", function (jsonObject) {
    console.log("User:", jsonObject);
    let newuserHTML = ``
    newuserHTML += `
    <div class="o-layout o-layout--gutter-lg">
      <h1 class="o-layout__item">
          Register
      </h1>
    </div>
    <div class="o-layout o-layout--gutter-lg">
        <div class="o-layout__item">
            <label for="nickname">User name</label>
            <input class="c-input-field js-add-nickname" type="text" id="nickname" name="nickname" required/>
            <label for="firstname">First name</label>
            <input class="c-input-field js-add-firstname" type="text" id="firstname" name="firstname" required/>
            <label for="lastname">Last name</label>
            <input class="c-input-field js-add-lastname" type="text" id="lastname" name="lastname" required/>
            <label for="nickname">Password</label>
            <input class="c-input-field js-add-password" type="password" id="password" name="password" required/>
            <label for="containerid">Container ID</label>
            <input class="c-input-field js-add-container" type="text" id="containerid" name="containerid" required/>
        </div>
      </div>
      <div class="o-layout o-layout--gutter-lg o-layout--align-center">
        <div class="o-layout__item">
          <a href="index.html" type="submit" class="c-cta-button--lg">Back</a>
          <a href="index.html" type="submit" class="c-cta-button--lg js-button-add-user">Register</a>
        </div>
      </div>
    </div>`
  html_new_user.innerHTML = newuserHTML;
  addButton = document.querySelector(".js-button-add-user");
  listenToAddUser();
  });

  const listenToAddUser = function(){
    addButton.addEventListener("click", function(){
      const nickname = document.querySelector(".js-add-nickname");
      const firstname = document.querySelector(".js-add-firstname");
      const lastname = document.querySelector(".js-add-lastname");
      const password = document.querySelector(".js-add-password");
      const container = document.querySelector(".js-add-container");
      socket.emit("F2B_add_user", {nickname: nickname.value,firstname: firstname.value, lastname: lastname.value, password: password.value, container: container.value});
    });
  };
};



document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  html_nickname = document.querySelector('.js-nickname');
  html_new_user = document.querySelector('.js-new-user');
  listenToSocket();
});