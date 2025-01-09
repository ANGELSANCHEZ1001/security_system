const functions = require("firebase-functions");
const express = require("express");
const path = require("path");

const app = express();

// Ruta principal
app.get("/home", (req, res) => {
    res.sendFile(path.join(__dirname, "../INICIO/home.html"));
});

// Ruta API
app.get("/ditto", (req, res) => {
    res.json(require("./ditto.json")); // Asegúrate de que ditto.json esté aquí.
});

// Manejo de rutas no encontradas
app.use((req, res) => {
    res.status(404).send("Página no encontrada");
});

exports.api = functions.https.onRequest(app);
