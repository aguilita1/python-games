sea-python

This is the games I built in UMBC Summer Enrichment Academy (SEA) to learn python.

How to Create Repository From Existing Code

1. Initialize Git in your project folder

git init

2. Add all your code files to the staging area

git add .

3. Commit your files locally

git commit -m "Initial commit"

4. Rename your default local branch to 'main'

git branch -M main

5. Link your local project to your new GitHub repository

git remote add origin https://github.com/aguilita2/sea-python.git

6. Push your local code up to GitHub

git push -u origin main

How to commit changes later

1. Find what changed

git status

2. Decide which files you want to commit

Replace with actual file name e.g. README.md
Pro-Tip use tab key to automatically complete filename
git add <filename>

3. Add a commit message to describe the change me

replace message with some description of the commit
git commit -m "Added documentation"

4. Publish your changes to Github cloud.

Note you will likely need to log into you github account
git push
