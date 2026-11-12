
from dataclasses import dataclass, field
from drafter import *

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

add_website_file("aircraft-background.jpg")
set_website_framed(False)
hide_debug_information()


# -----------------------------
# DATA CLASSES
# -----------------------------

@dataclass
class Plane:
    name: str
    wingspan: float
    chord: float
    weight: float
    speed: float
    wing_area: float
    aspect_ratio: float
    lift: float
    cg: float
    score: float


@dataclass
class State:
    planes: list = field(default_factory=list)
    current_plane: dict = field(default_factory=dict)
    current_page: str = "home"
    plane_number: int = 1


# -----------------------------
# STARTING STATE
# -----------------------------

def make_state():
    return State(
        planes=[],
        current_plane={
            "name": "My Aircraft",
            "wingspan": 10.0,
            "chord": 1.5,
            "weight": 100.0,
            "speed": 20.0
        },
        current_page="home",
        plane_number=1
    )


# -----------------------------
# CALCULATIONS
# -----------------------------

def safe_float(value):
    try:
        number = float(value)

        if number < 0:
            return 0.0

        return number

    except (ValueError, TypeError):
        return 0.0


def calculate_plane(name, wingspan, chord, weight, speed):
    wingspan = safe_float(wingspan)
    chord = safe_float(chord)
    weight = safe_float(weight)
    speed = safe_float(speed)

    wing_area = wingspan * chord

    if wing_area > 0:
        aspect_ratio = (wingspan ** 2) / wing_area
    else:
        aspect_ratio = 0

    lift = 0.5 * 1.225 * (speed ** 2) * wing_area
    cg = chord * 0.25

    if weight > 0:
        score = aspect_ratio * 10 + lift / weight
    else:
        score = aspect_ratio * 10

    return Plane(
        name=name,
        wingspan=wingspan,
        chord=chord,
        weight=weight,
        speed=speed,
        wing_area=wing_area,
        aspect_ratio=aspect_ratio,
        lift=lift,
        cg=cg,
        score=score
    )


def plane_summary(plane):
    return [
        "Aircraft: " + plane.name + "\n",
        "Wingspan: " + str(round(plane.wingspan, 2)) + "\n",
        "Chord: " + str(round(plane.chord, 2)) + "\n",
        "Weight: " + str(round(plane.weight, 2)) + "\n",
        "Speed: " + str(round(plane.speed, 2)) + "\n",
        "Wing Area: " + str(round(plane.wing_area, 2)) + "\n",
        "Aspect Ratio: " + str(round(plane.aspect_ratio, 2)) + "\n",
        "Estimated Lift: " + str(round(plane.lift, 2)) + "\n",
        "Center of Gravity: " + str(round(plane.cg, 2)) + "\n",
        "Design Score: " + str(round(min(100, plane.score), 2)) + "\n"
    ]


# -----------------------------
# DYNAMIC AIRCRAFT ILLUSTRATION
# -----------------------------

