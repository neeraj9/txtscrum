#!/usr/bin/python -u
"""

TODO: change string to unicode.

copyright (c) 2013 Neeraj Sharma <neeraj.sharma@alumni.iitg.ernet.in>
License: See LICENSE file
"""

import csv
import logging
import re


LOG = logging.getLogger(__name__)


class CsvFileBadInstance(Exception):
    pass


class CsvFileBadHeader(Exception):
    pass


class CsvFileEofException(Exception):
    pass


class CsvFileArrayBoundException(Exception):
    pass


class CsvFileQuery(object):
    """
    Query class to operate over the csv dataset.
    """
    def __init__(self, app, start_index=0, end_index=0):
        if end_index > 0:
            self.row_range = range(start_index, end_index+1)
        else:
            # indicates full range
            self.row_range = None
        self.app = app

    def get_range(self):
        """Let the application call this method to
        get the current range which reflect the latest
        filter result.
        """
        return self.row_range

    def sq_filter(self, column_index, cmp_func, typecast=None):
        """
        A generic filter which applies to a particular csv column_index
        (0 to N) and filters based on the cmp_func() over the column value.
        """
        new_row_range = []
        if self.row_range is not None:
            for i in self.row_range:
                val = self.app.read_val_by_col_index(column_index, i):
                if val in None:
                    continue
                if (typecast is not None):
                    val = typecast(val)
                if cmp_func(val):
                    new_row_range.append(i)
        else:
            # None is has special handing and self.row_range is None
            # when the complete file needs to be read.
            i = 0
            try:
                while True:
                    val = self.app.read_val_by_col_index(column_index, i):
                    if val in None:
                        continue
                    if (typecast is not None):
                        val = typecast(val)
                    if cmp_func(val):
                        new_row_range.append(i)
                    i += 1
            except CsvFileEofException, e:
                pass
        #
        # new_query = CsvFileQuery(self.app)
        #
        # CsvFileQuery can be derived, so instantiate the
        # derived class instead
        new_query = self.__class__(self.app)
        new_query.row_range = new_row_range
        return new_query

    def sq_filter_range(self, column_index, minval, maxval):
        """Filter the rows with cell of column_index name within
        the set [min,max]. Alternatively the value of the cell
        at column column_index is min <= x <= max.
        Note that the type(x) is datetime.datetime or int or float.
        """
        return self.sq_filter(column_index, lambda x: ((x >= minval) and (x <= maxval)))

    def sq_filter_equals(self, column_index, val):
        """Filter the rows with cell of column_index name filter_equal
        to val (doesnt matter if its datetime, unicode, int or float).
        """
        return self.sq_filter(column_index, lambda x: x == val)


    def sq_filter_strsearch(self, column_index, pattern, ignore_case=True):
        """Search that the pattern exists in the rows.

        Note that the pattern is treated as a python regular expression.
        See python re module for more details.
        """
        if ignore_case:
            p = re.compile(pattern, re.I)
        else:
            p = re.compile(pattern)
        return self.sq_filter(column_index, lambda x: p.search(x) is not None, str)

    def sq_filter_strmatch(self, column_index, pattern, ignore_case=True):
        """Match (exactly) that the pattern exists in the rows.

        Note that the pattern is treated as a python regular expression.
        See python re module for more details.
        """
        if ignore_case:
            p = re.compile(pattern, re.I)
        else:
            p = re.compile(pattern)
        return self.sq_filter(column_index, lambda x: p.match(x) is not None, str)


