<script src="https://www.gstatic.com/firebasejs/9.6.3/firebase-app.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.6.3/firebase-auth.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.6.3/firebase-firestore.js"></script>

const firebaseConfig = {
    apiKey: "AIzaSyCOwA--4HISXFSdKZr-a6e3JY7_KKqJfVs",
    authDomain: "healthcare-project-7d629.firebaseapp.com",
    projectId: "healthcare-project-7d629",
    storageBucket: "healthcare-project-7d629.appspot.com",
    messagingSenderId: "444565501959",
    appId: "1:444565501959:web:392c3fd7f113f94442d2a2",
    measurementId: "G-1360NGENXT"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Firebase UI configuration
const uiConfig = {
    signInSuccessUrl: '/dashboard', // Redirect URL after sign-in success
    signInOptions: [
        firebase.auth.GoogleAuthProvider.PROVIDER_ID // Enable Google Sign-In
    ],
    tosUrl: '/terms-of-service', // Terms of service URL
    privacyPolicyUrl: '/privacy-policy' // Privacy policy URL
};

// Initialize the FirebaseUI Widget using Firebase
const ui = new firebaseui.auth.AuthUI(firebase.auth());

// Start the FirebaseUI sign-in flow
ui.start('#firebaseui-auth-container', uiConfig);

// Show a loading indicator while FirebaseUI loads
document.getElementById('loader').style.display = 'none';

// JavaScript for Search Form
document.getElementById('search-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent default form submission

    let medicineName = document.getElementById('medicine_name').value;
    fetch(`/search?medicine_name=${encodeURIComponent(medicineName)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            let resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '';

            if (data.error || data.message) {
                resultDiv.innerHTML = `<p class="text-red-500">${data.message || data.error}</p>`;
            } else {
                let html = '<ul class="list-disc pl-5">';
                data.organic_results.forEach(item => {
                    html += `<li class="mb-4"><a href="${item.link}" class="text-blue-500 hover:underline" target="_blank">${item.title}</a><p>${item.snippet}</p></li>`;
                });
                html += '</ul>';
                resultDiv.innerHTML = html;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            let resultDiv = document.getElementById('result');
            resultDiv.innerHTML = `<p class="text-red-500">An error occurred: ${error.message}</p>`;
        });
});