def aircraft_illustration(wingspan, chord):
    wingspan = safe_float(wingspan)
    chord = safe_float(chord)

    wing_half_span = 55 + min(wingspan, 25) * 4
    wing_depth = 25 + min(chord, 5) * 13

    wing_front = 145 - wing_depth / 2
    wing_back = 145 + wing_depth / 2

    left_tip = 250 - wing_half_span
    right_tip = 250 + wing_half_span

    left_inner_tip = left_tip + 12
    right_inner_tip = right_tip - 12

    left_front = wing_front + 12
    right_front = wing_front + 12

    left_mark_x1 = left_tip + 20
    left_mark_x2 = left_tip + 30

    right_mark_x1 = right_tip - 20
    right_mark_x2 = right_tip - 30

    mark_front = wing_front + 15
    mark_back = wing_back - 10

    drawing = (
        '<rect x="0" y="0" width="500" height="400" '
        'rx="25" fill="#edf5fb"/>'

        '<circle cx="250" cy="195" r="155" '
        'fill="#dceaf5"/>'

        '<path d="M235 ' + str(wing_front) +
        ' L' + str(left_tip) + ' ' + str(left_front) +
        ' L' + str(left_inner_tip) + ' ' + str(wing_back) +
        ' L235 ' + str(wing_back) +
        ' Z" fill="#287db8" stroke="#17496d" stroke-width="4"/>'

        '<path d="M265 ' + str(wing_front) +
        ' L' + str(right_tip) + ' ' + str(right_front) +
        ' L' + str(right_inner_tip) + ' ' + str(wing_back) +
        ' L265 ' + str(wing_back) +
        ' Z" fill="#287db8" stroke="#17496d" stroke-width="4"/>'

        '<line x1="' + str(left_mark_x1) +
        '" y1="' + str(mark_front) +
        '" x2="' + str(left_mark_x2) +
        '" y2="' + str(mark_back) +
        '" stroke="#dceaf5" stroke-width="4"/>'

        '<line x1="' + str(right_mark_x1) +
        '" y1="' + str(mark_front) +
        '" x2="' + str(right_mark_x2) +
        '" y2="' + str(mark_back) +
        '" stroke="#dceaf5" stroke-width="4"/>'

        '<path d="M250 25 '
        'C230 65 232 110 237 155 '
        'L238 285 L250 345 L262 285 L263 155 '
        'C268 110 270 65 250 25 Z" '
        'fill="#ffffff" stroke="#24394b" stroke-width="4"/>'

        '<path d="M250 45 C232 65 240 95 250 105 '
        'C260 95 268 65 250 45 Z" '
        'fill="#38a5d6" stroke="#17496d" stroke-width="3"/>'

        '<path d="M250 115 L250 310" '
        'stroke="#9baab5" stroke-width="2" stroke-dasharray="6 6"/>'

        '<path d="M250 285 L180 320 L190 345 L250 330 Z" '
        'fill="#287db8" stroke="#17496d" stroke-width="4"/>'

        '<path d="M250 285 L320 320 L310 345 L250 330 Z" '
        'fill="#287db8" stroke="#17496d" stroke-width="4"/>'

        '<circle cx="250" cy="25" r="5" fill="#f29b38"/>'

        '<text x="250" y="385" text-anchor="middle" '
        'font-size="15" fill="#24394b">'
        'Top View Aircraft Design</text>'
    )

    return SVG(
        drawing,
        width=500,
        height=400
    )


# -----------------------------
# NAVIGATION
# -----------------------------

def make_navigation():
    return [
        Button("Home", "index"),
        " ",
        Button("Instructions", "instructions"),
        " ",
        Button("Aircraft Designer", "designer"),
        " ",
        Button("Saved Aircraft", "saved_planes"),
        " ",
        Button("Learn", "learn"),
        "\n"
    ]


# -----------------------------
# SHARED PAGE DESIGN
# -----------------------------

