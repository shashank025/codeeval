from os import environ
from collections import namedtuple
from itertools import chain, combinations

Point = namedtuple('Point', ['lat', 'lon'], verbose=False)

def debug_print(msg):
    if 'DEBUG' in environ and environ['DEBUG']:
        print msg

def intersect1d((start1, end1), (start2, end2)):
    """Do these 1-D line segments intersect?

    Assumptions: start1 <= end1 and start2 <= end2.

    1-d line segments are line segments that lie
    on the same straight line, e.g., the x-axis.

    >>> intersect1d((2, 4), (5, 7))  # disjoint
    False
    >>> intersect1d((2, 7), (5, 6))  # contained
    True
    >>> intersect1d((2, 7), (5, 9))  # proper int
    True
    >>> intersect1d((5, 7), (2, 4))  # disjoint
    False
    >>> intersect1d((5, 6), (2, 7))  # contained
    True
    >>> intersect1d((5, 9), (2, 7))  # proper int
    True
    """

    assert start1 <= end1, "first arg for intersect1d invalid: start > end"
    assert start2 <= end2, "second arg for intersect1d invalid: start > end"
    return start2 <= end1 <= end2 or start1 <= end2 <= end1

def box((p1, p2)):
    """Returns the bounding box corresponding to the segment (p1, p2).

    >>> box((Point(24, -35), Point(21, 46)))
    (Point(lat=21, lon=-35), Point(lat=24, lon=46))
    """
    return Point(min(p1.lat, p2.lat), min(p1.lon, p2.lon)), Point(max(p1.lat, p2.lat), max(p1.lon, p2.lon))

def box_overlap(segment1, segment2):
    """Do the bounding boxes formed by these two segments overlap?

    Note that this is a prerequisite for the segments intersecting.
    """

    pstart1, pend1 = box(segment1)
    pstart1, pend2 = box(segment2)

    xint = intersect1d((pstart1.lat, pend1.lat), (pstart2.lat, pend2.lat))
    if not xint:
        return False
    yint = intersect1d((pstart1.lon, pend1.lon), (pstart2.lon, pend2.lon))
    return yint

def ccw(a, b, c):
    """Points a, b, c are counterclockwise iff slope of ab is less than slope of ac"""
    return (a.lat - c.lat)*(a.lon - b.lon) > (a.lat - b.lat)*(a.lon - c.lon)

def cross((A, B), (C, D)):
    """returns True if and only if the two segments intersect.

    From http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/

    >>> segment1 = (Point(37.532599, -122.218094), Point(37.615863, -122.097244))
    >>> segment2 = (Point(37.516262, -122.198181), Point(37.653383, -122.151489))
    >>> cross(segment1, segment2)
    True
    >>> segment2 = (Point(37.788353, -122.387695), Point(37.829853, -122.294312))
    >>> cross(segment1, segment2)
    False
    """
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def feasible(indices, segments):
    """Is there no pair of crossing segments?

    >>> s1 = (Point(37.532599, -122.218094), Point(37.615863, -122.097244))
    >>> s2 = (Point(37.788353, -122.387695), Point(37.829853, -122.294312))
    >>> s3 = (Point(37.516262, -122.198181), Point(37.653383, -122.151489))
    >>> feasible([1, 2], {1: s1, 2: s2, 3: s3})   # we know these two dont cross
    True
    >>> feasible([1, 2, 3], {1:s1, 2:s2, 3:s3})   # we know s1 and s3 cross
    False
    """
    return not(any(cross(segments[s1], segments[s2])
                   for s1, s2 in combinations(indices, 2)))

def bridges(segments):
    """Return the largest subset of bridges with no intersecting bridges

    >>> s1 = (Point(37.788353, -122.387695), Point(37.829853, -122.294312))
    >>> s2 = (Point(37.429615, -122.087631), Point(37.487391, -122.018967))
    >>> s3 = (Point(37.474858, -122.131577), Point(37.529332, -122.056046))
    >>> s4 = (Point(37.532599, -122.218094), Point(37.615863, -122.097244))
    >>> s5 = (Point(37.516262, -122.198181), Point(37.653383, -122.151489))
    >>> s6 = (Point(37.504824, -122.181702), Point(37.633266, -122.121964))
    >>> bridges({1:s1, 2:s2, 3:s3, 4:s4, 5:s5, 6:s6})
    [1, 2, 3, 5, 6]
    """

    for size in range(len(segments), 0, -1):
        for subset in combinations(segments, size):
            if feasible(subset, segments):
                # subsets of size 1 are always feasible,
                # so we *will* always return something.
                return sorted(subset)

if __name__ == '__main__':
    import doctest
    import fileinput
    import re

    pattern = r"\[(\-?\d+(?:.\d+)),\s*(\-?\d+(?:.\d+))\],\s*\[(\-?\d+(?:.\d+)),\s*(\-?\d+(?:.\d+))\]"
    regex = re.compile(pattern)
    input = {}
    for line in fileinput.input():
        idx, points_str = line.split(':')
        idx = int(idx)
        match = regex.search(points_str)
        if match:
            g = [float(e) for e in match.groups()]
            p1 = Point(g[0], g[1])
            p2 = Point(g[2], g[3])
            input[idx] = (p1, p2)
    debug_print("input = %s" % (input,))
    for b in bridges(input):
        print b
