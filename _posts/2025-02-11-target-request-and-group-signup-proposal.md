---
published: 'true'
date: '2025-02-11 19:51 -0500'
author: Xanax
title: Target Request and Group Signup Proposal
description: Proposal for a new feature and process
keywords: 'feature, raiding, grouping, exp, leveling'
---
## The Issues with #epic-mob-fight-request
- Difficult to sort through requests and chatter
- No way to know if a request has been completed
- Time consuming for raid leader

## Use Case

The raid leader needs a fast and simple way to look at a raid night, and determine if any extra targets need to be added to the schedule. Members need a straightforward way of making requests. Removal of requests must be simple or hands-off.

## Proposal - Target Requests

1. We remove or "archive" all content in #epic-mob-fight-request.
2. Post a description of the new process:

	a. Use the Target Request Form to sumbit your request and availability.
    
    b. Requests can be found at [https://formerglory.lol/targets](https://formerglory.lol/targets "Target Requests")
    
    c. If you need a raid force for a target not in the form, please message Xanax
    
3. The thread is then locked so no posts can be made by members. This is done to keep the form and instructions visible at all times, indicating this is the new process. 

## Preview - Target Requests

The first part is a simple Google form. It does not require or capture authentication (emails). Each field is mandatory. The member enters their Name, selects the zone and target, and the days they are available. 

![form]({{site.baseurl}}/assets/img/form.png)

The results are available in a spreadsheet that will be made available to officers. The Timestamp and Completed columns are not printed. Any text in the Completed field will cause the row to not be printed. I did this so we can keep entries around for 30 days or so just to keep track of what we've done. 

![sheet]({{site.baseurl}}/assets/img/sheet.png)

The card system was designed to mimic a short ticket system. The raid leader can easily click on a raid day to jump to the cards for that day. Each card should be easy to read and cards are automatically sorted based on which targets we typically do on which days. Its all pretty simple and can be expanded per expansion for any targets that require a raid force. Currently the update process runs at 4 AM EST and 4 PM EST. 

![cards]({{site.baseurl}}/assets/img/cards.png)

## The Issues with closing #epic-mob-fight-request
- Smaller group content found in this channel will be funneled into #static-group-signup.
- #static-group-signup already suffers from similar problems with sorting content.
- The problems with #static-group-signup compounded over time and engagement has gone down.

## Use Case for a better LFG system
- Group chat should be contained so that other chat doesn't cause the group to lose focus when organizing.
- Different types of groups need to be identified example epic targets, exp groups, quest mobs, etc.
- The user needs to be able to sort through these easily to return to the content they are interested in.

## Proposal - Threads

Threads were made for this purpose. The #static-group-signup should be fully converted to Threads preventing normal chat in that channel, to enforce the new process.

![thread1]({{site.baseurl}}/assets/img/thread1.png)

- All conversation is contained in the related thread
- Tags can be set indicating the type of content the group is hunting
- Threads can be auto archived after 2 weeks of inactivity to keep active threads at the top
- Emoji's can easily be enforced so you can quickly discern how much interest there is in the posted event
- Discord comes with several ways of searching this type of content

I firmly believe this plan only works if both processes are enacted, giving people better tools for small or large group targets. Users will likely return to old habits if given the opportunity to do so.

## Future Thoughts

This was a fun project and I learned a lot. The minute I got the handshake between Github and Google to work, a slew of ideas opened up. I could give Dihat a Google Doc to paste his spells and sky items into. I could make another system for people to apply to the guild, and give tickets to officers to invite them. I'd love to add a way to post MQs on this Targets page too. I have a lot of work to do before Velious, thats for sure.
