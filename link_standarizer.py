import urllib.parse
import re


def wikilink_to_mdlink(wikilink):
    # Convert wiki style embedded images (e.g. Obsidian app) ![[image nice.jpg]] and links [[linked file]] to
    # compatible markdown ![[]](image%20nice.jpg)
    #
    # The trick here is that with double brackets we get compatibility for both wiki-style linkers (1writer,
    # Obsidian for example) and standard markdown editors such as Typora.
    #
    # So, [[linked_file]] and [[linked_file]](linked_file) works on both systems. The only catch is that the rendered
    # view will show links inside single brackets - not big deal for me.

    # First, confirm this is a wikilink
    var_type = link_type(wikilink)

    if var_type == 'wikilink':
        wikilink_dictionary = wikilink_split(wikilink)
        filename = wikilink_dictionary['wikilink']

        # Check if its a link to another md note
        groups = re.search(r'.*\..*', filename)
        if not groups:
            # Add ".md" to the filename
            filename += ".md"

        # URL-encode it
        urlencoded_filename = urllib.parse.quote(filename)

        # Now build the markdown link
        mdlink = wikilink + "(" + urlencoded_filename + ")"

        return mdlink
    else:
        return False


# Split wikilink in it's parts
def wikilink_split(wikilink):
    # Extract the link
    groups = re.search(r'\[\[(.*)\]\]', wikilink)

    if groups:
        wikilink_dictionary = {
            'wikilink': groups.group(1)
        }

        return wikilink_dictionary
    else:
        # Something went wrong
        return False


# Split markdown links in it's parts, else return False
def mdlink_split(mdlink):
    # First check if it is an internal link or url link
    mdlink_dictionary = internal_mdlink_split(mdlink)

    if mdlink_dictionary:
        # Now see if it's URL
        url_split = urllib.parse.urlparse(mdlink_dictionary['Path'])

        if url_split.scheme is not '':
            mdlink_dictionary['Url'] = mdlink_dictionary['Path'] + mdlink_dictionary['Filename']
            del mdlink_dictionary['Filename']
            del mdlink_dictionary['Path']

        return mdlink_dictionary
    else:
        return False


# Split markdown INTERNAL links
def url_mdlink_split(mdlink):
    # Regex pattern to split markdown internal links in it's parts
    regex = re.compile("""
        ^           # Line begin anchor
        (!)?        # 1 Optional Embedded
        [(.*)]    # 2 Optional Title
        ((.*/)?   # 3 Optional path
        (.*))      # 4 Filename
        $           # Line end anchor
        """, re.X)

    search = regex.search(mdlink)

    # If regex pattern matches the input string
    if search:

        mdlink_dictionary = {
            'Embedded': search.group(1),
            'Title': search.group(2),
            'Path': search.group(3),
            'Filename': search.group(4)
        }

        # Clean optional components
        if not mdlink_dictionary['Embedded']:
            mdlink_dictionary['Embedded'] = ''

        if not mdlink_dictionary['Title']:
            mdlink_dictionary['Title'] = ''

        if not mdlink_dictionary['Path']:
            mdlink_dictionary['Path'] = ''

        return mdlink_dictionary

    # mdlink was not detected on the input string
    else:
        return False


# Split markdown INTERNAL links
def internal_mdlink_split(mdlink):
    # Regex pattern to split markdown internal links in it's parts
    regex = re.compile(r"""
        ^           # Line begin anchor
        (!)?        # 1 Optional Embedded
        \[(.*)\]    # 2 Optional Title
        \((.*/)?   # 3 Optional path
        (.*)\)      # 4 Filename
        $           # Line end anchor
        """, re.X)

    search = regex.search(mdlink)

    # If regex pattern matches the input string
    if search:

        mdlink_dictionary = {
            'Embedded': search.group(1),
            'Title': search.group(2),
            'Path': search.group(3),
            'Filename': search.group(4)
        }

        # Clean optional components
        if not mdlink_dictionary['Embedded']:
            mdlink_dictionary['Embedded'] = ''

        if not mdlink_dictionary['Title']:
            mdlink_dictionary['Title'] = ''

        if not mdlink_dictionary['Path']:
            mdlink_dictionary['Path'] = ''

        return mdlink_dictionary

    # mdlink was not detected on the input string
    else:
        return False


# If title is not double-bracketed, add another pair of brackets and change title to filename for compatibility
def mdlink_to_wikilink(mdlink):
    # Check this is an internal mdlink
    var_type = link_type(mdlink)

    if var_type == 'internalmdlink':
        # Get parts of mdlink
        mdlink_dictionary = mdlink_split(mdlink)

        if not mdlink_dictionary:
            # Something went wrong
            return False

        else:
            # Check if title is already double-bracketed
            groups = re.search(r'\[.*\].*', mdlink_dictionary['Title'])
            if not groups:
                # Add another pair of brackets
                mdlink_dictionary['Title'] = "[" + mdlink_dictionary['Title'] + "]"

            wikilink = mdlink_dictionary['Embedded'] + "[" + mdlink_dictionary['Title'] + "]" + "(" + mdlink_dictionary[
                'Path'] + mdlink_dictionary['Filename'] + ")"

            return wikilink

    else:
        return False


# Analyze the string and see if it's a link, and which type. Returns either:
# 'urlmdlink': Markdown url link i.e. [title](url)
# 'internalmdlink': Markdown internal link ie. [titile](path/to/mdfile.md)
# 'ahreflink': HTML formatted link i.e. <a href='url'>title</a>
# 'wikilink': Extended markdown wililink i.e. [[mdfile]] (without .md extension)
# False: No link detected
def link_type(string):
    # First check if it is an internal link or url link
    mdlink_dictionary = internal_mdlink_split(string)

    if mdlink_dictionary:
        url_split = urllib.parse.urlparse(mdlink_dictionary['Path'])

        if url_split.scheme is not '':
            return 'urlmdlink'
        else:
            return 'internalmdlink'

    # Not mdlink. Check if it's wikilink
    else:
        wikilink_dictionary = wikilink_split(string)

        if wikilink_dictionary:
            return 'wikilink'

    return False
