# GithubUserStats

measuring a "mostly made up metric" &trade;

## rationale

the most common way to measure contributions to Github is via total commits,
and while this is a great measure of depth, it doesn't necessarily capture
breadth of contributions as well.

Mostly spurred on by my [pypobot](https://github.com/lpm-13/pypobot) adventures,
I felt like christening a new metric, primarily as a way to start a conversation
about open source contributions, but also selfishly as one that exaggerates 
the contributions via pypobot.

An article I wrote about it, explaining in a bit more detail, is [here](https://medium.com/@leskis/why-the-github-metric-monoculture-d179a2f1d130).

### historical note

- the original version of the data collection used the GitHub API directly, querying specific users with no way to "get all users"
- this currently lives in the `legacy` branch, if you're interested

## what does it measure?

contributions by merged PR into a unique repo not owned by the PR author.

## output

sends everything into a postgres DB that can be used to populate a frontend.

## basic overview of data flow

### GH Archive https://www.gharchive.org/

- supplies data in json format from the Timeline API (pre-2015) and the Events API (post-2015)
- the API isn't 100% stable/predictable prior to 2015, so that's why the python scripts have all the try/except blocks

### `grab_gharchive.sh`

- pulls down data from the GitHub archive (in gzipped json format), one month at a time (the more recent months can total over 10GB of data)
- unzips and passes each json file into `convert_data.py`
- removes the raw data files

### `convert_data.py`

- reads in the raw json, and filters for merged PRs to repos where the owner is not the same as the author
- saves some data about those (repo url, PR url, author's username, unique identifier), and writes out to a json file
