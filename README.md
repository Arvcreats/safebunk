# SafeBunk v2 🎓
Attendance planner: Today screen, undo + history, semester projection, leave planner, login + cloud sync (Firebase), daily notification, admin user list + Excel export, share, APK.

App icon/logo: `assets/logo.png` (web icons `www/icon-192.png` / `www/icon-512.png` isi se bane hain).

## 1. Login chalu karna (Firebase, free) — sirf owner ko karna hai
1. console.firebase.google.com -> **Add project** (apne Google account se)
2. Build -> Authentication -> Get started -> **Email/Password** enable
3. Build -> Firestore Database -> Create database (production mode). Phir **Rules** tab me ye POORA text paste karo:
   ```
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       // Har user ka apna attendance data — sirf wahi padh/likh sakta hai
       match /users/{uid} {
         allow read, write: if request.auth != null && request.auth.uid == uid;
       }
       // Login record (email, kab login kiya, kitni baar) — user khud likhta hai,
       // list sirf admin (owner) dekh sakta hai
       match /profiles/{uid} {
         allow create, update: if request.auth != null && request.auth.uid == uid;
         allow read: if request.auth != null && request.auth.uid == uid;
         allow list, get: if request.auth != null && request.auth.token.email == "atharvpatel2008@gmail.com";
       }
     }
   }
   ```
   Note: admin email `www/index.html` ke `ADMIN_EMAIL` se match hona chahiye.
4. Project settings -> Your apps -> Web (`</>`) -> app register karo -> **firebaseConfig** copy karke `www/firebase-config.js` me paste karo.
5. Config bhar ke dobara push karoge to login + sync + admin sab chalu. Khali chhodoge to app **guest mode** me chalega (login band, baaki sab on).

**Password ke baare me:** passwords Firebase secure rakhta hai — owner ko bhi kabhi nahi dikhte.
Owner ko sirf ye dikhta hai: user ka **email, join date, last login time, kul kitni baar login kiya**.

## 2. Admin — kaun use kar raha hai + Excel
- Owner apne admin email se app me login kare -> **Settings** me "👑 Admin — users" card aayega.
- **Users load karo** = saare users ki list (email, last login, login count).
- **⬇ Excel download** = wahi list Excel me khulne wali CSV file me. Jab chaaho, app se hi download kar lo — data Firestore me live rehta hai.

## 3. GitHub pe daalo
```
git init && git add . && git commit -m "SafeBunk v2"
git branch -M main
git remote add origin https://github.com/<username>/safebunk.git
git push -u origin main
```

## 4. APK download
Push ke baad GitHub -> **Actions** -> "Build APK" -> run complete hone par **Artifacts -> SafeBunk-APK** download karo, phone me install karo (Unknown sources allow).
Build ke time workflow `assets/logo.png` se APK ka launcher icon banane ki koshish karta hai (step fail ho jaye to bhi APK ban jayega, default icon ke saath).

## Notes
- Notification: APK me Settings -> Daily reminder (Android 13+ me permission allow karna).
- Login ke bina bhi app chalta hai (guest mode). Offline: app shell cache hota hai.
- Share: Settings -> "App share karo" (WhatsApp/share sheet).
- Debug APK hai; Play Store ke liye signed release build alag banana hoga.
- Sab kuch free tier par hai: Firebase Spark (free), GitHub Actions (public repo free), koi server nahi.
