# SSH Key Setup for GitHub

This guide will help you set up SSH authentication for GitHub, allowing you to interact with repositories securely without needing to enter your password each time.

## Prerequisites

- Git installed on your system
- A GitHub account

## Step 1: Generate SSH Key

Open your terminal and run the following command to generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "bkemoli@associatedfire.net"
```

> **Note:** Replace `bkemoli@associatedfire.net` with your own email address.

**What this command does:**
- `-t ed25519`: Specifies the type of key to create (Ed25519 algorithm, which is more secure and performant)
- `-C "your-email@example.com"`: Adds a label to the key with your email address

**During key generation:**
1. You'll be prompted to enter a file location to save the key. Press Enter to accept the default location (`~/.ssh/id_ed25519`)
2. You'll be asked to enter a passphrase. You can either:
   - Enter a secure passphrase (recommended for additional security)
   - Press Enter twice to skip the passphrase (less secure but more convenient)

## Step 2: Start the SSH Agent

Start the SSH agent in the background:

```bash
eval "$(ssh-agent -s)"
```

This should output something like `Agent pid 12345`.

## Step 3: Add SSH Key to SSH Agent

Add your SSH private key to the ssh-agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

## Step 4: Copy Your Public SSH Key

Copy your public SSH key to your clipboard. Choose the appropriate command for your operating system:

**macOS:**
```bash
pbcopy < ~/.ssh/id_ed25519.pub
```

**Linux (requires xclip):**
```bash
# Install xclip if needed (choose based on your distribution)
# Debian/Ubuntu:
sudo apt-get install xclip
# Fedora:
# sudo dnf install xclip
# Arch:
# sudo pacman -S xclip

# Copy the key
xclip -selection clipboard < ~/.ssh/id_ed25519.pub
```

**Windows (Git Bash):**
```bash
clip < ~/.ssh/id_ed25519.pub
```

**Alternative (all platforms):**
```bash
cat ~/.ssh/id_ed25519.pub
```

If using `cat`, the output will look something like:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJl3dIeudNqd0PZMD7BqvP8D8vqKNQzZ8Hc6PJg7X3Ko your-email@example.com
```

Copy the entire output (including `ssh-ed25519` and your email).

## Step 5: Add SSH Key to GitHub

1. Go to GitHub and log into your account
2. Click your profile picture in the upper-right corner
3. Click **Settings**
4. In the left sidebar, click **SSH and GPG keys**
5. Click **New SSH key** or **Add SSH key**
6. In the "Title" field, add a descriptive label (e.g., "Work Laptop")
7. Paste your key into the "Key" field
8. Click **Add SSH key**
9. If prompted, confirm your GitHub password

## Step 6: Test Your SSH Connection

Verify that your SSH key is working correctly:

```bash
ssh -T git@github.com
```

You should see a message like:
```
Hi YourUsername! You've successfully authenticated, but GitHub does not provide shell access.
```

If you see this message, your SSH key is set up correctly!

## Step 7: Configure Git to Use SSH

### For New Repository Clones

When cloning repositories, use the SSH URL instead of HTTPS:

```bash
# SSH URL format
git clone git@github.com:username/repository.git

# Instead of HTTPS
# git clone https://github.com/username/repository.git
```

### For Existing Repositories

To convert an existing repository from HTTPS to SSH:

**For the afp-estimator repository:**
```bash
# Change remote URL to SSH
git remote set-url origin git@github.com:KemosBram1/afp-estimator.git

# Push to main branch
git push origin main
```

**For other repositories:**
```bash
# General format
git remote set-url origin git@github.com:username/repository.git

# Push to your default branch
git push origin main  # or master, depending on your default branch
```

**Verify the remote URL was changed:**
```bash
git remote -v
```

You should see SSH URLs (starting with `git@github.com:`) instead of HTTPS URLs.

## Troubleshooting

### Permission Denied (publickey)

If you get a "Permission denied" error:

1. Make sure you copied the entire public key
2. Check that the key was added to your GitHub account
3. Verify the SSH agent is running and has your key: `ssh-add -l`
4. Try adding your key again: `ssh-add ~/.ssh/id_ed25519`

### Key Already Exists

If you get an error that the key already exists, you can:
- Use the existing key
- Generate a new key with a different filename: `ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/id_ed25519_new`

## Additional Resources

- [GitHub SSH Documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Git Documentation](https://git-scm.com/doc)

## Security Best Practices

1. **Never share your private key** (`~/.ssh/id_ed25519`)
2. **Use a passphrase** for additional security
3. **Keep your keys secure** with proper file permissions
4. **Rotate keys periodically** for enhanced security
5. **Use different keys** for different machines or purposes
