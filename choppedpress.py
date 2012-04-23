# -*- coding: utf-8 -*-


import os
import sys

try:
    from lxml import etree
except ImportError:
    print "Please install lxml and try again: http://codespeak.net/lxml/"
    sys.exit(-1)

from optparse import OptionParser

# This is the default xml tag for wordpress
WP_TAG = "/rss/channel/item"
OUTFILE = "outfile"
CHUNKSIZE = 2
TMPFILE = "/tmp/template.xml"

# Function found on ActiveState Code
# Licensed under the PSF license
# http://code.activestate.com/recipes/425397-split-a-list-into-roughly-equal-sized-pieces/
def split_seq(seq, size):
    newseq = []
    splitsize = 1.0/size*len(seq)
    for i in range(size):
            newseq.append(seq[int(round(i*splitsize)):int(round((i+1)*splitsize))])

    return newseq

def chopit(xmlfile, outfile=OUTFILE, xmltag=WP_TAG, chunksize=CHUNKSIZE):
    parser = etree.XMLParser(resolve_entities=False, encoding="utf-8", strip_cdata=False)
    doc = etree.parse(xmlfile, parser)

    matches = doc.xpath(xmltag)
    print "Found %s blog posts!" % len(matches)
    matcheslist = split_seq(matches, chunksize)

    channel = doc.getroot().find('channel')

    # Create an empty wordpress xml file
    for e in matches:
        channel.remove(e)
    doc.write(TMPFILE, encoding="utf-8", method="xml", pretty_print=True)

    # Now, create smaller wordpress xml files
    ctr = len(matcheslist)
    print "Breaking WordPress XML into %s smaller files." % ctr
    for entities in matcheslist:
        doc = etree.parse(TMPFILE)
        channel = doc.getroot().find('channel')
        for entity in entities:
            channel.append(entity)

        output = '%s%03d.xml' % (outfile, ctr)
        doc.write(output, encoding='utf-8', method="xml", pretty_print=True)
        print " - File %s has %s posts." % (output, len(entities))
        ctr -= 1
    print "Done!"

def main():

    description = "ChoppedPress lets you split the WordPress XML export file " \
    "into smaller files that can be used to import your posts, comments, tags" \
    " and categories into a new WordPress installation."

    usage = "Usage:  %prog <INFILE> [[<OUTFILE>] [<TAG>] [<NUMBER>]]"
    epilog = "Constructive comments and feedback can be sent to ogmaciel at gnome dot org."
    version = "%prog version 0.1"

    parser = OptionParser(usage=usage, description=description, epilog=epilog, version=version)
    parser.add_option('-i', '--infile', dest='infile', metavar='<FILE>', help='The XML file generated by WordPress')
    parser.add_option('-o', '--outfile', dest='outfile', default='out', metavar='<FILE>', help='The name for the smaller XML files. [default: %default]')
    parser.add_option('-t', '--tag', dest='tag', default='/rss/channel/item', help='The XML tag that represents your data. [default: %default]')
    parser.add_option('-n', '--number', dest='number', default=2, type=int, help='How many new files should be generated. [default: %default]')

    # Verify arguments
    (opts, args) = parser.parse_args()

    if not opts.infile:
        parser.print_help()
        sys.exit(-1)

    chopit(opts.infile, opts.outfile, opts.tag, opts.number)

if __name__ == "__main__":
    main()
