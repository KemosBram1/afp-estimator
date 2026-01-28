# afp-estimator
Quote Estimator

## Getting Started

### Setting Up GitHub Authentication

To interact with this repository securely, you can set up SSH authentication with GitHub.

See [SSH_SETUP.md](SSH_SETUP.md) for detailed instructions on generating and configuring SSH keys.

**Quick commands to set up SSH key:**
```bash
# 1. Generate SSH key
ssh-keygen -t ed25519 -C "bkemoli@associatedfire.net"

# 2. Start SSH agent
eval "$(ssh-agent -s)"

# 3. Add key to SSH agent
ssh-add ~/.ssh/id_ed25519

# 4. Copy public key (macOS)
pbcopy < ~/.ssh/id_ed25519.pub

# 5. After adding the key to GitHub, configure repository to use SSH
git remote set-url origin git@github.com:KemosBram1/afp-estimator.git
git push origin main
```

> **Note:** Replace the email address with your own when running these commands. For Linux/Windows clipboard commands, see the full guide.
