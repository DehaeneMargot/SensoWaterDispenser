"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
const endpoint = '/api/v1/';

let html_total, html_average, user;

const listenToSocket = function () {
  socket.on("connect", function () {
    console.log("verbonden met socket webserver");
    socket.emit('F2B_statistics')
  });

  socket.on("B2F_update_total", function (jsonObject) {
    console.log("Update total:", jsonObject);
    html_total.innerHTML = jsonObject.waarde+' ml';
    user = jsonObject.userid;
    getConsumptionData(user);
    getGoalData(user);
  });

  socket.on("B2F_update_average", function (jsonObject) {
    console.log("Update average:", jsonObject);
    html_average.innerHTML = jsonObject.waarde+' ml';
  });
};

//charts
const showDataTemp = function(data) {
  console.log(data)

  let converted_labels = [];
  let converted_data = [];
  for(let i = data.length-1; i >= 0; i--) {
      converted_labels.push(data[i].DateTime);
      converted_data.push(data[i].HistoryValue);
  }
  drawChartTemp(converted_labels, converted_data) //x en y
};

const showGoals = function(data) {
    console.log(data)
  
    let converted_labels = [];
    let converted_data = [];
    for(let i = data.length-1; i >= 0; i--) {
        converted_labels.push(data[i].Datetime);
        converted_data.push(data[i].DailyGoal);
    }
    drawChartGoals(converted_labels, converted_data) //x en y
};

const showDataConsumption = function(data) {
  console.log(data)

  let converted_labels = [];
  let converted_data = [];
  for (const element of data) {
      converted_labels.push(element.DateTime);
      converted_data.push(element.HistoryValue);
  }
  drawChartConsumption(converted_labels, converted_data) //x en y
};

const drawChartTemp = function(labels, data) {
  let ctx = document.querySelector(".js-charttemp").getContext('2d');

  let config = {
      type: 'line',
      data: {
          labels: labels,
          datasets: [
              {
                  label: 'Temperature', //label at the top
                  backgroundColor: 'white', //styling
                  borderColor: '#1D4873', //styling
                  data: data, //data binded to the chart
                  fill: false //styling
              }
          ]
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
          title: {
              display: false
          },
          tooltips: {
              mode:'index',
              intersect: true
          },
          hover: {
              mode: 'nearest',
              intersect: true
          },
          scales: {
              xAxes: [
                  {
                      display: true,
                      scaleLabel: {
                          display: true,
                          labelString: 'Time'
                      }
                  }
              ],
              yAxes: [
                  {
                      display:true,
                      scaleLabel: {
                          display: true,
                          labelString: 'Value'
                      }
                  }
              ]
          }
      }
  };

  let myChart = new Chart(ctx, config);
}

const drawChartGoals = function(labels, data) {
    let ctx = document.querySelector(".js-chartgoals").getContext('2d');
  
    let config = {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Goals', //label at the top
                    backgroundColor: 'white', //styling
                    borderColor: '#1D4873', //styling
                    data: data, //data binded to the chart
                    fill: false //styling
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: false
            },
            tooltips: {
                mode:'index',
                intersect: true
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [
                    {
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Time'
                        }
                    }
                ],
                yAxes: [
                    {
                        display:true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Goal'
                        }
                    }
                ]
            }
        }
    };
  
    let myChart = new Chart(ctx, config);
}

const drawChartConsumption = function(labels, data) {
  let ctx = document.querySelector(".js-chartconsumption").getContext('2d');

  let config = {
    type: 'line',
    data: {
          labels: labels,
          datasets: [
              {
                  label: 'Consumption', //label at the top
                  backgroundColor: 'white', //styling
                  borderColor: '#1D4873', //styling
                  data: data, //data binded to the chart
                  fill: false //styling
              }
          ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        title: {
            display: false
        },
        tooltips: {
            mode:'index',
            intersect: true
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [
                {
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }
            ],
            yAxes: [
                {
                    display:true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                }
            ]
        }
    }
  };

  let myChart = new Chart(ctx, config);
}
const getTemperatureData = function() {
  handleData(`http://${lanIP}/1/progress`, showDataTemp);
};

const getConsumptionData = function(user) {
  handleData(`http://${lanIP}/4/${user}/progress`, showDataConsumption);
};

const getGoalData = function(user) {
    handleData(`http://${lanIP}/${user}/goals`, showGoals);
};  

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  html_total = document.querySelector('.js-total');
  html_average = document.querySelector('.js-average');
  listenToSocket();
  getTemperatureData();
});
