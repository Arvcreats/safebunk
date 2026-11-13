# Firestore Rules — Reference (SafeBunk)

**Status (13 Nov 2026):** The live Firestore rules were set to strict owner-only access and live-tested on 6 Nov 2026. However, the exact rules text lives only in the Firebase Console — it was not stored in this project until now, which was a verification gap found in the 13 Nov 2026 security audit.

**⚠️ Do NOT deploy the sketch below blindly.** It is a reconstruction of the *design* from the project record, not a copy of the live text. To complete this item properly: Firebase Console → Firestore Database → Rules → copy the exact live text and replace this file's sketch with it (2-minute job, Atharv only — console access is his).

## Design (as recorded)
- `users/{uid}` — a signed-in user can read/write **only their own** document (`request.auth.uid == uid`).
- `profiles/{uid}` — a user can read/write only their own profile; the **admin account only** (Atharv's email) can list/get all profiles (this powers the in-app admin card + the users list).
- Everything else: denied by default.
- Passwords are never stored in Firestore (Firebase Auth handles them).

## Sketch (for shape only — verify against the console before any use)
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{uid} {
      allow read, write: if request.auth != null && request.auth.uid == uid;
    }
    match /profiles/{uid} {
      allow read, write: if request.auth != null && request.auth.uid == uid;
      // + admin-only list/get for the owner's email — exact form: see live console text
    }
  }
}
```
