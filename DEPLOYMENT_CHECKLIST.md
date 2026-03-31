# THE SWARM - Deployment Checklist

## Pre-Flight Check

- [ ] Anthropic API key ready
- [ ] Python 3.11+ installed
- [ ] Git installed (for GitHub deployment)
- [ ] GitHub account (for Codespaces/repo)
- [ ] Hugging Face account (for Space deployment, optional)

## Option 1: Browser Version (Fastest)

- [ ] Download `index.html`
- [ ] Serve locally: `python -m http.server 8000`
- [ ] Open `http://localhost:8000`
- [ ] Open browser console
- [ ] Paste input text
- [ ] Click "ACTIVATE SWARM"
- [ ] Export results

**Time:** 2 minutes  
**Difficulty:** ⭐☆☆☆☆

## Option 2: Local Gradio

- [ ] Extract repo: `tar -xzf the-swarm-repo.tar.gz`
- [ ] Navigate: `cd swarm-repo`
- [ ] Install: `pip install -r requirements.txt`
- [ ] Set API key: `export ANTHROPIC_API_KEY="..."`
- [ ] Run: `./start.sh` or `python app.py`
- [ ] Open `http://localhost:7860`
- [ ] Test with sample input

**Time:** 5 minutes  
**Difficulty:** ⭐⭐☆☆☆

## Option 3: GitHub Repository

### Create Repo
- [ ] Create new repo on GitHub
- [ ] Clone locally: `git clone https://github.com/you/the-swarm.git`
- [ ] Copy all files from `swarm-repo/` to your clone
- [ ] Commit: `git add . && git commit -m "Initial commit"`
- [ ] Push: `git push origin main`

### Verify
- [ ] README renders correctly
- [ ] Files are all present
- [ ] .gitignore working
- [ ] GitHub Actions badge shows

**Time:** 5 minutes  
**Difficulty:** ⭐⭐☆☆☆

## Option 4: GitHub Codespaces

**Prerequisites:** Repo on GitHub

- [ ] Go to your GitHub repo
- [ ] Click green "Code" button
- [ ] Select "Codespaces"
- [ ] Click "Create codespace on main"
- [ ] Wait for environment setup (~2 min)
- [ ] Open terminal in Codespaces
- [ ] Set API key: `export ANTHROPIC_API_KEY="..."`
- [ ] Run: `./start.sh`
- [ ] Click forwarded port URL
- [ ] Test application

**Time:** 5-7 minutes  
**Difficulty:** ⭐⭐☆☆☆

## Option 5: Hugging Face Space

### Method A: Create New Space
- [ ] Go to huggingface.co/spaces
- [ ] Click "Create new Space"
- [ ] Name it (e.g., "the-swarm")
- [ ] Choose Gradio SDK
- [ ] Create Space
- [ ] Upload files:
  - [ ] `app.py`
  - [ ] `requirements.txt`
  - [ ] `README_HUGGINGFACE.md` (rename to README.md)
- [ ] Go to Settings → Repository secrets
- [ ] Add `ANTHROPIC_API_KEY` secret
- [ ] Wait for build (~3-5 min)
- [ ] Test Space

**Time:** 10 minutes  
**Difficulty:** ⭐⭐⭐☆☆

### Method B: Link to GitHub
- [ ] Create Space on Hugging Face
- [ ] Link to your GitHub repo
- [ ] Add API key to secrets
- [ ] Auto-deploys from GitHub

**Time:** 5 minutes  
**Difficulty:** ⭐⭐☆☆☆

## CLI Tools Setup

- [ ] Make scripts executable: `chmod +x swarm_cli.py swarm_batch.py`
- [ ] Test CLI: `echo "test" | python swarm_cli.py`
- [ ] Test batch: `python swarm_batch.py ./test_docs ./outputs`
- [ ] Add to PATH (optional):
  ```bash
  echo 'export PATH="$PATH:$(pwd)"' >> ~/.bashrc
  source ~/.bashrc
  ```

**Time:** 2 minutes  
**Difficulty:** ⭐⭐☆☆☆

## Customization

### Add Custom Persona
- [ ] Open `app.py` and `index.html`
- [ ] Find `PERSONAS` dict
- [ ] Add new persona with template
- [ ] Test locally
- [ ] Commit changes

**Time:** 15-30 minutes  
**Difficulty:** ⭐⭐⭐☆☆

### Change Model
- [ ] Find model string: `claude-sonnet-4-20250514`
- [ ] Replace with:
  - `claude-opus-4-6` (best quality)
  - `claude-haiku-4-5-20251001` (fastest/cheapest)
- [ ] Test
- [ ] Commit

**Time:** 2 minutes  
**Difficulty:** ⭐☆☆☆☆

## Testing Checklist

### Functional Tests
- [ ] Browser version works
- [ ] Gradio interface works
- [ ] CLI processes file
- [ ] Batch processes multiple files
- [ ] All 8 personas run
- [ ] Exports generate correctly
- [ ] SCHEMA recommendations appear

### Content Tests
- [ ] Short input (~100 words)
- [ ] Long input (~5000 words)
- [ ] Technical content
- [ ] Creative content
- [ ] Research paper
- [ ] Meeting notes

### Export Tests
- [ ] TXT export downloads
- [ ] MD export downloads
- [ ] JSON export downloads
- [ ] YAML export downloads
- [ ] CSV export downloads

## Production Checklist

### Security
- [ ] API key in environment variable (not hardcoded)
- [ ] .env in .gitignore
- [ ] Secrets properly configured (HF/Codespaces)
- [ ] No sensitive data in repo

### Documentation
- [ ] README complete
- [ ] Setup guide clear
- [ ] Examples provided
- [ ] License included

### Performance
- [ ] Response times acceptable (<60s)
- [ ] No API errors
- [ ] Rate limits respected
- [ ] Costs within budget

### Maintenance
- [ ] GitHub Actions passing
- [ ] Dependencies up to date
- [ ] Issues template created
- [ ] Contributing guide present

## Rollback Plan

If something breaks:

1. **Browser version** - Revert to last working index.html
2. **Local** - `git checkout HEAD~1`
3. **GitHub** - Revert commit in GitHub UI
4. **Codespaces** - Rebuild container
5. **HF Space** - Revert to previous version

## Success Metrics

- [ ] All tests pass
- [ ] No errors in logs
- [ ] Users can process content
- [ ] Exports work
- [ ] Performance acceptable
- [ ] Costs reasonable

## Next Steps After Deployment

1. [ ] Create example outputs
2. [ ] Share with team/community
3. [ ] Gather feedback
4. [ ] Iterate on personas
5. [ ] Add integrations
6. [ ] Write blog post
7. [ ] Submit to showcases

## Support Resources

- **GitHub Issues** - Bug reports, feature requests
- **Discussions** - Questions, ideas
- **Documentation** - README, guides, architecture
- **Examples** - Sample inputs/outputs

## Common Gotchas

❌ **Forgot to set API key**  
✅ `export ANTHROPIC_API_KEY="..."`

❌ **CORS errors in browser**  
✅ Use local server, not file://

❌ **Port 7860 already in use**  
✅ `lsof -ti:7860 | xargs kill`

❌ **Rate limit errors**  
✅ Wait 60 seconds, use different key

❌ **Requirements not installed**  
✅ `pip install -r requirements.txt`

❌ **Can't find outputs**  
✅ Check current directory or specified path

---

## Ready to Deploy?

Pick your option above and follow the steps.  
Most people start with **Option 1 (Browser)** or **Option 2 (Local Gradio)**.

Questions? Check the docs or open an issue!

**Good luck! 🚀**
