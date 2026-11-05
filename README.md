# SafeBunk v2.3 🎓

**SafeBunk is an attendance planner for college students.** It answers one question in seconds: *"Can I safely bunk today's class, or will my attendance drop below the target?"* It tracks every subject, shows recovery and safe-bunk numbers, plans leaves in advance, and — from v2.2 — understands your uploaded timetable.

> **v2.3 fix:** a startup order bug made the app open but nothing was clickable. Fixed and verified with a full simulated user-flow test (all tabs, timetable add, attend marking).

---

## ✨ Features

- **Today screen** — one clear answer every morning: "Safe to bunk today" or "Don't bunk today", plus today's classes with Attend / Bunk buttons.
- **Subjects** — per-subject attendance %, overall %, weakest subject highlighted, last-10-classes history dots, undo.
- **Recovery calculator** — how many classes you must attend in a row to get back to your target.
- **Safe-bunk counter** — how many classes you can still miss without dropping below target.
- **Semester projection** — if your semester end date and class days are set, the app projects to the end of the semester and honestly warns you if the target has become impossible (so you can talk to your college about condonation/medical options in time).
- **Leave Planner** — pick leave dates and see, per subject, how many classes you will miss and what your % will become.
- **Timetable (Table tab)** — upload your timetable once (see below) and the Today screen shows today's classes in time order.
- **Target setting** — 60 / 65 / 70 / 75 / 80%, with an option to count 74.5% as 75% (rounding), if your college rounds that way.
- **Login + cloud sync (optional)** — sign up / log in with email and password; your data syncs via Firebase. Without login the app works fully in guest mode on the device.
- **Daily reminder** — a notification at your chosen time to mark attendance.
- **Backup** — copy/paste export-import of your data, plus share options.
- **Share** — send the app to friends from Settings.
- **Everything is free** — static app, Firebase free (Spark) plan, GitHub Actions free for public repos. No server, no cost.

## 🗓️ Timetable (v2.2)

Open the **Table** tab and add your timetable in any of three ways:

- **Photo upload** — upload a photo of your timetable. The photo is saved inside the app and read with OCR (Tesseract.js, free; needs internet once). Detected subjects and start/end times appear on a **confirm screen** where you can fix anything before saving.
- **CSV upload** — the most reliable route. Format: `Day,Subject,Start,End,Room` — e.g. `Mon, Accounts, 09:00, 09:50, R-12`.
- **Manual add** — pick the day, subject, start time, end time and room. A new subject name automatically creates the subject and sets its class days.

Once the timetable is saved, the **Today** screen lists today's classes in time order with each lecture's duration (e.g. `09:00 – 09:50 · 50 min`), the day's total classes and total hours, and Attend/Bunk buttons for every class. The weekly Table view shows per-day totals too.

App icon/logo: `assets/logo.png` (the web icons `www/icon-192.png` and `www/icon-512.png` are generated from it).

---

## 👑 Who is the "Owner"? (Admin — please read)

**"Owner" means the creator and admin of this app — Atharv Patel.** The owner's admin email is `atharvpatel2008@gmail.com` (set as `ADMIN_EMAIL` in `www/index.html` and in the Firestore rules below). There is exactly **one** owner account. Everyone else is a normal user.

### What the owner CAN see

When the owner logs in to the app with the admin email, a special **"👑 Admin — users"** card appears in **Settings** (no other user ever sees this card). From there the owner can:

- **See who is using the app** — the full list of signed-up users.
- For every user, see exactly three things:
  1. **Email address** (the one they signed up with)
  2. **Join date** (when they first logged in) and **last login time** (when they last opened/logged in to the app)
  3. **Total login count** (how many times they have logged in)
- **Download the same list as an Excel file** — tap **"⬇ Excel download"** and a CSV file (`safebunk-users.csv`) is saved, which opens directly in Excel/Google Sheets. The data lives live in Firestore, so the list is always up to date — just open the app and download whenever you want.

