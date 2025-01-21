const mongoose = require('mongoose');

const imageSchema = new mongoose.Schema({
    title: { type: String, required: true },
    url: { type: String, required: true },
});

const Image = mongoose.model('Image', imageSchema);

module.exports = Image;