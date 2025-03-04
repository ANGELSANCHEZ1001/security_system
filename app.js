const express = require('express');
const cors = require('cors');
const app = express();
const path = require('path');
const mongoose = require("mongoose");
const Image = require('./models/image.js');

mongoose.connect('mongodb://localhost:27017/imageDB', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
}).then(() => {
    console.log("✅ Conectado a MongoDB");
}).catch((err) => {
    console.error("❌ Error conectando a MongoDB:", err);
});

app.use(cors());
app.use(express.json()); // Necesario para procesar JSON en POST
app.use(express.static(path.join(__dirname, './web')));

// Rutas de las páginas HTML
app.get('/ventana', (req, res) => res.sendFile(path.join(__dirname, './web/home.html')));
app.get('/historico', (req, res) => res.sendFile(path.join(__dirname, './web/historico.html')));
app.get('/fotos', (req, res) => res.sendFile(path.join(__dirname, './web/fotos.html')));
app.get('/fotos/:key', (req, res) => res.redirect(`/fotos.html?key=${req.params.key}`));

// Rutas de imágenes en MongoDB
app.get('/images', async (req, res) => {
    try {
        const images = await Image.find();
        res.json(images);
    } catch (error) {
        console.error('❌ Error al obtener imágenes:', error);
        res.status(500).json({ error: 'Error al obtener imágenes' });
    }
});

app.get('/images/:key', async (req, res) => {
    try {
        const images = await Image.find({ key: req.params.key });
        res.json(images);
    } catch (error) {
        console.error('❌ Error al obtener imágenes:', error);
        res.status(500).json({ error: 'Error al obtener imágenes' });
    }
});

// Ruta para agregar una nueva imagen
app.post('/images', async (req, res) => {
    const { title, url, key } = req.body;
    if (!title || !url || !key) {
        return res.status(400).json({ error: 'Faltan datos requeridos' });
    }
    try {
        const newImage = new Image({ title, url, key });
        await newImage.save();
        res.status(201).json({ message: 'Imagen agregada correctamente' });
    } catch (error) {
        console.error('❌ Error al agregar la imagen:', error);
        res.status(500).json({ error: 'Error al agregar la imagen' });
    }
});

const port = 4321;
app.listen(port, () => console.log(`🚀 Servidor en http://localhost:${port}`));