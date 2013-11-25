txtscrum
========

A text file based Scrum project planning.

## Authors

* Neeraj Sharma <neeraj.sharma@alumni.iitg.ernet.in>

## Motivation


I wanted a text based project planning and timesheet maintainance
software, so that the data can be added to a version control system
and complex tools can be built easily to analyze the project.


## Goals

* Text based project planning and timesheet management system
* Clear separation of content and tools
* Follow the KISS principle
* Portable across platforms
* Easy to build tools for creating and visualizing content
* Version control friendly


## History

<table>
<th>
  <td>Date (YYYY-MM-DD)</td>
  <td>Author</td>
  <td>Comment</td>
</th>
<tr>
  <td>2013-11-25</td>
  <td>Neeraj Sharma</td>
  <td>Initial content</td>
</tr>
</table>

## Design

The csv (command separated values) is widely accepted and easy to read
file format. There are numerous ways to store data but csv comes closer
to a human readable, yet a compact format. The wide acceptance of the
file format ensures tons of tools and programming libraries to process
the data. Which is by far the most important reason to pick csv instead
of creating another content format.

The proposed format is to create a new folder per project and each
project will have number of files as shown below:

1. readme.rst
2. task-list.csv
3. story-list.csv
4. sprint-list.csv
5. time-board-1.csv
6. time-board-2.csv
7. time-board-3.csv
8. time-board-4.csv
9. (... and so on ...)

> The time-board-X.csv is a split to keep the time-board manageable, so
> you could choose to have just one of the files instead of splitting into
> many of those.
>
> I suggest that you keep one time-board file per sprint (as a convention).
>

### readme.rst

The readme.rst (RestructedText file format) is for doumentation purpose, which
should contain useful information related to the project. I know that
documentation is seldom the focus of a project, but dont neglect it and it will
pay off in the future.


> This file can contain references to design document or content which is
> useful in understanding the project. Please refrain from adding content
> related to implementation or low level design, because that will just
> make this document long and not so useful. You should just focus on
> very high level information and have references to design or implementation
> howto/doc instead.


### task-list.csv

The tast-list.csv (one per project) contains all the tasks in a project, so
this could be a pretty big file. Additionally, each entry in this file will
map a story with a task. In the beginning you could use story-id 0 (reserved
for backlog story) while planning out the project. The real stories can
be substituted after the sprint planning, so before the first sprint the
value of story-id in each row will be 0.


    story-id(int),task-id(int),task-description(str),initial-hrs(float)


### story-list.csv

The story-list.csv (one per project) contains all the stories planned in a
project. When you are starting out the project always assign sprint-id as 0
for unplanned stories. The content will be updated during sprint planning
when the team creats stories out of one or more tasks. Note that the
sprint-id 0 is reserved for backlog stories, so there will be time when
unfinished stories needs to be moved to the backlog. That is the time
when you will use sprint-id 0 for unfinished stories. Additionally, there
will be time when few of the tasks are unfinished in the story, so you will have
to create new entries with sprint-id 0 and a new story-id indicating a
continuation of earlier story-id in the description (as "continue story-id#Y").

    sprint-id(int),story-id(int),story-description(str)


> This file maps a sprint to number of stories, so it will have useful
> information before the sprint is started.


### sprint-list.csv

The sprint-list.csv (one per project) contains the list of sprints in a project.
This file is very compact and stores description of a sprint. This file will
have useful information once sprints are planned, so update the content
during sprint planning.

    sprint-id(int),sprint-description(str)


> Dont try to go overboard and try to create sprints unnecessarily. Read the
> section on Workflow to gain a better understanding of which content
> needs to be created during the process for optimal use.


### time-board-X.csv

The time-baord-X.csv (can be many per project) will contain timesheet filled
by the team members. There can be one or more than one such file per project
to allow management of timesheets. It is recomended to have one such file per
sprint for easy management, but its not enforced at present. This flexibility
comes at a cost - which is the tool writers needs to parse all the time-board
files before concluding anything useful. If this troubles you then writing
a tool rearranging timesheets per sprint is as simple as finding all the
story-id which exists in a sprint and then filtering story-id into a new
time-board set of files. This step can be automated as a version control hook
so the sanity of these files is ensured (without trusting the developers).


    date(yyyymmdd),author(str),story-id(int),task-id(int),hrs-spent(float)


## Workflow

1. Create readme.rst with project aim/goal/motivation/introduction/etc info.
2. Create task-list.csv with the smallest possible tasks. Dont worry if you
   cannot split to hearts content because you can always do that later.
3. Create story-list.csv during sprint planning and aggregate tasks into
   stories which have a tangible output.
4. Create sprint-list.csv during sprint planning and include as much
   stories which can be completed in the stipulated time.
5. Start adding time-board-X.csv (preferably one per sprint) during the
   sprint.



## Advantages

This project is a starting point to introduce a text based project
management, but since the format is so simple so you could choose to
dump the set of tools provided in this project and use your own.
Additionally, you can take advantage of any spreadsheet application
to process the information in any way possible. The csv format
also allows easy migration to custom format or importing the same to
other project management softwares. This gives a lot of flexibility
in migrating to another framework without much of effort (the
target framework should allow some means of doing that ofcourse).

