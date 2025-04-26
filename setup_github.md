# Setting up GitHub Remote with Access Token

To push your code to GitHub using an access token, follow these steps:

## 1. Create a GitHub Personal Access Token (if you haven't already)

1. Go to GitHub and log in to your account
2. Click on your profile picture in the top right corner
3. Go to Settings > Developer settings > Personal access tokens > Tokens (classic)
4. Click "Generate new token" and select "Generate new token (classic)"
5. Give your token a descriptive name
6. Select the scopes or permissions you want to grant this token (for pushing to a repository, you need at least the `repo` scope)
7. Click "Generate token"
8. Copy the token (you won't be able to see it again!)

## 2. Add the remote repository with your token

Run the following command, replacing `YOUR_ACCESS_TOKEN` with your actual token:

```bash
git remote add origin https://YOUR_ACCESS_TOKEN@github.com/TanveerAhmedKhan/Restaurant_reservation.git
```

For example, if your token is `ghp_abc123def456`, the command would be:

```bash
git remote add origin https://ghp_abc123def456@github.com/TanveerAhmedKhan/Restaurant_reservation.git
```

## 3. Push your code to GitHub

After setting up the remote with your token, you can push your code:

```bash
git push -u origin master
```

## Note on Security

- Never share your access token with anyone
- Don't commit the token to your repository
- If you accidentally expose your token, go to GitHub and revoke it immediately, then generate a new one
