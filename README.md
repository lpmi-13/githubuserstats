# GithubUserStats

measuring a "mostly made up metric" &trade;

## rationale

the most common way to measure contributions to Github is via total commits,
and while this is a great measure of depth, it doesn't necessarily capture
breadth of contributions as well.

Mostly spurred on by my [pypobot](https://github.com/lpmi-13/pypobot) adventures,
I felt like christening a new metric, primarily as a way to start a conversation
about open source contributions, but also selfishly as one that exaggerates 
the contributions via pypobot.

## what does it measure?

contributions by merged PR into a unique repo not owned by the PR author.

for example:

user `foo` has the following merged PRs:
- `https://github.com/foo/ownRepo/pull/12`
- `https://github.com/foo/ownRepo/pull/16`
- `https://github.com/bar/newProject/pull/3`
- `https://github.com/bar/newProject/pull/5`
- `https://github.com/baz/oldProject/pull/8`

the score for the metric would be 2, since there are two commits to `bar/newProject`,
but it's the same repo, so that only gets counted once. `baz/oldProject` is also
a repo not owned by `foo`, so that gets an additonal point. Both of the merged PRs
to `foo/ownRepo` are owned by the PR author, so they don't count in the metric.

## output

currently takes hardcoded userdata (taken from the very excellent
[Gist by Paul Miller](https://gist.github.com/paulmillr/2657075)) and outputs
values for this particular metric

eventually hoping to have an online portal for browsing the output as well as adding
in a particular github username to be included in the results, but just haven't
had the time yet.

## basic overview of data flow

### 1) `getMergedPRs.py`

- reads in from `baseline_data/git-users.json`
- iterates through the users and calls the Github search API for all the user's issues which are PRs
- checks to see if the PR is merged
- if the PR was merged, saves the issue's html url as well as the date merged for later filtering
- writes the saved data to `data/` folder as `USER_LOGIN-results` (one repo url and date per line)

### 2) `getGraph.py`

- opens the output of the above process (grabbing each file from the `/data` directory)
- for each user result file, checks if the user login is the same as the owner of the repo
(currently done via looking at the value after `https://github.com/` in the issue URL)
- if the user login and owner are not the same, adds the issue to the list of repos contributed to
- makes this list a set to filter for unique repos
- writes this result to `results.txt`

...this is currently as far as the data is processed, though would be nice to eventually
put the results into a data store or something, then make available via an API.


### caveats

in theory, one user could create a number of different users from various email accounts and then
simulate getting PRs merged into unique repos that look like they're different from the original
author, but that would take a level of interest in this metric that is unlikely at best.
