let selectedField = '';

function openModal(field) {
    selectedField = field;
    document.getElementById('field-name').innerText = "Booking for " + field;
    document.getElementById('bookingModal').style.display = "flex";
}

function closeModal() {
    document.getElementById('bookingModal').style.display = "none";
    selectedField = '';
}

function confirmBooking() {
    const timeSlot = document.getElementById('time-slot').value;
    if (timeSlot === '') {
        alert("Please select a time slot.");
        return;
    }

    alert(`Booking confirmed for ${selectedField} at ${timeSlot}`);

    // Redirect back to home
    window.location.href = "/";
}