def make_page(state, title, content):
    page_content = []

    page_content.append(Header("AeroLab Aircraft Designer"))
    page_content.extend(make_navigation())
    page_content.append(HorizontalRule())
    page_content.append(Header(title))
    page_content.extend(content)

    javascript = """
    document.addEventListener("input", function(event) {
        const field = event.target;

        const allowedFields = [
            "wingspan",
            "chord",
            "weight",
            "speed"
        ];

        if (allowedFields.includes(field.id)) {
            if (field.value !== "" && Number(field.value) < 0) {
                field.value = "0";
            }
        }
    });
    """

    css = """
    body {
        background-image:
            linear-gradient(
                rgba(255, 255, 255, 0.86),
                rgba(255, 255, 255, 0.86)
            ),
            url("aircraft-background.jpg");

        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
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

    return Page(
        state,
        page_content,
        css=css,
        js=javascript
    )


# -----------------------------
# HOME PAGE
# -----------------------------

@route
def index(state: State) -> Page:
    state.current_page = "home"

    content = [
        Paragraph("Welcome to AeroLab Aircraft Designer!"),
        Paragraph(
            "Create your own aircraft design, calculate its "
            "performance, and compare your saved aircraft."
        ),
        Header("What You Can Do"),
        Paragraph("Design an aircraft using four measurements."),
        Paragraph("Calculate wing area, aspect ratio, and lift."),
        Paragraph("Save aircraft designs for later."),
        Paragraph("Compare the results of different designs."),
        Button("Start Designing", "designer"),
        "\n",
        Button("Read Instructions", "instructions")
    ]

    return make_page(state, "Home", content)


# -----------------------------
# INSTRUCTIONS PAGE
# -----------------------------

@route
def instructions(state: State) -> Page:
    state.current_page = "instructions"

    content = [
        Paragraph(
            "Use the Aircraft Designer page to enter measurements "
            "for your aircraft."
        ),
        Header("Measurements"),
        Paragraph(
            "Wingspan: The distance from one wingtip to the other."
        ),
        Paragraph(
            "Chord: The distance from the front of the wing "
            "to the back of the wing."
        ),
        Paragraph("Weight: The weight of the aircraft."),
        Paragraph("Speed: The speed of the aircraft."),
        Header("Calculations"),
        Paragraph("Wing Area = Wingspan multiplied by Chord."),
        Paragraph(
            "Aspect Ratio = Wingspan squared divided by Wing Area."
        ),
        Paragraph(
            "Estimated Lift = 0.5 multiplied by air density, "
            "speed squared, and wing area."
        ),
        Paragraph(
            "Center of Gravity is estimated as 25 percent "
            "of the chord."
        ),
        Paragraph(
            "The design score combines aspect ratio and estimated "
            "lift divided by weight. It is a simplified comparison "
            "score, not a real aircraft safety rating."
        ),
        Button("Start Designing", "designer")
    ]

    return make_page(state, "Instructions", content)


# -----------------------------
# AIRCRAFT DESIGNER PAGE
# -----------------------------

@route
def designer(state: State) -> Page:
    state.current_page = "designer"

    content = [
        Paragraph(
            "Enter your aircraft measurements below. "
            "Negative values will be changed to zero."
        ),

        Header("Aircraft Name"),
        TextBox(
            "name",
            state.current_plane.get("name", "My Aircraft")
        ),

        Header("Wingspan"),
        TextBox(
            "wingspan",
            state.current_plane.get("wingspan", 10.0),
            kind="number",
            id="wingspan"
        ),

        Header("Chord"),
        TextBox(
            "chord",
            state.current_plane.get("chord", 1.5),
            kind="number",
            id="chord"
        ),

        Header("Weight"),
        TextBox(
            "weight",
            state.current_plane.get("weight", 100.0),
            kind="number",
            id="weight"
        ),

        Header("Speed"),
        TextBox(
            "speed",
            state.current_plane.get("speed", 20.0),
            kind="number",
            id="speed"
        ),

        "\n",
        Button("Update Preview", "update_preview"),
        "\n",
        Button("Preview and Save Aircraft", "update_preview"),
        "\n",
        Button("Reset Measurements", "reset")
    ]

    return make_page(state, "Aircraft Designer", content)


# -----------------------------
# AIRCRAFT RESULTS / PREVIEW
# -----------------------------

@route
def update_preview(
    state: State,
    name: str,
    wingspan: str,
    chord: str,
    weight: str,
    speed: str
) -> Page:

    state.current_plane = {
        "name": name,
        "wingspan": safe_float(wingspan),
        "chord": safe_float(chord),
        "weight": safe_float(weight),
        "speed": safe_float(speed)
    }

    plane = calculate_plane(
        name,
        wingspan,
        chord,
        weight,
        speed
    )

    content = [
        Header("Aircraft Results:"),
        Paragraph("Here are the calculated results for your aircraft."),

        Paragraph(
            "Wing area: " + str(round(plane.wing_area, 2)) + " m²"
        ),

        Paragraph(
            "Aspect ratio: " + str(round(plane.aspect_ratio, 2))
        ),

        Paragraph(
            "Estimated lift: " + str(round(plane.lift, 2)) + " N"
        ),

        Paragraph(
            "Estimated center of gravity: "
            + str(round(plane.cg, 2)) + " m"
        ),

        Paragraph(
            "Design score: "
            + str(round(min(100, plane.score), 2)) + "/100"
        ),

        Button("Save this aircraft", "save_preview"),
        "\n",
        Button("Edit design", "designer"),

        "\n",
        Header("Your Aircraft Illustration:"),

        aircraft_illustration(
            plane.wingspan,
            plane.chord
        ),

        Paragraph(
            "Wingspan: " + str(round(plane.wingspan, 2)) + " m"
        ),

        Paragraph(
            "Chord: " + str(round(plane.chord, 2)) + " m"
        )
    ]

    return make_page(state, "Results", content)


# -----------------------------
# SAVE PREVIEW
# -----------------------------

@route
def save_preview(state: State) -> Page:
    current = state.current_plane

    plane = calculate_plane(
        current.get("name", "My Aircraft"),
        current.get("wingspan", 0),
        current.get("chord", 0),
        current.get("weight", 0),
        current.get("speed", 0)
    )

    content = [
        Paragraph("Review your aircraft before saving."),
        Header("Aircraft Summary")
    ]

    content.extend(plane_summary(plane))

    content.extend([
        "\n",
        Button("Confirm Save", "save_plane"),
        "\n",
        Button("Go Back", "designer")
    ])

    return make_page(state, "Save Aircraft", content)


# -----------------------------
# SAVE AIRCRAFT
# -----------------------------

@route
def save_plane(state: State) -> Page:
    current = state.current_plane

    plane = calculate_plane(
        current.get("name", "My Aircraft"),
        current.get("wingspan", 0),
        current.get("chord", 0),
        current.get("weight", 0),
        current.get("speed", 0)
    )

    state.planes.append(plane)
    state.plane_number += 1

    content = [
        Paragraph("Your aircraft has been saved!"),
        Header("Saved Aircraft"),
        Paragraph("Aircraft name: " + plane.name),
        Button("View Saved Aircraft", "saved_planes"),
        "\n",
        Button("Design Another Aircraft", "designer")
    ]

    return make_page(state, "Aircraft Saved", content)


# -----------------------------
# SAVED AIRCRAFT PAGE
# -----------------------------

@route
def saved_planes(state: State) -> Page:
    state.current_page = "saved_planes"

    content = []

    if len(state.planes) == 0:
        content.append(
            Paragraph("You have not saved any aircraft yet.")
        )

    else:
        content.append(
            Paragraph(
                "You have saved " + str(len(state.planes)) + " aircraft."
            )
        )

        for plane in state.planes:
            content.append(Header(plane.name))
            content.extend(plane_summary(plane))
            content.append(HorizontalRule())

        best_plane = state.planes[0]

        for plane in state.planes:
            if plane.score > best_plane.score:
                best_plane = plane

        content.append(Header("Best Saved Aircraft"))

        content.append(
            Paragraph(
                best_plane.name + " is your best saved aircraft "
                "because it has the highest design score."
            )
        )

        content.append(
            Paragraph(
                "Its design score is "
                + str(round(best_plane.score, 2))
                + "."
            )
        )

        aspect_points = best_plane.aspect_ratio * 10

        if best_plane.weight > 0:
            lift_weight_points = best_plane.lift / best_plane.weight
        else:
            lift_weight_points = 0

        content.append(Header("Why This Aircraft Is Best"))

        content.append(
            Paragraph(
                "AeroLab calculates the design score using two parts: "
                "aspect ratio multiplied by 10, and estimated lift "
                "divided by weight. The aircraft with the highest "
                "combined score ranks first."
            )
        )

        content.append(
            Paragraph(
                "Aspect Ratio: "
                + str(round(best_plane.aspect_ratio, 2))
                + ". This contributes "
                + str(round(aspect_points, 2))
                + " points to the score. A higher aspect ratio "
                "adds more points."
            )
        )

        content.append(
            Paragraph(
                "Lift-to-Weight Ratio: "
                + str(round(lift_weight_points, 2))
                + ". The aircraft has an estimated lift of "
                + str(round(best_plane.lift, 2))
                + " N and a weight of "
                + str(round(best_plane.weight, 2))
                + "."
            )
        )

        if best_plane.weight > 0:
            content.append(
                Paragraph(
                    "Its estimated lift divided by its weight "
                    "contributes "
                    + str(round(lift_weight_points, 2))
                    + " additional points. A higher ratio adds "
                    "more points to the score."
                )
            )
        else:
            content.append(
                Paragraph(
                    "Because its weight is zero, the app does not "
                    "include a lift-to-weight contribution in "
                    "its score."
                )
            )

        content.append(
            Paragraph(
                "Together, these two contributions produce a total "
                "score of "
                + str(round(best_plane.score, 2))
                + ". This is why "
                + best_plane.name
                + " ranks first among your saved aircraft."
            )
        )

        content.append(
            Paragraph(
                "This is a simplified educational comparison. "
                "A higher score means the aircraft performs better "
                "according to AeroLab's formula. It does not prove "
                "that the aircraft would fly better or be safer "
                "in real-world conditions."
            )
        )

    content.extend([
        Button("Compare Results", "results"),
        "\n",
        Button("Design Another Aircraft", "designer")
    ])

    return make_page(state, "Saved Aircraft", content)


# -----------------------------
# RESULTS COMPARISON PAGE
# -----------------------------

@route
def results(state: State) -> Page:
    state.current_page = "results"

    content = []

    if len(state.planes) == 0:
        content.append(
            Paragraph("Save an aircraft before viewing comparisons.")
        )

    else:
        content.append(
            Paragraph("Compare the scores of your saved aircraft.")
        )

        best_plane = state.planes[0]

        for plane in state.planes:
            if plane.score > best_plane.score:
                best_plane = plane

        content.append(Header("Aircraft Comparison"))

        for plane in state.planes:
            content.append(
                Paragraph(
                    plane.name + " - Score: "
                    + str(round(plane.score, 2))
                )
            )

        content.append(HorizontalRule())
        content.append(Header("Highest Design Score"))

        content.append(
            Paragraph(
                best_plane.name + " has the highest design score."
            )
        )

        content.append(
            Paragraph(
                "Score: " + str(round(best_plane.score, 2))
            )
        )

        content.append(HorizontalRule())
        content.append(Header("Why This Aircraft Is Best"))

        content.append(
            Paragraph(
                "The aircraft ranks first because it has the highest "
                "total score among your saved designs. The score is "
                "calculated using two measurements: aspect ratio "
                "and estimated lift divided by weight."
            )
        )

        aspect_points = best_plane.aspect_ratio * 10

        if best_plane.weight > 0:
            lift_weight_points = best_plane.lift / best_plane.weight
        else:
            lift_weight_points = 0

        content.append(Header("1. Aspect Ratio Contribution"))

        content.append(
            Paragraph(
                "This aircraft has an aspect ratio of "
                + str(round(best_plane.aspect_ratio, 2))
                + ". Its aspect ratio contributes "
                + str(round(aspect_points, 2))
                + " points to the total score."
            )
        )

        content.append(
            Paragraph(
                "A higher aspect ratio adds more points to the score. "
                "In this app, aspect ratio is calculated using "
                "wingspan squared divided by wing area."
            )
        )

        content.append(Header("2. Lift-to-Weight Contribution"))

        content.append(
            Paragraph(
                "This aircraft produces an estimated lift of "
                + str(round(best_plane.lift, 2))
                + " N and has a weight of "
                + str(round(best_plane.weight, 2))
                + "."
            )
        )

        if best_plane.weight > 0:
            content.append(
                Paragraph(
                    "Its estimated lift divided by weight is "
                    + str(round(lift_weight_points, 2))
                    + ". This adds "
                    + str(round(lift_weight_points, 2))
                    + " points to the total score."
                )
            )

            content.append(
                Paragraph(
                    "A higher lift-to-weight ratio adds more points "
                    "because the aircraft produces more estimated "
                    "lift compared with its weight."
                )
            )

        else:
            content.append(
                Paragraph(
                    "Its weight is zero, so the app does not add "
                    "a lift-to-weight contribution to its score. "
                    "Only its aspect ratio contributes points."
                )
            )

        content.append(Header("Winning Score Breakdown"))

        content.append(
            Paragraph(
                "Aspect ratio points: "
                + str(round(aspect_points, 2))
            )
        )

        content.append(
            Paragraph(
                "Lift-to-weight points: "
                + str(round(lift_weight_points, 2))
            )
        )

        content.append(
            Paragraph(
                "Total score: "
                + str(round(best_plane.score, 2))
            )
        )

        content.append(
            Paragraph(
                "The two contributions are added together to produce "
                "the final design score. The aircraft with the highest "
                "total earns first place in this comparison."
            )
        )

        content.append(HorizontalRule())
        content.append(Header("Top Scoring Aircraft Illustration"))

        content.append(
            aircraft_illustration(
                best_plane.wingspan,
                best_plane.chord
            )
        )

        content.append(
            Paragraph(
                "Wingspan: " + str(round(best_plane.wingspan, 2)) + " m"
            )
        )

        content.append(
            Paragraph(
                "Chord: " + str(round(best_plane.chord, 2)) + " m"
            )
        )

        content.append(HorizontalRule())
        content.append(Header("Important Note"))

        content.append(
            Paragraph(
                "This score is a simplified educational tool for "
                "comparing the aircraft designs saved in AeroLab. "
                "A higher score means the aircraft performs better "
                "according to this app's formula. It does not prove "
                "that the aircraft would fly better or be safer "
                "in real-world conditions."
            )
        )

    content.extend([
        "\n",
        Button("View Saved Aircraft", "saved_planes"),
        "\n",
        Button("Design Another Aircraft", "designer")
    ])

    return make_page(state, "Results Comparison", content)


# -----------------------------
# LEARN PAGE
# -----------------------------

@route
def learn(state: State) -> Page:
    state.current_page = "learn"

    content = [
        Header("Aircraft Design Basics"),
        Paragraph(
            "Aircraft design involves balancing several factors, "
            "including wing size, weight, and speed."
        ),
        Header("Wing Area"),
        Paragraph(
            "Wing area is the total area of the wing. "
            "In this application, it is estimated using "
            "wingspan multiplied by chord."
        ),
        Header("Aspect Ratio"),
        Paragraph(
            "Aspect ratio compares wingspan with wing area. "
            "It is calculated by dividing wingspan squared "
            "by wing area."
        ),
        Header("Lift"),
        Paragraph(
            "Lift is the force that helps an aircraft stay in the air. "
            "This application uses a simplified lift equation."
        ),
        Header("Center of Gravity"),
        Paragraph(
            "The center of gravity is the point where the aircraft's "
            "weight is balanced. This application uses a simplified "
            "estimate based on the chord."
        ),
        Paragraph(
            "These calculations are educational estimates. "
            "They do not represent a complete aircraft engineering model."
        ),
        Button("Start Designing", "designer")
    ]

    return make_page(state, "Learn", content)


# -----------------------------
# RESET DESIGN
# -----------------------------

@route
def reset(state: State) -> Page:
    state.current_plane = {
        "name": "My Aircraft",
        "wingspan": 10.0,
        "chord": 1.5,
        "weight": 100.0,
        "speed": 20.0
    }

    return designer(state)


# -----------------------------
# TESTS
# -----------------------------

def run_tests():
    plane = calculate_plane(
        "Test Aircraft",
        10,
        2,
        100,
        20
    )

    assert plane.wing_area == 20
    assert plane.aspect_ratio == 5
    assert plane.cg == 0.5
    assert safe_float(-5) == 0
    assert safe_float("not a number") == 0

    negative_plane = calculate_plane(
        "Negative Test",
        -10,
        -2,
        -100,
        -20
    )

    assert negative_plane.wingspan == 0
    assert negative_plane.chord == 0
    assert negative_plane.weight == 0
    assert negative_plane.speed == 0


# -----------------------------
# START APPLICATION
# -----------------------------

run_tests()
start_server(make_state())