This exists so the owner can know how many people are actually using the app and whether they are active — the same basic analytics every app owner has.

### What the owner can NEVER see

- **Passwords.** Passwords are stored by Firebase in secure hashed form. They are not visible to the owner, to any user, or to anyone else — not in the app, not in Firebase, not in the Excel sheet. This is by design and cannot be changed.
- **Any user's attendance data.** Every user's subjects, attendance and timetable are stored under their own private account (`users/{uid}`), and the Firestore rules below allow **only that user** to read or write it. The admin panel shows login information only — never anyone's attendance.

### For normal users (privacy in one paragraph)

If you create an account, the app stores: your email, your join/last-login times and login count (so the owner can see app usage, as explained above), and your own attendance data, synced privately to your account so you don't lose it. Nothing else is collected. There are no ads and no trackers. If you never log in, everything stays only on your device (guest mode).

### Who can change this app and this code?

This is a public repository: anyone can **view** the code and **suggest** changes (open a GitHub Issue). Only the **owner** can edit the code, approve changes and publish new versions. The app is a living project and is updated from time to time.

---

## 1. Enable login (Firebase, free) — owner does this once

1. Go to console.firebase.google.com → **Add project** (with the owner's Google account).
2. Build → Authentication → Get started → enable **Email/Password**.
3. Build → Firestore Database → Create database (production mode). Then in the **Rules** tab, paste this ENTIRE text:
   ```
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       // Each user's own attendance data — only that user can read/write it
       match /users/{uid} {
         allow read, write: if request.auth != null && request.auth.uid == uid;
       }
       // Login record (email, last login, login count) — the user writes their own,
       // and only the admin (owner) can list/read all profiles
       match /profiles/{uid} {
         allow create, update: if request.auth != null && request.auth.uid == uid;
         allow read: if request.auth != null && request.auth.uid == uid;
         allow list, get: if request.auth != null && request.auth.token.email == "atharvpatel2008@gmail.com";
       }
     }
   }
   ```
   Note: the admin email here must match `ADMIN_EMAIL` in `www/index.html`.
4. Project settings → Your apps → Web (`</>`) → register the app → copy the **firebaseConfig** and paste it into `www/firebase-config.js`.
5. Push again with the config filled in — login, sync and the admin panel all switch on. If the config is left empty, the app simply runs in **guest mode** (no login, everything else works).

## 2. Admin — see users + Excel (owner only)

- Log in to the app with the owner/admin email → open **Settings** → the **"👑 Admin — users"** card appears.
- **Users load karo / Load users** = the full user list (email, last login, login count, join date).
- **⬇ Excel download** = the same list as a CSV file that opens in Excel. Simple version: the owner can see **who logged in, when they logged in, and how many times** — and download it as a sheet any time. (Full explanation: the **Owner** section above.)

## 3. Put it on GitHub

```
git init && git add . && git commit -m "SafeBunk v2"
git branch -M main
git remote add origin https://github.com/<username>/safebunk.git
git push -u origin main
```

## 4. Download the APK

After pushing, go to GitHub → **Actions** → "Build APK" → when the run finishes, download **Artifacts → SafeBunk-APK** and install it on the phone (allow "Install unknown apps" if Android asks).
During the build, the workflow tries to generate the APK launcher icon from `assets/logo.png` (even if that one step fails, the APK still builds, with a default icon).

## Notes

- **Notifications:** in the APK, set your time in Settings → Daily reminder (on Android 13+, allow the notification permission).
- **Offline:** the app shell is cached, so the app opens offline; OCR and login/sync need internet.
- **Share:** Settings → "Share SafeBunk" (WhatsApp / share sheet).
- This is a debug APK; a signed release build would be made separately for the Play Store.
- Total running cost: **₹0** — Firebase Spark (free), GitHub Actions (free for public repos), no server.
