// Connect to the socket
var socket = io("http://127.0.0.1:5002", {
  withCredentials: true,
  transports: ["polling"],
  extraHeaders: {
    "Access-Control-Allow-Origin": "*",
  },
  forceNew: true,
  allowEIO3: true,
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
    allowedHeaders: ["*"],
    credentials: true,
  },
});
socket.on("connect", function () {
  console.log("Connected to server");
});
socket.on("disconnect", function () {
  console.log("Disconnected from server");
  // displayError({ message: "インターネット接続を確認してください。" });
});
socket.on("progress", function (data) {
  var activeTab = document.querySelector(".tab-content.active");
  activeTab.querySelector(".progress").style.width = data.progress + "%";
  activeTab.querySelector(".progress-text").innerText =
    Math.round(data.progress) + "%";
});
socket.on("text", function (data) {
  var activeTab = document.querySelector(".tab-content.active");
  activeTab.querySelector("#text").innerText = data.text;
});
