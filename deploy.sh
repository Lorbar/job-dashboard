#!/bin/bash
# First time:  ./deploy.sh https://github.com/<you>/job-dashboard.git
# Later:       ./deploy.sh   (publishes Claude's latest status.json / edits)
set -e
[ -d .git ] || git init -q
git add -A; git commit -qm "Update dashboard" || true
git branch -M main
if [ -n "$1" ]; then git remote remove origin 2>/dev/null || true; git remote add origin "$1"; fi
git pull --rebase -X theirs origin main 2>/dev/null || true
git push -u origin main
