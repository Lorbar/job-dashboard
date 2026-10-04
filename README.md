# Job Command Center
Static site (no build). Light off-white / dark / auto themes, mobile-friendly.

## Host it on GitHub Pages
1. github.com → **New repository** → name `job-dashboard`. Choose **Public** (free Pages). Don't add a README. Create.
2. Optional privacy: delete the `resumes/` folder first (it holds your phone/email). The dashboard works without it; keep resumes in Drive instead.
3. Terminal, in this folder:  `chmod +x deploy.sh && ./deploy.sh https://github.com/<you>/job-dashboard.git`
   (sign in when Git asks — use a Personal Access Token as the password, or `gh auth login`.)
4. Repo → **Settings → Pages** → Source: *Deploy from a branch* → `main` / `(root)` → Save.
5. Repo → **Settings → Actions → General** → Workflow permissions → **Read and write** → Save.
6. Repo → **Actions** tab → *Daily job link check* → **Run workflow**. It then runs daily by itself and commits `status.json`.
7. Open `https://<you>.github.io/job-dashboard/` (1–2 min after first deploy). On your phone: Share → *Add to Home Screen*.

## How updates work
- **GitHub Action (hands-off, daily):** checks each posting URL and writes `status.json` (✅ live / ❌ closed / ❔ can't tell for JS-only sites).
- **Claude daily task (deeper):** opens pages in a browser, finds new roles, edits local `status.json`, drafts an email digest. Publish its changes with `./deploy.sh`.
- Your own statuses/notes stay in your browser (Tools → Export to move devices).
