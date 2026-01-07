const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bodyParser = require('body-parser');
const { Appointment, Doctor, City } = require('./models');

const app = express();

app.use(cors());
app.use(bodyParser.json());

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/appointment_db', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function () {
    console.log('Connected to MongoDB');
});

// Routes

// Book appointment
app.post('/api/book-appointment', async (req, res) => {
    const { state, city, doctor, timeSlot } = req.body;
    if (!state || !city || !doctor || !timeSlot) {
        return res.status(400).json({ message: 'All fields are required.' });
    }

    const appointment = new Appointment({
        state,
        city,
        doctor,
        timeSlot
    });

    try {
        await appointment.save();
        res.json({ message: 'Appointment booked successfully!' });
    } catch (err) {
        res.status(500).json({ message: 'An error occurred while booking the appointment.' });
    }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
