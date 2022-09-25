from git import Repo
from pathlib import Path

git_dir = f"{Path.home()}/Documents/Programming/YoutubeAutomationPY"

repo = Repo(git_dir)
origin = repo.remotes.origin
origin.fetch()
repo.head.ref.set_tracking_branch(origin.refs.main)
repo.heads.main.checkout()
origin.pull() 
