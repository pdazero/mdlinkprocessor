import urllib
from urllib import parse

import re
from bs4 import BeautifulSoup


## Convert internal mdlinks to standarizedinternalmdlink
def internal_mdlink_to_standarizedinternal_mdlink(mdlink):
    """
    If title is not double-bracketed, add another pair of brackets and change title to filename for compatibility.

    i.e.: [Title](some%20file.md) -> [[Some File]](some%20file.md)

    :string string: Expects a link from a markdown file

    :return: returns a wiki-linkified mdlink
    """

    # Check this is an internal mdlink
    var_type = link_type(mdlink)

    if var_type == 'internalmdlink':
        # Get parts of mdlink
        mdlink_dictionary = mdlink_split(mdlink)

        if not mdlink_dictionary:
            # Something went wrong
            return False

        else:
            # Check if title is already double-bracketed, in that case leave it as is
            groups = re.search(r'\[.*\].*', mdlink_dictionary['Title'])
            if not groups:
                # Add another pair of brackets and set up url decoded filename as title
                mdlink_dictionary['Title'] = "[" + urllib.parse.unquote(mdlink_dictionary['Filename']) + "]"

            # Decode and encode filename to make sure its encoded
            mdlink_dictionary['Filename'] = urllib.parse.quote(urllib.parse.unquote(mdlink_dictionary['Filename']))
            wikilink = mdlink_dictionary['Embedded'] + "[" + mdlink_dictionary['Title'] + "]" + "(" + mdlink_dictionary[
                'Path'] + mdlink_dictionary['Filename'] + ")"

            return wikilink

    else:
        return False

# Convert wiki style embedded images (e.g. Obsidian app) ![[image nice.jpg]] and links [[linked file]] to
# compatible markdown ![[]](image%20nice.jpg)
def wikilink_to_mdlink(wikilink):
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

        if url_split.scheme != '':
            mdlink_dictionary['Url'] = mdlink_dictionary['Path'] + mdlink_dictionary['Filename']
            del mdlink_dictionary['Filename']
            del mdlink_dictionary['Path']

        return mdlink_dictionary
    else:
        return False


# Split a href link
# 'Title'
# 'Url'
# 'Class'
def ahreflink_split(ahreflink):
    # First check it's the correct link type
    var_type = link_type(ahreflink)

    if var_type == 'ahreflink':
        soup = BeautifulSoup(ahreflink, 'html.parser')

        a_soup = soup.find('a')

        ahreflink_dictionary = {
            'Title': a_soup.string,
            'Url': a_soup.get('href'),
            'Class': a_soup.get('class')
        }

        # Clean optional components
        if not ahreflink_dictionary['Class']:
            ahreflink_dictionary['Class'] = ''

        return ahreflink_dictionary
    else:
        return False


# Split markdown INTERNAL links
# 'Embedded': Optional exclamation mark
# 'Title'
# 'Path'
# 'Filename'
def internal_mdlink_split(mdlink):
    # Regex pattern to split markdown internal links in it's parts
    regex = re.compile(r"""
        ^           # Line begin anchor
        (!)?        # 1 Optional Embedded
        \[(.*)\]    # 2 Optional Title
        \((.*/)?    # 3 Optional path
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


def link_type(string: str) -> str:
    """
    Analyze the string and see if it's a link, and which type. Returns either:
       - **'urlmdlink'**: Markdown url link i.e. [title](url)
       - **'internalmdlink'**: Markdown internal link ie. [title](path/to/mdfile.md)
       - **'standardizedinternalmdlink'**: Markdown wikilink-compatible internal link i.e. [[mdfile]](path/to/mdfile.md)
       - **'ahreflink'**: HTML formatted link i.e. <a href='url'>title</a>
       - **'wikilink'**: Extended markdown wikilink without .md extension i.e. [[mdfile]]
       - **False**: No link detected

    :string string: Expects a link from a markdown file

    :return: returns link type
    """
    # First check if it is an internal link or url link
    mdlink_dictionary = internal_mdlink_split(string)

    if mdlink_dictionary:
        url_split = urllib.parse.urlparse(mdlink_dictionary['Path'])

        if url_split.scheme != '':
            return 'urlmdlink'
        else:
            # See if title is a wikilink
            if not wikilink_split('['+mdlink_dictionary['Title']+']'):
                return 'internalmdlink'
            else:
                return 'standardizedinternalmdlink'

    # Not mdlink. Check if it's wikilink
    else:
        wikilink_dictionary = wikilink_split(string)

        if wikilink_dictionary:
            return 'wikilink'
        else:
            # Check if its an ahref link
            soup = BeautifulSoup(string, 'html.parser')

            if soup.find('a'):
                return 'ahreflink'

    return False
