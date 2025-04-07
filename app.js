// 👉 Replace this with your Firebase config
const firebaseConfig = {
    apiKey: "AIzaSyCO_4Jsk5SnrfyKQWZnmBtVklSadCs9pg8",
    authDomain: "cyber-44b22.firebaseapp.com",
    projectId: "cyber-44b22",
    storageBucket: "cyber-44b22.firebasestorage.app",
    messagingSenderId: "248146736668",
    appId: "1:248146736668:web:3b202009e00dcefed8d1d9",
    measurementId: "G-987YVFK1Q2"
  };
  
  
  firebase.initializeApp(firebaseConfig);
  const auth = firebase.auth();
  
  // LOGIN
  function login() {
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;
    auth.signInWithEmailAndPassword(email, password)
      .then(() => window.location.href = "home.html")
      .catch(err => alert(err.message));
  }
  
  // SIGNUP
  function signup() {
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;
    auth.createUserWithEmailAndPassword(email, password)
      .then(() => window.location.href = "home.html")
      .catch(err => alert(err.message));
  }
  
  // GOOGLE LOGIN
  function googleLogin() {
    const provider = new firebase.auth.GoogleAuthProvider();
    auth.signInWithPopup(provider)
      .then(() => window.location.href = "home.html")
      .catch(err => alert(err.message));
  }
  
  // LOGOUT
  function logout() {
    auth.signOut().then(() => window.location.href = "index.html");
  }
  
  // SHOW USER ON HOME PAGE
  firebase.auth().onAuthStateChanged(user => {
    if (user && document.getElementById("userEmail")) {
      document.getElementById("userEmail").innerText = `Logged in as: ${user.email}`;
    }
  });
  