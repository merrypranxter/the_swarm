# Contributing to THE SWARM

Thanks for considering contributing! THE SWARM thrives on community additions and improvements.

## Ways to Contribute

### 1. Add New Personas
The easiest and most valuable contribution!

**What makes a good persona:**
- Distinct cognitive mode (not overlapping with existing 8)
- Clear specialty/expertise
- Unique voice/style
- Specific output format

**How to add:**
1. Fork the repo
2. Edit `app.py` and `index.html`
3. Add your persona to `PERSONAS` dict
4. Choose `frontLine` (parallel) or `hiddenLayer` (sequential)
5. Test thoroughly
6. Submit PR with examples

**Template:**
```python
{
    "id": "yourpersona",
    "name": "🔶 YOURNAME",
    "role": "Your Role Description",
    "color": "#ff6600",
    "icon": "🔶",
    "prompt": """You are YOURNAME, the [specialty]. 
    
    Your voice: [description]
    
    Your job: [task description]
    
    Format: [output format]"""
}
```

### 2. Improve Existing Personas
Persona prompts can always be refined!

**Good improvements:**
- Clearer instructions
- Better examples
- More consistent output format
- Reduced verbosity
- Enhanced specialty focus

**How to improve:**
1. Test current persona
2. Identify specific issues
3. Propose prompt changes
4. Include before/after examples
5. Submit PR

### 3. Add Examples
Real-world examples help others understand the tool.

**What to include:**
- Input text (paste or file)
- Full JSON output
- What made it interesting
- Use case description

**How to contribute:**
1. Run Swarm on interesting content
2. Export JSON
3. Add to `examples/` folder
4. Document in `examples/EXAMPLES.md`
5. Submit PR

### 4. Build Integrations
Connect Swarm to other tools!

**Integration ideas:**
- Obsidian plugin
- VS Code extension
- Raycast script
- Alfred workflow
- Browser extension
- Discord bot
- Slack app
- API wrapper

**How to share:**
1. Build your integration
2. Document setup
3. Add to `integrations/` folder
4. Link from main README
5. Submit PR

### 5. Improve Documentation
Clear docs help everyone.

**Docs to enhance:**
- README.md - main overview
- SETUP_GUIDE.md - deployment steps
- ARCHITECTURE.md - technical details
- EXAMPLES.md - use cases

**How to improve:**
- Fix typos/errors
- Add missing info
- Clarify confusing parts
- Add diagrams
- Submit PR

### 6. Report Bugs
Found an issue? Let us know!

**Good bug reports include:**
- What you did
- What happened
- What you expected
- Version info
- Error messages
- Minimal reproduction

**How to report:**
1. Check existing issues
2. Create new issue
3. Use bug template
4. Provide details

### 7. Request Features
Ideas welcome!

**Good feature requests:**
- Clear use case
- Why it's valuable
- How it might work
- Mockups/examples

**How to request:**
1. Open issue
2. Use feature template
3. Discuss approach
4. (Optional) Implement yourself!

## Development Setup

### Local Development
```bash
# Clone your fork
git clone https://github.com/yourusername/the-swarm.git
cd the-swarm

# Create branch
git checkout -b feature/your-feature

# Install deps
pip install -r requirements.txt

# Make changes
# ... edit files ...

# Test
python app.py  # Gradio
python swarm_cli.py test_input.txt  # CLI

# Commit
git add .
git commit -m "Description of changes"
git push origin feature/your-feature
```

### Codespaces Development
1. Fork repo
2. Open in Codespaces
3. Make changes
4. Test
5. Commit & push
6. Create PR

## Code Style

### Python
- Follow PEP 8
- Use f-strings for formatting
- Add docstrings to functions
- Keep functions focused
- Comment non-obvious code

### JavaScript
- Use const/let (not var)
- Camelcase for variables
- Clear function names
- Comment complex logic

### Prompts
- Clear instructions
- Specific examples
- Defined output format
- Consistent voice

## Testing

### Manual Testing Checklist
- [ ] Browser version works
- [ ] Gradio version works
- [ ] CLI version works
- [ ] Batch processing works
- [ ] Exports generate correctly
- [ ] No API errors
- [ ] Output quality good

### Test Cases to Try
1. Short input (~100 words)
2. Long input (~5000 words)
3. Technical content
4. Creative content
5. Research/academic
6. Conversational text

## Pull Request Process

1. **Fork & branch**
   - Fork the repo
   - Create feature branch

2. **Make changes**
   - Follow code style
   - Test thoroughly
   - Update docs

3. **Commit**
   - Clear commit messages
   - Atomic commits
   - Reference issues

4. **Submit PR**
   - Describe changes
   - Link related issues
   - Show examples
   - Request review

5. **Address feedback**
   - Respond to comments
   - Make requested changes
   - Update PR

6. **Merge**
   - Maintainer reviews
   - CI passes
   - Merge to main

## Persona Design Guidelines

### Good Persona Characteristics

**Distinct specialty:** Each persona should have a unique cognitive mode that doesn't overlap significantly with others.

**Clear voice:** The persona should have a recognizable style (surfer-philosopher, chaos goblin, database designer, etc.)

**Specific output:** The format should be consistent and well-defined (themes, entity maps, file structures, etc.)

**Additive value:** The persona should provide insights the others don't, not just rephrase.

### Persona Testing

When proposing a new persona:

1. **Run it on 5+ different inputs**
   - Technical docs
   - Creative writing
   - Research papers
   - Meeting notes
   - Philosophical text

2. **Compare to existing personas**
   - Does it overlap significantly?
   - Does it add unique value?
   - Is the output distinct?

3. **Check consistency**
   - Does it maintain voice?
   - Is output format stable?
   - Does it stay on-task?

## Community

### Communication
- GitHub Issues - bugs, features
- Discussions - questions, ideas
- PRs - code contributions

### Code of Conduct
- Be respectful
- Be constructive
- Be inclusive
- Help others
- Have fun!

## Recognition

Contributors get:
- Credit in README
- Attribution in commits
- Karma points ✨
- Our eternal gratitude 🙏

## Questions?

Not sure about something?
- Open a discussion
- Ask in an issue
- Tag maintainers

We're here to help!

---

**Ready to contribute?** Pick an area above and dive in. Even small improvements make a difference!
