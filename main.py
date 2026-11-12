# -----------------------------
# WEBSITE RELEASE SETTINGS
# -----------------------------

set_website_title("AeroLab Aircraft Designer")

set_site_information(
    author="Your Name",
    description=(
        "AeroLab is an educational aircraft design application. "
        "Users can enter aircraft measurements, calculate performance "
        "estimates, and compare saved aircraft designs."
    ),
    sources="Drafter documentation and aircraft design research.",
    planning=(
        "The repository includes brainstorming-worksheet.pdf "
        "and design-worksheet.pdf."
    ),
    links=[
        "https://github.com/alexnic-hue/AeroLab"
    ]
)

# Let the website fill the browser window.
set_website_framed(False)

# Hide the debug panel for the published website.
hide_debug_information()


# -----------------------------
# REPLACEMENT CSS INSIDE make_page
# -----------------------------

css = """
body {
    background: linear-gradient(
        rgba(255, 255, 255, 0.86),
        rgba(220, 234, 245, 0.95)
    );
    color: #172536;
}

p {
    margin-top: 4px;
    margin-bottom: 4px;
    line-height: 1.15;
    color: #172536;
}

h1, h2, h3 {
    margin-top: 8px;
    margin-bottom: 5px;
    line-height: 1.2;
    color: #172536;
}

hr {
    margin-top: 6px;
    margin-bottom: 6px;
}

button {
    margin-top: 2px;
    margin-bottom: 2px;
}
"""
