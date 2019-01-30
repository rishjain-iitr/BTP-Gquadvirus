import math
import queue
import time


class G4Candidate:

    def __init__(self, sequence, tetrads, start_pos):
        self.sequence = sequence
        self.numTetrads = tetrads
        self.start = start_pos
        self.y1 = -1
        self.y2 = -1
        self.y3 = -1
        self.tstring = ""
        for i in range(self.numTetrads):
            self.tstring += "G"
        self.maxLength = 30 if (self.numTetrads < 3) else 45

    def gmax(self):
        return (self.maxLength - (self.numTetrads * 4 + 1))

    def score(self):
        gavg = float(
            (
                abs(self.y1-self.y2) +
                abs(self.y2-self.y3) +
                abs(self.y1-self.y3)
            )/3.0
        )
        return math.floor(self.gmax() - gavg + self.gmax() * (self.numTetrads-2))

    def length(self):
        return (4 * self.numTetrads + self.y1 + self.y2 + self.y3)

    def t1(self):
        return self.start

    def t2(self):
        return (self.t1() + self.numTetrads + self.y1)

    def t3(self):
        return (self.t2() + self.numTetrads + self.y2)

    def t4(self):
        return (self.t3() + self.numTetrads + self.y3)

    def cursor(self):
        if (self.y1 < 0):
            return self.t1() + self.numTetrads
        elif (self.y2 < 0):
            return self.t2() + self.numTetrads
        elif (self.y3 < 0):
            return self.t3() + self.numTetrads
        else:
            return -1

    def partialLength(self):
        length = (self.numTetrads) * 4
        # add the minimum loops left
        if (self.y1 >= 0) and (self.y2 < 0):
            # only hte first loop is known
            if (self.y1 == 0):
                # other two must be at least 2
                length += 2
            else:
                length += 1
        elif (self.y2 >= 0) and (self.y3 < 0):
            # first two loop lengths are known
            if (self.y1 == 0) or (self.y2 == 0):
                length += 1
        # add the current loops
        if (self.y1 > 0):
            length += self.y1
        if (self.y2 > 0):
            length += self.y2
        if (self.y3 > 0):
            length += self.y3
        return length

    def minAcceptableLoopLength(self):
        if (self.y1 == 0 or self.y2 == 0 or self.y3 == 0):
            return 1
        else:
            return 0

    def complete(self):
        if (self.y1 < 0 or self.y2 < 0 or self.y3 < 0):
            return False
        else:
            return True

    def viable(self, min_score):
        if (self.score() < min_score):
            return False
        if (self.length() > self.maxLength):
            return False
        # only one loop is allowed to have a 0 length
        count = 0
        if (self.y1 < 1):
            count += 1
        if (self.y2 < 1):
            count += 1
        if (self.y3 < 1):
            count += 1
        return (count < 2)

    def findLoopLengthsFrom(self, ys, i):
        p = i
        done = False
        while(not done):
            p = (self.sequence).find(self.tstring, p)
            if (p < (self.start+self.maxLength+1) and p >= 0):
                y = p - i
                if (y >= self.minAcceptableLoopLength()) and ((p-self.start+len(self.tstring)-1) < self.maxLength):
                    ys.put(y)
                else:
                    done = True
            else:
                done = True
            p += 1

    def expand(self, cands):
        ys = queue.Queue()
        self.findLoopLengthsFrom(ys, self.cursor())
        # print(ys.qsize())
        # print(list(ys.queue))

        while (not ys.empty()):
            y = ys.get()
            cand = G4Candidate(self.sequence, self.numTetrads, self.start)
            cand.y1 = self.y1
            cand.y2 = self.y2
            cand.y3 = self.y3
            if self.y1 < 0:
                cand.y1 = y
            elif self.y2 < 0:
                cand.y2 = y
            elif self.y3 < 0:
                cand.y3 = y
            # print(cand.partialLength())
            # if cand.y1 < 0 or cand.y2 < 0 or cand.y3 < 0:
            #     print(True)
            #     pass
            if (cand.partialLength() <= cand.maxLength):
                cands.put(cand)


class G4(G4Candidate):
    def __init__(self, candidate):
        self.start = candidate.start
        self.tetrads = candidate.numTetrads
        self.tetrad1 = candidate.t1()
        self.tetrad2 = candidate.t2()
        self.tetrad3 = candidate.t3()
        self.tetrad4 = candidate.t4()
        self.y1 = candidate.y1
        self.y2 = candidate.y2
        self.y3 = candidate.y3
        self.length = candidate.length()
        self.gscore = candidate.score()
        self.sequence = candidate.sequence[candidate.start:candidate.length()]
        self.overlaps = []

    def isequal(self, other):
        if (self.start != other.start):
            return False
        if (self.tetrads != other.tetrads):
            return False
        if (self.y1 != other.y1):
            return False
        if (self.y2 != other.y2):
            return False
        if (self.y3 != other.y3):
            return False
        return True


