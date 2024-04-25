# Using Slack


## Principle

All of our lab communication goes through our dedicated [Slack workspace](https://neuro-group-femto.slack.com), and not by email (see [this page](../../../becoming-a-lab-member/important-lab-accounts/) for how to install and get a Slack account). 

## Good practices

We have a number of good practices on how to use Slack: 

- no internal email. Slack only works if we know all the information is there, and nowhere else. Don't send information to other lab members or your PI(s) by email. If you need to transfer information from a specific email, or are responding to email conversations including both lab members and external collaborators who are not on slack, please also send a quick notification on slack, and consider copying important information and files directly to slack too.  

- default language on Slack is English. If you're a French speaker, please use French only in DMs with other French speakers, or in specific project channels where it is absolutely certain that no one involve will ever _not_ be a French speaker. Be respectuful of the future lab member who may be taking on part of your project in 6 months, and may not be a French speaker.  

- every conversation should occur in a public channel: while one may think that discussing a minor point of their research project is not of public interest to the rest of the group, and may be tempted to do it in private direct messages - refrain: first, you never know whether that is the case, and you may often find that someone may chime in with the relevant expertise even though you didn't think they could. Second, maintaining all conversation public also helps creating collective mindspace: even if one doesn't take part in all parallel conversations, we know that these are happening. 

!!! warning "Exceptions"

	The only exception to posting publicly is, of course, confidential information about HR, leave of absence, etc. and anything contract related. Please contact your PI directly with direct message about these. For longer conversations that you want to keep private (e.g. apply to a competitive position), you can also create a private channel. 

- create dedicated channels liberally: the rule of thumb is to create and use one dedicated channel per project (see below), but channels can also be created adhoc to discuss e.g. who's going to a specific conference, etc.  Don't spam the #general channel for specific project communication. Also, try not to bury information about one project into another project's channel. You can have as many active channels as you have projects. 

- Upon creating a new channel, include the relevant people and post a brief message about what the channel is about. When they are not used, channels can be archived so they can still be searched. 

- use the #general channel for common interest announcements, a bit like a mailing list. Don't spam it with specific project conversation (rule of thumb: if you're tagging a single person in your message, this probaby shouldn't go to #general), but it's totally ok to use it for sending e.g. a polite note to let people know you'll be late to the lab on a certain day, etc. 

- familiarize yourself with notifications/channel follows: while everything is by default public, Slack is replete with options to e.g. get only notified of certain categories of messages, or follow and stop following certain channels as your work may need. Take some time to optimize what information you're getting. 


!!! warning "Slack and work-life balance"

	Because we don't use email for internal communication among lab members, we tend to use Slack as both a synchronous (e.g. to chat in real-time) and asynchronous (e.g. post an idea, a request, share a paper...) means of communication. This means that you'll see slack messages being posted at pretty much any time, including by PIs. Except in case of clear emergency (which will be clearly indicated by your PI), please don't take this as an injonction to answer outside of normal working hours - you can if you like, but you are not expected to.

## 1 project, 1 channel

In our domain of research, the standard unit of research is typically the experiment: one experiment gets brainstormed (to find the best idea, and the best way to address it), designed (both conceptually, and practically with e.g. Python code), data collected, analysed, and a journal paper written. For practicality, let's call all this package of work a "project". 

By rule, every new project should get : 

1. its dedicated slack channel
2. its dedicated repo on the lab's github

!!! warning 
	By rule, every project should have PI approval - so, basically, involve your PI in deciding whether to launch a new slack/repo project space. 

Both channel and repo should have the same name (sometimes the first thing we should talk about is decide on how we call the channel and repo). All information/discussion about that project goes to that channel, and all code regarding the project's experiment design and data analysis should go to that repo. 

In addition, channels and repo should be linked using the `/github` [bot](https://slack.github.com/). Type  `/github subscribe [repository_name]` in the repository_name channel in Slack, and the channel will automatically post updates about e.g. commits, PRs, etc. occurring in the repo. 

!!! hint
	If you make any change to the lab_manual, i.e. to [the lab_manual repo in github](./../../../about-this-manual/how-to-update-the-manual/), you'll see automatic notifications in the lab_manual channel in Slack. That's because the lab_manual channel was subscribed to the corresponding repo in github, in the same way project channel should be. 

Because this cycle of _design + data-collection + analysis + writing_ can be quite long, we expect the typical active life of a project channel would be about ~1 year. The typical project channel will implicate mainly one lab member (e.g. PhD student or postdoc) + their PI, with the adhoc addition of whoever else is needed for expertise/comments etc. over the course of the project. Sometimes we will also invite to Slack external collaborators (.g. co-supervisors for some PhD projects) so we keep all project discussion in Slack. 

Each lab member can of course participate in as many project channels in parallel, as needed and as their work develops. The rule of thumb is that PhD students create perhaps one project channel per year (culminating in 3 parallel project in their 3rd year, one in design/data-collection, another in data-analysis, and a third one at the paper-writing stage), and that postdocs may entertain 2-3 projects from their first year, but there are no rule. 


