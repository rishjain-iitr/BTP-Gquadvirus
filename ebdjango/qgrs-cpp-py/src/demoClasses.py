import math
import queue


class Snake:
    def __init__(self, name1, age1):
        self.name = name1
        self.age = age1
    y1 = "here"

    def t1(self):
        print(self.name)
        return (self.age)

    def t2(self):
        return (self.t1()+self.age)


class Stripped(Snake):

    def fin(self):
        print(Snake.t1(self))
        pass


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
        gavg = float((abs(self.y1-self.y2) + abs(self.y2 -
                                                 self.y3) + abs(self.y1-self.y3))/3.0)
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
        length = self.numTetrads * 4
        # add the minimum loops left
        if (self.y1 >= 0 and self.y2 < 0):
            # only hte first loop is known
            if (self.y1 == 0):
                # other two must be at least 2
                length += 2
            else:
                length += 1
        elif(self.y2 >= 0 and self.y3 < 0):
            # first two loop lengths are known
            if(self.y1 == 0 or self.y2 == 0):
                length += 1
        # add the current loops
        if (self.y1 > 0):
            length += self.y1
        if (self.y2 > 0):
            length += self.y2
        if (self.y3 > 0):
            length += self.y3

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
                if (y >= self.minAcceptableLoopLength() and (p-self.start+len(self.tstring)-1) < self.maxLength):
                    ys.put(y)
                else:
                    done = True
            else:
                done = True
            p += 1

    def expand(self, cands):
        ys = queue.Queue()
        self.findLoopLengthsFrom(ys, self.cursor())
        while (not ys.empty()):
            y = ys.get()
            cand = G4Candidate(self.sequence, self.numTetrads, self.start)
            cand.y1 = self.y1
            cand.y2 = self.y2
            cand.y3 = self.y3
            if self.y1 < 0:
                cand.y1 = y
            if self.y2 < 0:
                cand.y2 = y
            if self.y3 < 0:
                cand.y3 = y
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


cand = G4Candidate("GGGGATCCGGGATAGGATTCGGAGGCCCTGGGCCCTGGGCCCCGG", 3, 0)
cand2 = G4(cand)
print(cand2.tetrad1)
snake = Snake("Python", 10)
snake2 = Stripped("Python", 20)
print(snake2.fin())
