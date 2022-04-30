const fs = require("fs");
const path = require("path");

const uuid = require("uuid");
const express = require("express");
const cookieParser = require("cookie-parser");
const multer = require("multer");

const LISTEN_PORT = 8080;

const storage = multer.diskStorage({
    destination: (req, file, callback) => {
        callback(null, "./uploads");
    },
    // Keep original file name
    filename: (req, file, callback) => {
        callback(null, file.originalname);
    }
});

const upload = multer({ storage });

const app = express();

app.use(cookieParser());

app.set("view engine", "ejs");

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use("/uploads", express.static(path.join(__dirname, "uploads")));

// Key : session id, value : username
const sessions = {};

function isEmpty(value) {
    return (typeof value === "undefined" || value.length === 0);
}

function waitSeconds(seconds) {
    return new Promise(resolve => setTimeout(resolve, seconds * 1000));
}

function retrieveSession(req) {
    const { cookies } = req;
    if (cookies && cookies.sessionid && sessions[cookies.sessionid]) {
        return sessions[cookies.sessionid];
    }
    return null;
}

app.get("/", (req, res) => {
    const user = retrieveSession(req);
    if (user === null) {
        return res.redirect("/login");
    }
    res.redirect("/dashboard");
})

app.get("/login", (req, res) => {
    res.render("login");
});

app.post("/login", (req, res) => {
    const { username, password } = req.body;
    
    if (isEmpty(username)) res.send("Missing username");
    if (isEmpty(password)) res.send("Missing password");

    const sessionId = uuid.v4();
    sessions[sessionId] = username;
    res.cookie("sessionid", sessionId);

    res.redirect("/dashboard");
});

app.get("/dashboard", (req, res) => {
    const user = retrieveSession(req);
    if (user === null) {
        return res.redirect("/login");
    }
    res.render("dashboard", {
        username: user,
        files: fs.readdirSync("uploads")
    });
});

app.post("/upload", upload.single("file"), (req, res) => {

    const { originalname } = req.file;

    res.render("upload_ok", {
        filename: originalname
    });
});

app.listen(LISTEN_PORT, () => {
    console.log(`App listening on port ${LISTEN_PORT}`);
});
