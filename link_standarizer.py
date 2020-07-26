import urllib.parse
import re


def wikilink_to_mdlink(wikilink):
    # Convert wiki style embedded images (e.g. Obsidian app) ![[image nice.jpg]] and links [[linked file]] to
    # compatible markdown ![[]](image%20nice.jpg)
    #
    # The trick here is that with double brackets we get compatibility for both wiki-style linkers (1writer,
    # obsidian for example) and standard markdown editors such as Typora.
    #
    # So, [[linked_file]] and [[linked_file]](linked_file) works on both systems. The only catch is that the rendered
    # view will show links inside single brackets - not big deal for me.

    # Extract the link
    groups = re.search('\[\[(.*)\]\]', wikilink)
    if groups:
        # Proper wikilink
        filename = groups.group(1)
    else:
        # Something went wrong
        return False

    # Check if its a link to another md note
    groups = re.search('.*\..*', filename)
    if not groups:
        # Add ".md" to the filename
        filename += ".md"

    # URL-encode it
    urlencoded_filename = urllib.parse.quote(filename)
    #    urllib.parse(filename)

    # Now build the markdown link
    mdlink = wikilink + "(" + urlencoded_filename + ")"

    return mdlink

def mdlink_to_wikilink(mdlink):
    # If title is not double-bracketed, add another pair of brackets and change title to filename for compatibility

    # Get parts of the mdlink
    regex = re.compile(r""""
        ^           # Line begin anchor
        (!)?        # 1 Embedded
        \[(.*)\]    # 2 Title
        \((.*\/)?   # 3 Optional path
        (.*)\)      # 4 filename
        $           # Line end anchor
        """, re.X)

    # groups = regex.search(mdlink)
    groups = re.search('^(!)?\[(.*)\]\((.*\/)?(.*)\)$', mdlink)
    if not groups:
        # Something went wrong
        return False
    else:
        if groups.group(1):
            embedded = groups.group(1)
        else:
            embedded = ''

        title = groups.group(2)

        if groups.group(3):
            path = groups.group(3)
        else:
            path = ''

        filename = groups.group(4)


    # Check if title is already double-bracketed
    groups = re.search('\[.*\].*', title)
    if not groups:
        # Add another pair of brackets
        title = "[" + title + "]"

    wikilink = embedded + "[" + title + "]" + "(" + path + filename + ")"

    return wikilink