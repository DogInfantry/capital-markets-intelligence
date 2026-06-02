# Deploying Capital Markets Intelligence Dashboard

## Option 1: Vercel Dashboard (Recommended — 2 minutes)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Click **"Add New Project"**
3. Import `DogInfantry/capital-markets-intelligence` from GitHub
4. Set **Root Directory** → `dashboard`
5. Framework: **Next.js** (auto-detected)
6. Click **Deploy** → done

## Option 2: GitHub Actions (Auto-deploy on every push)

Add these secrets to your GitHub repo (`Settings → Secrets → Actions`):

| Secret | Value |
|--------|-------|
| `VERCEL_TOKEN` | Personal access token from vercel.com/account/tokens |
| `VERCEL_ORG_ID` | `team_4pgfqRkIU2W9etJoOiEwg250` |
| `VERCEL_PROJECT_ID` | Project ID after first deploy |

The workflow `.github/workflows/deploy-dashboard.yml` runs automatically on push to `main`.

## Environment

No environment variables required. All data is served from `/public/data/` at build time.
