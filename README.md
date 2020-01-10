# fidele007 Repo

fidele007's Cydia repository for personal projects.

## Docker

A Docker container for this static site can be easily setup:

```bash
docker build -t github-page .
docker run -v [LOCAL_REPO_PATH]:/usr/share/nginx/html -d -p 80:80 github-page
```
