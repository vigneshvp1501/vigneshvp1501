# Setup guide: vigneshvp1501

## 1. Create the profile repository
Create a **public** repository named exactly `vigneshvp1501` on GitHub. If it already exists, do not create it again.

## 2. Clone it using Windows PowerShell
Open VS Code → Terminal → New Terminal. Run:

```powershell
git --version
cd $HOME\Documents
New-Item -ItemType Directory -Force -Path GitHub | Out-Null
cd GitHub
git clone https://github.com/vigneshvp1501/vigneshvp1501.git
cd vigneshvp1501
```

If you already cloned it, just enter the existing folder:
```powershell
cd $HOME\Documents\GitHub\vigneshvp1501
```

## 3. Copy the ZIP contents
Extract this ZIP and copy all its contents into the cloned `vigneshvp1501` folder. Keep `.github\workflows\update-profile-art.yml` in place.

## 4. Install Python packages for local portrait generation
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r scripts/requirements.txt
```

## 5. Create the portrait and info card
Put a photo in the repository root named `source-photo.jpg`, then run:
```powershell
python scripts/prep_photo.py source-photo.jpg
python scripts/make_ascii_svg.py
python scripts/make_info_card.py
```

## 6. Generate the heatmap locally (optional)
```powershell
$env:GITHUB_USERNAME = "vigneshvp1501"
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
```

## 7. Commit and push
```powershell
git add .
git commit -m "Add animated GitHub profile art"
git branch -M main
git push -u origin main
```
If you created a README directly on GitHub and Git reports remote changes, run `git pull --rebase origin main`, resolve any conflicts if prompted, then push.

## 8. Run the daily workflow
On GitHub, open repository `vigneshvp1501` → **Actions**. Enable workflows if prompted, choose **Update profile art**, and click **Run workflow**.

## Notes
- The daily workflow updates only the contribution heatmap. Portrait and info-card SVGs are generated locally.
- GitHub may change its contribution-page HTML or rate-limit scraping. If the workflow fails, inspect the Actions log.
- The displayed total is the total parsed from the returned calendar, not a guaranteed lifetime total.
