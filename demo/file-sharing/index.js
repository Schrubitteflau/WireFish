const fs = require("fs");
const path = require("path");

const express = require("express");
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

app.set("view engine", "ejs");

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use("/uploads", express.static(path.join(__dirname, "uploads")));

let currentUser = null;

function isEmpty(value)
{
    return (typeof value === "undefined" || value.length === 0);
}

function waitSeconds(seconds)
{
    return new Promise(resolve => setTimeout(resolve, seconds * 1000));
}

app.get("/login", (req, res) => {
    res.render("login");
});

app.post("/login", (req, res) => {
    const { username, password } = req.body;
    
    if (isEmpty(username)) res.send("Missing username");
    if (isEmpty(password)) res.send("Missing password");

    currentUser = username;

    res.redirect("/dashboard");
});

app.get("/dashboard", (req, res) => {
    res.render("dashboard", {
        username: currentUser,
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
