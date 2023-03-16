const express = require("express");
const cors = require("cors");
const http = require("http");
const bodyParser = require("body-parser");
const path = require("path");

const port = 8000;

app = express();

const server = http.createServer(app).listen(port, ()=>{});

app.use(cors());

app.use(express.static(path.join(__dirname, "client")));

app.use(bodyParser.json());

app.post("/server", (req, res) => {
    io.emit("command", req.body);
    console.log(req.body);
    res.status(201).json({ status: "reached" });
});

const io = require("socket.io")(server);

io.on("connection", (socket) => {
    socket.on("command", (data) => {
        io.emit("command", data);
    });
});
