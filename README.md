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

## what does it measure?

contributions by merged PR into a unique repo not owned by the PR author.

## output

currently takes hardcoded userdata (taken from the very excellent
[Gist by Paul Miller](https://gist.github.com/paulmillr/2657075)) and outputs
values for this particular metric

eventually hoping to have an online portal for browsing the output as well as adding
in a particular github username to be included in the results, but just haven't
had the time yet.

## basic overview of data flow

### `getMergedPRs.py`

- reads in from `baseline_data/git-users.json`
- iterates through the users and calls the Github search API for all the user's issues with are PRs
- checks to see if the PR is merged
- if the PR was merged, saves the issue's html url as well as the date merged for later filtering
- writes the saved data to `data/` folder as `USER_LOGIN-results` (one repo url and date per line)

### `getGraph.py`

- opens the output of the above process (grabbing each file from the `/data` directory)
- for each user result file, check if the user login is the same as the owner of the repo
(currently done via looking at the value after `https://github.com/` in the issue URL
- if the user login and owner are not the same, add the issue to the list of repos contributed to
- make this list a set to filter for unique repos
- write this result to `results.txt`

...this is currently as far as the data is processed, though would be nice to eventually
put the results into a data store or something, then make available via an API.