def overlapped(a, b):
    a_start = a.start
    a_end = a_start + a.length

    b_start = b.start
    b_end = b_start + b.length

    if (a_start >= b_start and a_start <= b_end):
        return True
    if (a_end >= b_start and a_end <= b_end):
        return True
    if (b_start >= a_start and b_start <= a_end):
        return True
    if (b_end >= a_start and b_end <= a_end):
        return True
    return False


def seedQ(cands, sequence, min_tetrads):
    g = min_tetrads
    starts = queue.Queue()
    done = False

    while (not done):
        getStartingPoints(starts, sequence, g)
        done = True if (starts.qsize() == 0) else False
        while (not starts.empty()):
            cands.put(G4Candidate(sequence, g, starts.get()))
        g += 1

    # for i in (list(cands.queue)):
    #     print(i.start)
    #     print(i.numTetrads)
    #     print(i.y1)
    #     print(i.y2)
    #     print(i.y3)
    #     print(i.length)
    #     print(i.sequence)


def getStartingPoints(starts, sequence, g):
    tstring = ""
    for i in range(g):
        tstring += "G"

    p = 0
    done = False
    while(not done):
        p = sequence.find(tstring, p)
        if (p >= 0):
            starts.put(p)
        else:
            done = True
        p += 1


def belongsin(g4, family):
    for qgrs in family:
        if overlapped(g4, qgrs):
            return True
    return False


def find(sequence, overlaps, min_tetrads, min_score):
    raw_g4s = []
    cands = queue.Queue()
    seedQ(cands, sequence, min_tetrads)
    while(not cands.empty()):
        # print(cands.qsize())
        # print(candi.sequence)
        # print(candi.numTetrads)
        # print(candi.start)
        # print("done")
        cand = cands.get()
        # cand = G4Candidate(candi.sequence, candi.numTetrads, candi.start)
        # print(cand.complete())
        if (cand.complete()):
            if (cand.viable(min_score)):
                g = G4(cand)
                raw_g4s.append(g)
        else:
            expanded = queue.Queue()
            cand.expand(expanded)
            # ys = queue.Queue()
            # cand.findLoopLengthsFrom(ys, cand.cursor())
            # while (not ys.empty()):
            #     y = ys.get()
            #     candid = G4Candidate(
            #         cand.sequence, cand.numTetrads, cand.start)
            #     candid.y1 = cand.y1
            #     candid.y2 = cand.y2
            #     candid.y3 = cand.y3
            #     if cand.y1 < 0:
            #         candid.y1 = y
            #     elif cand.y2 < 0:
            #         candid.y2 = y
            #     elif cand.y3 < 0:
            #         candid.y3 = y
            #     if (candid.partialLength() <= cand.maxLength):
            #         expanded.put(candid)
            # print(expanded.get().y3)
            while(not expanded.empty()):
                cands.put(expanded.get())

    # raw_g4s.sort()
    fams = [[]]
    while(not (not raw_g4s)):
        g = raw_g4s[0]
        del raw_g4s[0]
        newFam = True
        for family in fams:
            if (belongsin(g, family)):
                family.append(g)
                newFam = False
        if newFam:
            f = []
            f.append(g)
            fams.append(f)

    g4s = []

    for family in fams:
        highest = 0
        final = G4(G4Candidate("", 2, 0))
        for qgrs in family:
            if qgrs.gscore > highest:
                final = qgrs
                highest = qgrs.gscore

        if overlaps:
            for qgrs in family:
                if(not final.isequal(qgrs)):
                    final.overlaps.append(qgrs)
        g4s.append(final)
    return g4s


if __name__ == '__main__':

    sequence = "GGTCTGGAGGAGGCT"
    # sequence = "GGGCCCCGGGGGGGGGGG"
    # sequence = "GGTCTGGAGGAGGCTCTCGGGGCCCCAACGGTTTGGACTTGAGTAGG"
    # sequence = "TTTTGATTGACCTCCTCTCTGGTCTGGAGGAGGTCAAATTGGAGTTGCAATTCTACTTT"
    overlaps = False
    tetrads = 2
    gscore = 17

    # pos_length = math.log10(len(sequence))+2
    results = find(sequence, overlaps, tetrads, gscore)
    for i in results:
        print(i.start)
        print(i.tetrads)
        print(i.tetrad1)
        print(i.tetrad2)
        print(i.tetrad3)
        print(i.tetrad4)
        print(i.y1)
        print(i.y2)
        print(i.y3)
        print(i.length)
        print(i.gscore)
        print(i.sequence)
        print(i.overlaps)
