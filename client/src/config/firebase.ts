import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyDS-JOtJQs1pGjWNWWfs0gSAAKCOR5XVyg",
  authDomain: "traffic-signal-controlle-2206a.firebaseapp.com",
  projectId: "traffic-signal-controlle-2206a",
  storageBucket: "traffic-signal-controlle-2206a.firebasestorage.app",
  messagingSenderId: "524610994605",
  appId: "1:524610994605:web:ca1e1ca25f3a6b8534e124",
  measurementId: "G-2BTM3DM0EP"
};

export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();