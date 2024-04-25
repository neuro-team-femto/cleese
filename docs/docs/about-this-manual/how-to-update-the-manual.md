# How and when to update the manual

## When to update the manual

Anytime you like !! This document is meant as a place of continuous improvement, and being on the look-out for opportunities to update the lab manual is good lab citizenship. 

Changes can be anything from minor (ex. fix a typo), add or edit an information (ex. link has changed, or information needs updating), to adding a new page or section. Changes can also concern the formatting of the manual, which is also fully configurable (although such changes should be handled with care, as they may break existing pages). 

A good rule of thumb is that 

1. whenever you learn about how to do a certain procedure (ex. admin), 

2. the information for doing it is either not in the manual, or the info there did not help, and

3. there is non-0% probability that other lab members may one day have to do the same, 

then the manual should be updated. 


## How to update

### First, communicate about it

If you have any comments or suggestions regarding the contents of this manual, use the `#lab_manual` Slack channel to communicate about it : mention `@` your PI, explain what change you'd like to see, and whether you'd like to do it yourself. 


### Second, make your change

This manual is written in the [materials for mkdocs](https://squidfunk.github.io/mkdocs-material/) framework, and is hosted as a repository on the lab's [github page](https://github.com/neuro-team-femto). Materials for mkdocs is a simple framework for writing online documentation, in which every file is simply written in [Markdown](https://en.wikipedia.org/wiki/Markdown). Every page in this manual is stored as a single .md file in the [lab_manual](https://github.com/neuro-team-femto/lab_manual) repository.

!!! hint
	Mkdocs-material has a lot of fancy formatting options (like this box, called an admonission). See [this page](https://squidfunk.github.io/mkdocs-material/reference) for reference.  

This means that, in the most simple instance, updating this manual simply requires you to edit the corresponding page with your favorite text editor, and then either create a pull request or push the new change to the repository, via your preferred git method. 

#### Updating via a pull request (recommended best practice)

1. Material for MkDocs is published as a Python package and can be installed with pip. If you haven't already, open up a terminal and install Material for MkDocs with:
	```
		pip install mkdocs-material

	```

2. Fork the [lab_manual](https://github.com/neuro-team-femto/lab_manual) repository to your personal git account

3. Clone the repo to your local computer, e.g. at `c:/work/lab_manual`

4. Use you favorite text editor to make any change to existing .md pages, which are stored in `c:/work/lab_manual/docs` 

5. You can preview your changes by running `mkdocs serve` from your local repository, i.e.  `c:/work/lab_manual> mkdocs serve`. Your local manual will be accessible in the browser at `http://localhost:8000`, and any changes you make to the files in `c:/work/lab_manual/docs` will be reflected immediately. 

6. Once you're happy with the changes, git add, commit and push to your remote repository in your personal git account

7. Then issue a PR to the main [repository](https://github.com/neuro-team-femto/lab_manual), so your change can be reviewed and merged. 

#### Pushing directly to the lab's git (faster, non-recommended) 

If you have write permission to the master repository on the lab's [github page](https://github.com/neuro-team-femto), you have the option to push directly to the [lab_manual](https://github.com/neuro-team-femto/lab_manual) repository. 

1. If you haven't already, open up a terminal and install Material for MkDocs with:
	```
		pip install mkdocs-material

	```

2. Clone the [lab_manual](https://github.com/neuro-team-femto/lab_manual) repository to your local computer, e.g. at `c:/work/lab_manual`

3. Use you favorite text editor to make any change to existing .md pages, which are stored in `c:/work/lab_manual/docs` 

5. You can preview your changes by running `mkdocs serve` from your local repository, i.e.  `c:/work/lab_manual> mkdocs serve`. Your local manual will be accessible in the browser at `http://localhost:8000`, and any changes you make to the files in `c:/work/lab_manual/docs` will be reflected immediately. 

6. Once you're happy with the changes, git add, commit and push to the team's repo. 

!!! warning
	When you do this, your changes cannot be reviewed before publishing. If you're uncertain about your doing (or if you care about good etiquette), use the PR procedure above instead. 

#### Commiting directly on the lab's git page (fastest, not recommended) 

If you have write permission to the master repository on the lab's [github page](https://github.com/neuro-team-femto), and you don't need to preview/test/debug your changes, you have the option to edit changes directly on the lab's [repository page](https://github.com/neuro-team-femto/lab_manual). This should be restricted to simple changes which have very little chances to break the manual (ex. fixing a typo) and to situations where any of the favored approaches above are impractical (ex. pushing a quick change from your mobile phone) 


1. Navigate to the page you'd like to change on the lab's [repository page](https://github.com/neuro-team-femto/lab_manual), e.g. for this page [https://github.com/neuro-team-femto/lab_manual/blob/main/docs/about-this-manual/how-to-update-the-manual.md](https://github.com/neuro-team-femto/lab_manual/blob/main/docs/about-this-manual/how-to-update-the-manual.md)

	!!! tip
		You can open the github page for any specific page in the manual by clicking on the pencil-shape edit icon next to the page title (scroll up). 

2. Click the pencil-shape edit button on the top right corner of the github page

4. Make your changes, enter a commit message that describes what change you did, and click commit

!!! warning
	When you do this, your changes cannot be reviewed before publishing. If you're uncertain about your doing (or if you care about good etiquette), use the PR procedure instead. 






