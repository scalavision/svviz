import collections
import logging
import time

class ReadSet(object):
    def __init__(self):
        self.reads = []
        self.strings = []
    def add(self, newread):
        if str(newread) not in self.strings:
            self.strings.append(str(newread))
            self.reads.append(newread)

class PairFinder(object):
    def __init__(self, regions, sam, minmapq=-1, pair_minmapq=-1, is_paired=True, include_supplementary=False,
                 max_reads=None):
        self.include_supplementary = include_supplementary
        self.regions = regions
        self.sam = sam
        self.minmapq = minmapq
        self.readsByID = collections.defaultdict(ReadSet)
        self.tomatch = set()
        self.supplementaryAlignmentsFound = False
        self.maxReads = max_reads

        for region in self.regions:
            self.tomatch.update(self.loadRegion(region.chr(), region.start(), region.end()))

        if is_paired:
            logging.debug("  To-match: {}, min-mapq: {}".format(len(self.tomatch), self.minmapq))
            self.domatching()


        matchIDs = set(read.qname for read in self.tomatch)
        self.matched = [self.readsByID[id_].reads for id_ in matchIDs]

        if pair_minmapq > 0:
            self.matched = [self.readsByID[id_].reads for id_ in matchIDs 
                            if max(read.mapq for read in self.readsByID[id_].reads)>=pair_minmapq]

        logging.info("  reads with missing pairs: {}".format(sum(1 for x in self.matched if (len(x)<2 and x[0].is_paired))))

    def domatching(self):
        t0 = None

        for i, read in enumerate(self.tomatch):#[:150]):
            if i % 1000 == 0:
                if t0 is None:
                    t0 = time.time()
                    elapsed = "Finding mate pairs..."
                else:
                    t1 = time.time()
                    elapsed = t1-t0
                    t0 = t1
                logging.info("  {} {} {}".format(i, len(self.tomatch), elapsed))
            if len(self.readsByID[read.qname].reads) < 2:
                self.findmatch(read)


    def findmatch(self, read):
        if read.is_paired and read.rnext >= 0:
            chrom = self.sam.getrname(read.rnext)
            self.loadRegion(chrom, read.pnext, read.pnext+1, mates=True)


    def loadRegion(self, chrom, start, end, mates=False):
        ## TODO: should bail here if we're beyond self.maxReads and pair_minmapq is not 
        ## being used

        count = self.sam.count(chrom, start, end)
        reads = self.sam.fetch(chrom, start, end)

        if count > 1e5:
            if mates:
                logging.warn("  LOTS OF READS IN MATE-PAIR REGION: {}:{}-{} count={:,}".format(chrom, start, end, count))
            else:
                logging.warn("  LOTS OF READS IN BREAKPOINT REGION: {}:{}-{} count={:,}".format(chrom, start, end, count))

        goodReads = []
        for i, read in enumerate(reads):
            if i%1000000 == 0 and count > 5e6:
                logging.debug("   > {} of {}".format(i, count))

            if read.mapq >= self.minmapq and not read.is_secondary and not read.is_duplicate:
                if (read.flag & 0x800) != 0 and not self.include_supplementary:
                    self.supplementaryAlignmentsFound = True
                    continue
                # beforeString = str([(rr.qname, rr.flag) for rr in self.readsByID[read.qname].reads]) +str((read.qname, read.flag))
                self.readsByID[read.qname].add(read)
                goodReads.append(read)

                # if len(self.readsByID[read.qname].reads) > 1:
                #     print ""
                #     print "\n".join(map(str, self.readsByID[read.qname].reads))
                #     print "*"*200

        return goodReads