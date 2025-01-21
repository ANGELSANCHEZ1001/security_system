const mongoose = require('mongoose');
const fs = require('fs'); // Módulo para trabajar con el sistema de archivos
const path = require('path'); // Módulo para manejar rutas
const Image = require('./functions/models/image.js');

mongoose.connect('mongodb://localhost:27017/imageDB', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

const seedImages = async () => {
    try {
        // Lee los archivos del directorio y conviértelos a base64
        const images = [
            {
                title: 'Ladron 3',
                url: `data:image/jpeg;base64,${fs.readFileSync(path.join(__dirname, 'foto.jpg')).toString('base64')}`,
                path: path.join(__dirname, 'foto.jpg'),
                key: '14012025',
            },
            {
                title: 'Ladron 4',
                url: `data:image/jpeg;base64,${fs.readFileSync(path.join(__dirname, 'foto2.jpg')).toString('base64')}`,
                path: path.join(__dirname, 'foto2.jpg'),
                key: '13012025',
                
            },
        ];

        // Inserta las imágenes en la base de datos
        await Image.insertMany(images);
        console.log('Imágenes agregadas');
    } catch (error) {
        console.error('Error al agregar las imágenes:', error);
    } finally {
        mongoose.connection.close();
    }
};

seedImages();
