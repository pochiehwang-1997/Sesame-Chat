const express = require("express");
const cors = require("cors");
const http = require("http");
const bodyParser = require("body-parser");
const path = require("path");
const Server = require("socket.io");

const port = 9000;

app = express();

const server = http.createServer(app).listen(port, () => {});

app.use(express.static(path.join(__dirname, "client")));

app.use(bodyParser.json());

app.post("/server", (req, res) => {
  io.emit("command", req.body);
  res.status(201).json({ status: "reached" });
});

const io = new Server.Server(server, {
  cors: {
    origin: "*",
  },
});

io.on("connection", (socket) => {
  socket.on("command", (data) => {
    io.emit("command", data);
  });
});
