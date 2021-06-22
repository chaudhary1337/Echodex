# input: [('tag', 5), ...]
def print_tags(data, color):
    html = f"""
    <div>
        <style>
        .tagbox {{
        font-family: "IBM Plex Sans", sans-serif;
        border-radius: 25px;
        background-color:#ffffff;
        border: 1px solid #ccc;
        margin:0px 10px 10px 0px;
        line-height: 200%;
        padding:3px 0 3px 12px; 
        }}

        
        .tagbox a, .tagbox a:visited, .tagbox a:active 
        {{ 
        text-decoration:none;
        }}
        
        .tagcount {{
        font-family: "IBM Plex Sans", sans-serif;
        border-radius: 0px;
        background-color:{color};
        color:black;
        position: relative;
        padding:4px;
        }}
        </style>
    
    """

    text = ""
    for tag, count in data:
        text += f"""
            <span class="tagbox">
                {tag}
                <span class="tagcount">{count}</span>
            </span>
        """

    html = html + text + "</div>"
    return html


# print(get_tags([("mayank", 5), ("is", 3), ("a", 9), ("whore", 6)]))