class CsvFileFormat(object):
    """
    Base class to any csv file format reader/processor.
    """
    def __init__(self, default_header, delimiter=','):
        self.delimiter = delimiter
        self.filename = None
        self.is_modified = False
        self.default_header = default_header
        self.header = None
        self.data = []

    def load(self, filename):
        # lazy loading
        if self.filename == filename:
            return
        self.filename = filename
        self.is_modified = False
        self.header = None
        self.data = []

    def query(self):
        """
        Get query object to operate over the dataset.
        """
        return CsvFileQuery(self)

    def read_val_by_col_index(self, column_index, row_index):
        """
        row_index starts with zero and so does column_index.

        NOTE: see the references below for speed optimizations and unicode
        * http://stackoverflow.com/questions/9087039/most-efficient-way-to-parse-a-large-csv-in-python
        * https://github.com/jdunck/python-unicodecsv
        * https://www.nesono.com/node/414

        A sample output of reading csv is as follows:

        >>> import csv
        >>> 
        >>> csvfile = open("task-list.csv", "rb")
        >>> dialect = csv.Sniffer().sniff(csvfile.read(10*1024))
        >>> csvfile.seek(0)
        >>> reader = csv.reader(csvfile, dialect)
        >>> header = reader.next()
        >>> header
        ['story-id(int)', 'task-id(int)', 'task-description(str)', 'initial-hrs(float)']
        >>> data = [row for row in reader]
        >>> data
        [['0', '0', 'Create readme.rst', '10'], ['0', '0', 'Create basic tasks', '20.5'], ['0', '0', 'Plan the first sprint', '15'], ['0', '0', 'Setup version control system for the project', '15']]
        """

        if not self.header:
            # load the file now
            csvfile = open(self.filename, "rb")
            dialect = csv.Sniffer().sniff(csvfile.read(10*1024))
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            header = reader.next()
            if header != self.default_header:
                raise CsvFileBadHeader("Got %s, when expected %s" % \
                        (header, self.default_header))
            self.header = header
            self.data = [row for row in reader]
            csvfile.close()
        if row_index >= len(data):
            LOG.error("row_index(%d) exeeds the number of data rows(%d)" % \
                      (row_index, len(data)))
            return None
        if column_index >= len(data[row_index]):
            LOG.error("column_index(%d) exeeds the number of columns(%d) at index %d" % \
                      (column_index, len(data[row_index]), row_index))
            return None
        return data[row_index][column_index]

    def set_data(self, index, row_values):
        """
        Set the row values at a particular row index.
        Note that the index=0 points to the first data entry in the csv file.
        """
        if len(data) <= index:
            raise CsvFileArrayBoundException();
        # the header is always the default_header, so change
        # default_header if you want to change that
        self.header = self.default_header
        self.data[index] = row_values
        self.is_modified = True

    def save(self):
        """
        Save the csv file from memory to file.
        """
        if self.is_modified:
            # write header first
            # loop over self.data and write each column
            self.is_modified = False
            outfile = open(self.filename, "wb")
            writer = csv.writer(outfile)
            writer.writerow(self.header)
            for x in self.data:
                writer.writerow(x)
            outfile.close()
            return True
        else:
            LOG.warn("No changes detected, so none written to the file.")
            return False


class ScrumTimeBoardQuery(CsvFileQuery):
    """
    """
    def filter_date_eq(self, date_val):
        """
        Filter data for a particular date.
        Note that the date_val must be in string format (str).

        TODO: change string to unicode.
        """
        assert(isintance(date_val, str))
        self.sq_filter_strmatch(0, date_val)


class ScrumSprintListQuery(CsvFileQuery):
    pass


class ScrumStoryListQuery(CsvFileQuery):
    pass


class ScrumTaskListQuery(CsvFileQuery):
    pass


class ScrumTimeBoardFormat(CsvFileFormat):
    """
    The scrum time board format is in CSV and the format is as follows:

    date(yyyymmdd),author(str),story-id(int),task-id(int),hrs-spent(float)

    Note that there is one file per sprint (for a project).
    """
    HEADER = ['date(yyyymmdd)', 'author(str)', 'story-id(int)', 'task-id(int)', 'hrs-spent(float)']

    def __init__(self):
        CsvFileFormat.__init__(self, ScrumTimeBoardFormat.HEADER)

    def query(self):
        """
        Get query object to operate over the dataset.
        """
        return ScrumTimeBoardQuery(self)


class ScrumSprintListFormat(CsvFileFormat):
    """
    The scrum sprint list format is in CSV and the format is as follows:

    sprint-id(int),sprint-description(str)

    Note that there is one file per project.
    """
    HEADER = ['sprint-id(int)', 'sprint-description(str)']

    def __init__(self):
        CsvFileFormat.__init__(self, ScrumSprintListFormat.HEADER)

    def query(self):
        """
        Get query object to operate over the dataset.
        """
        return ScrumSprintListQuery(self)


class ScrumStoryListFormat(CsvFileFormat):
    """
    The scrum story list format is in CSV and the format is as follows:

    sprint-id(int),story-id(int),story-description(str)

    Note that there is one file per project.
    """
    HEADER = ['sprint-id(int)', 'story-id(int)', 'story-description(str)']

    def __init__(self):
        CsvFileFormat.__init__(self, ScrumStoryListFormat.HEADER)

    def query(self):
        """
        Get query object to operate over the dataset.
        """
        return ScrumStoryListQuery(self)


class ScrumTaskListFormat(CsvFileFormat):
    """
    The scrum task list format is in CSV and the format is as follows:

    story-id(int),task-id(int),task-description(str),initial-hrs(float)

    Note that there is one file per project.
    """
    HEADER = ['story-id(int)', 'task-id(int)', 'task-description(str)', 'initial-hrs(float)']

    def __init__(self):
        CsvFileFormat.__init__(self, ScrumTaskListFormat.HEADER)

    def query(self):
        """
        Get query object to operate over the dataset.
        """
        return ScrumTaskListQuery(self)

