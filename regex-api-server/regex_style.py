import re
import html
from utils.debug_utils import debug_log

def create_matches_html(regex, text, colors):
    pattern = re.compile(regex, re.IGNORECASE | re.MULTILINE)

    i = 0;
    output = ""
    m = None
    for m in pattern.finditer(text):
        output += "".join([text[i:m.start()],
                           "<strong><span style='background-color:%s; font-weight:100;'>" % colors[m.lastindex - 1],
                           text[m.start():m.end()],
                           "</span></strong>"])

        i = m.end()

    if m is not None:
        output += text[m.end():]

    output = mark_html_div(output)

    return output


def create_html_span_text(text):
    return "".join(["<span font-weight:100;'>", text, "</span>"])

def create_html_styled_text(text, color, title=""):
    return "".join([
        "<span title='%s' style='background-color:%s; font-weight:100;'>" % (title, color),
        text,
        "</span>"
    ])



def create_html_styled_groups(text, match, groups_dict, colors=None):
    # debug_log("Group Coloring")

    groups = match.groups()

    reverse_group_dict = {v:k for k,v in groups_dict.items()}

    # group[0] has the full match
    output=""
    offset = match.start()
    index = 0
    for index in range(1, len(groups)+1):
        # debug_log("Group Index[{},{}]:{}".format(index, match.span(index), match.group(index)))

        group_start, group_end = match.span(index)
        group_text = match.group(index)
        title = reverse_group_dict[index] if index in reverse_group_dict else str(index)
        plain_text = text[offset:group_start]
        output += "".join([create_html_span_text(html.escape(plain_text)),
                           create_html_styled_text(html.escape(group_text), colors[index % 5], title)
                           ])
        offset = group_end

    if index > 0:
        plain_text = text[offset:match.end()]
        output += create_html_span_text(html.escape(plain_text))
    else:
        match_text = match.group(0)
        output = create_html_styled_text(html.escape(match_text), colors[index % 5], "Match")

    for key,value in groups_dict.items():
        # debug_log("Group[{},{}]:{}".format(key, match.span(key), match.group(key)))
        pass

    return output


def create_html_styled_matches(regex, text, colors, title="Match"):
    pattern = re.compile(regex, re.IGNORECASE | re.MULTILINE)

    # Shows named groups with index. The unnamed groups are not are, they can be used by index
    groups_dict = dict(pattern.groupindex)

    offset = 0
    output = ""
    match = None
    index = 0
    for match in pattern.finditer(text):
        matched_colored_text = create_html_styled_groups(text, match, groups_dict, colors)

        plain_text = text[offset:match.start()]
        output += "".join([create_html_span_text(html.escape(plain_text)),
                           create_html_styled_text(matched_colored_text, colors[6], "{}[{}]".format(title, index))
                           ])
        offset = match.end()
        index += 1

    if match is not None:
        plain_text = text[offset:]
        output += create_html_span_text(html.escape(plain_text))
    else:
        output = html.escape(text)

    return output


def mark_html_div(text, flag_white_space_pre=True):
    line_regex = "^(?P<line>.*)$"
    # This line handling method should be simplified. Avoid regex
    pattern = re.compile(line_regex, re.MULTILINE)
    lines = pattern.findall(text)

    white_space_pre=""
    if flag_white_space_pre:
        white_space_pre = "white-space:pre; "
    new_line = "<br/>"

    html_str = "<div style=\"{}font-family:'Monaco'; font-size: 14px; font-weight:100; text-align:left\">".format(white_space_pre)
    num_lines = len(lines)
    for index in range(0, num_lines):
        line = lines[index]
        #Since we use beautiful soup
        if line != "":
            html_str += line
        
        # We ensure that last line does not have a <br/>
        if (index < num_lines - 1):
            html_str += new_line

        index += 1
    html_str += "</div>"

    return html_str


def create_colored_html_div(text, etrade_regex, colors):
    html_str = create_html_styled_matches(etrade_regex, text, colors, title="Trade")
    html_str = mark_html_div(html_str)
    return html_str
