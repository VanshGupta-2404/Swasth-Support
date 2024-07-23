const mongoose = require('mongoose');

// Define the Appointment Schema and Model
const appointmentSchema = new mongoose.Schema({
    state: { type: String, required: true },
    city: { type: String, required: true },
    doctor: { type: String, required: true },
    timeSlot: { type: String, required: true },
});

const Appointment = mongoose.model('Appointment', appointmentSchema);

// Define the Doctor Schema and Model
const doctorSchema = new mongoose.Schema({
    city: { type: String, required: true },
    name: { type: String, required: true },
    specialty: { type: String, required: true },
});

const Doctor = mongoose.model('Doctor', doctorSchema);

// Define the City Schema and Model
const citySchema = new mongoose.Schema({
    state: { type: String, required: true },
    name: { type: String, required: true },
});

const City = mongoose.model('City', citySchema);

module.exports = {
    Appointment,
    Doctor,
    City
};
