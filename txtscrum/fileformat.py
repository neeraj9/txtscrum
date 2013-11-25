"""
copyright (c) 2013 Neeraj Sharma <neeraj.sharma@alumni.iitg.ernet.in>
License: See LICENSE file
"""

class ScrumTimeBoardFormat(object):
    """
    The scrum time board format is in CSV and the format is as follows:

    date(yyyymmdd),author(str),story-id(int),task-id(int),hrs-spent(float)

    Note that there is one file per sprint (for a project).
    """
    pass


class ScrumSprintListFormat(object):
    """
    The scrum sprint list format is in CSV and the format is as follows:

    sprint-id(int),sprint-description(str)

    Note that there is one file per project.
    """
    pass


class ScrumStoryListFormat(object):
    """
    The scrum story list format is in CSV and the format is as follows:

    sprint-id(int),story-id(int),story-description(str)

    Note that there is one file per project.
    """
    pass


class ScrumTaskListFormat(object):
    """
    The scrum task list format is in CSV and the format is as follows:

    story-id(int),task-id(int),task-description(str),initial-hrs(float)

    Note that there is one file per project.
    """
    pass
