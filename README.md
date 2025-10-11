# githubcontribs: Simple analytics for GitHub contributions across an organization

Install:

```
pip install githubcontribs
```

Quickstart:

```
from githubcontribs import GitHubContribs
contribs = GitHubContribs("laminlabs")
df = contribs.get_contribs("lamindb")
df.head()
#> Dataframe of contributions
```

Contributing: Please run `pre-commit install` and `gitmoji -i` on the CLI before starting to work on this repository!
