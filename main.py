
from dataclasses import dataclass, field
from drafter import *

# -----------------------------
# WEBSITE RELEASE SETTINGS
# -----------------------------

set_website_title("AeroLab Aircraft Designer")

set_site_information(
    author="AeroLab Project",
    description=(
        "An educational aircraft design application that lets users "
        "enter aircraft measurements, estimate performance, and "
        "compare saved aircraft designs."
    ),
    sources="Drafter documentation and introductory aircraft design concepts.",
    planning="AeroLab project planning and user-testing feedback.",
    links=["https://github.com/alexnic-hue/AeroLab"]
)

# Keep the original aircraft background image.
# Put aircraft-background.jpg in the same folder as main.py.
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
    lift_weight_ratio: float
    aspect_points: float
    lift_points: float
    score: float


@dataclass
class State:
    planes: list = field(default_factory=list)
    current_plane: dict = field(default_factory=dict)
    current_page: str = "home"


# -----------------------------
# STARTING STATE
# -----------------------------

def make_state():
    return State(
        planes=[],
        current_plane={
            "name": "My Aircraft",
            "wingspan": 10,
            "chord": 2,
            "weight": 100,
            "speed": 20
        }
    )


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def safe_float(value):
    try:
        number = float(value)
        if number < 0:
            return 0.0
        return number
    except (ValueError, TypeError):
        return 0.0


def display_number(value):
    number = safe_float(value)

    if number == int(number):
        return str(int(number))

    return str(number)


# -----------------------------
# CALCULATIONS
# -----------------------------

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

    # Simplified lift equation.
    air_density = 1.225
    lift = 0.5 * air_density * (speed ** 2) * wing_area

    # Simplified center of gravity estimate.
    cg = chord * 0.25

    # Convert mass in kilograms to weight force in newtons.
    weight_force = weight * 9.81

    if weight_force > 0:
        lift_weight_ratio = lift / weight_force
    else:
        lift_weight_ratio = 0

    # Educational design score.
    # Aspect ratio contributes up to 40 points.
    # Lift-to-weight ratio contributes up to 60 points.
    aspect_points = min(40, aspect_ratio * 5)
    lift_points = min(60, lift_weight_ratio * 30)

    score = aspect_points + lift_points
    score = min(100, score)

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
        lift_weight_ratio=lift_weight_ratio,
        aspect_points=aspect_points,
        lift_points=lift_points,
        score=score
    )


def plane_summary(plane):
    return [
        Paragraph("Aircraft: " + plane.name),
        Paragraph("Wingspan: " + display_number(plane.wingspan) + " m"),
        Paragraph("Chord: " + display_number(plane.chord) + " m"),
        Paragraph("Mass: " + display_number(plane.weight) + " kg"),
        Paragraph("Speed: " + display_number(plane.speed) + " m/s"),
        Paragraph("Wing Area: " + str(round(plane.wing_area, 2)) + " m²"),
        Paragraph("Aspect Ratio: " + str(round(plane.aspect_ratio, 2))),
        Paragraph("Estimated Lift: " + str(round(plane.lift, 2)) + " N"),
        Paragraph("Lift-to-Weight Ratio: " + str(round(plane.lift_weight_ratio, 2))),
        Paragraph("Center of Gravity: " + str(round(plane.cg, 2)) + " m"),
        Paragraph("Design Score: " + str(round(plane.score, 2)) + "/100")
    ]


# -----------------------------
# AIRCRAFT ILLUSTRATION
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

        '<circle cx="250" cy="195" r="155" fill="#dceaf5"/>'

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

        '<path d="M250 25 C230 65 232 110 237 155 '
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

    return SVG(drawing, width=500, height=400)


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
        " ",
        Button("Deep Dive", "deep_dive"),
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
            "wingspan", "chord", "weight", "speed"
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
                rgba(255, 255, 255, 0.78),
                rgba(255, 255, 255, 0.78)
            ),
            url("aircraft-background.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #172536;
    }

    p {
        margin-top: 5px;
        margin-bottom: 5px;
        line-height: 1.4;
        color: #172536;
    }

    h1, h2, h3 {
        margin-top: 12px;
        margin-bottom: 7px;
        line-height: 1.2;
        color: #172536;
    }

    hr {
        margin-top: 8px;
        margin-bottom: 8px;
    }

    button {
        margin: 3px;
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
        Paragraph("Calculate wing area, aspect ratio, and estimated lift."),
        Paragraph("See a visual representation of your aircraft."),
        Paragraph("Save aircraft designs and compare their scores."),
        Button("Start Designing", "designer"),
        "\n",
        Button("Read Instructions", "instructions"),
        "\n",
        Button("Learn Aircraft Basics", "learn"),
        "\n",
        Button("Explore the Deep Dive", "deep_dive")
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
            "Enter your aircraft measurements on the Aircraft Designer "
            "page. After calculating your design, you can save it directly "
            "from the results page."
        ),
        Header("Measurements"),
        Paragraph("Wingspan: Distance from one wingtip to the other (meters)."),
        Paragraph("Chord: Distance from the front to the back of the wing (meters)."),
        Paragraph("Mass: The aircraft's mass (kilograms)."),
        Paragraph("Speed: The aircraft's speed (meters per second)."),
        Header("Calculations"),
        Paragraph("Wing Area = Wingspan × Chord (m²)."),
        Paragraph("Aspect Ratio = Wingspan² ÷ Wing Area."),
        Paragraph(
            "Estimated Lift = 0.5 × air density × speed² × wing area (newtons)."
        ),
        Paragraph(
            "The app estimates weight force by multiplying mass in kilograms "
            "by 9.81. The lift-to-weight ratio compares estimated lift "
            "with this weight force."
        ),
        Paragraph("Center of Gravity is estimated as 25% of the chord."),
        Header("Design Score"),
        Paragraph(
            "The design score is out of 100. Aspect ratio contributes "
            "up to 40 points, and lift-to-weight ratio contributes "
            "up to 60 points."
        ),
        Paragraph(
            "This is a simplified educational comparison score. "
            "It is not a real aircraft safety rating or a complete "
            "engineering model."
        ),
        Button("Start Designing", "designer"),
        "\n",
        Button("Learn Aircraft Basics", "learn"),
        "\n",
        Button("Explore the Deep Dive", "deep_dive")
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
            "Use the units shown beside each measurement."
        ),

        Header("Aircraft Name"),
        TextBox(
            "name",
            state.current_plane.get("name", "My Aircraft")
        ),

        Header("Wingspan (meters)"),
        TextBox(
            "wingspan",
            display_number(state.current_plane.get("wingspan", 10)),
            kind="number",
            id="wingspan"
        ),

        Header("Chord (meters)"),
        TextBox(
            "chord",
            display_number(state.current_plane.get("chord", 2)),
            kind="number",
            id="chord"
        ),

        Header("Mass (kilograms)"),
        TextBox(
            "weight",
            display_number(state.current_plane.get("weight", 100)),
            kind="number",
            id="weight"
        ),

        Header("Speed (meters per second)"),
        TextBox(
            "speed",
            display_number(state.current_plane.get("speed", 20)),
            kind="number",
            id="speed"
        ),

        "\n",
        Button("Calculate Aircraft", "update_preview"),
        "\n",
        Button("Reset Measurements", "reset")
    ]

    return make_page(state, "Aircraft Designer", content)


# -----------------------------
# CALCULATE AND PREVIEW AIRCRAFT
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

    if not name.strip():
        name = "My Aircraft"

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
        Header("Your Aircraft Results"),
        Paragraph("Here are the calculated results for your aircraft."),

        Header("Measurements"),
        Paragraph("Wingspan: " + display_number(plane.wingspan) + " m"),
        Paragraph("Chord: " + display_number(plane.chord) + " m"),
        Paragraph("Mass: " + display_number(plane.weight) + " kg"),
        Paragraph("Speed: " + display_number(plane.speed) + " m/s"),

        Header("Calculated Results"),
        Paragraph("Wing Area: " + str(round(plane.wing_area, 2)) + " m²"),
        Paragraph("Aspect Ratio: " + str(round(plane.aspect_ratio, 2))),
        Paragraph("Estimated Lift: " + str(round(plane.lift, 2)) + " N"),
        Paragraph(
            "Estimated Center of Gravity: "
            + str(round(plane.cg, 2)) + " m"
        ),
        Paragraph(
            "Lift-to-Weight Ratio: "
            + str(round(plane.lift_weight_ratio, 2))
        ),

        Header("Design Score"),
        Paragraph(str(round(plane.score, 2)) + " / 100"),
        Paragraph(
            "Aspect ratio contribution: "
            + str(round(plane.aspect_points, 2))
            + " / 40 points"
        ),
        Paragraph(
            "Lift-to-weight contribution: "
            + str(round(plane.lift_points, 2))
            + " / 60 points"
        ),

        Paragraph(
            "The score is a simplified educational comparison. "
            "It does not determine whether an aircraft is safe to fly."
        ),

        Header("Aircraft Illustration"),
        aircraft_illustration(plane.wingspan, plane.chord),

        "\n",
        Button("Save This Aircraft", "save_plane"),
        "\n",
        Button("Edit Aircraft", "designer"),
        "\n",
        Button("View Saved Aircraft", "saved_planes")
    ]

    return make_page(state, "Aircraft Results", content)


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

    content = [
        Header("Aircraft Saved!"),
        Paragraph(
            plane.name + " has been added to your saved aircraft."
        ),
        Paragraph(
            "Your aircraft received a design score of "
            + str(round(plane.score, 2))
            + " out of 100."
        ),
        Button("View Saved Aircraft", "saved_planes"),
        "\n",
        Button("Design Another Aircraft", "designer"),
        "\n",
        Button("Compare Results", "results")
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
        content.append(
            Button("Start Designing", "designer")
        )

    else:
        content.append(
            Paragraph(
                "You have saved " + str(len(state.planes)) + " aircraft."
            )
        )

        best_plane = state.planes[0]

        for plane in state.planes:
            content.append(HorizontalRule())
            content.append(Header(plane.name))
            content.extend(plane_summary(plane))

            if plane.score > best_plane.score:
                best_plane = plane

        content.append(HorizontalRule())
        content.append(Header("Best Saved Aircraft"))

        content.append(
            Paragraph(
                best_plane.name
                + " has the highest design score among your saved aircraft."
            )
        )

        content.append(
            Paragraph(
                "Its score is "
                + str(round(best_plane.score, 2))
                + " out of 100."
            )
        )

        content.append(Header("Why This Aircraft Ranks First"))

        content.append(
            Paragraph(
                "Aspect ratio contribution: "
                + str(round(best_plane.aspect_points, 2))
                + " out of 40 points."
            )
        )

        content.append(
            Paragraph(
                "Lift-to-weight contribution: "
                + str(round(best_plane.lift_points, 2))
                + " out of 60 points."
            )
        )

        content.append(
            Paragraph(
                "These two contributions are added together to produce "
                "the final score. The aircraft with the highest score "
                "ranks first."
            )
        )

        content.append(
            Paragraph(
                "This score is an educational comparison tool. "
                "It does not prove that an aircraft would fly better "
                "or be safer in real-world conditions."
            )
        )

    content.extend([
        "\n",
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
        content.append(
            Button("Start Designing", "designer")
        )

    else:
        best_plane = state.planes[0]

        for plane in state.planes:
            if plane.score > best_plane.score:
                best_plane = plane

        content.append(
            Paragraph("Compare the scores of your saved aircraft.")
        )

        content.append(Header("Aircraft Comparison"))

        for plane in state.planes:
            content.append(
                Paragraph(
                    plane.name + " - "
                    + str(round(plane.score, 2))
                    + " / 100"
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
                "Score: "
                + str(round(best_plane.score, 2))
                + " / 100"
            )
        )

        content.append(Header("Score Breakdown"))

        content.append(
            Paragraph(
                "Aspect ratio: "
                + str(round(best_plane.aspect_points, 2))
                + " / 40 points."
            )
        )

        content.append(
            Paragraph(
                "Lift-to-weight ratio: "
                + str(round(best_plane.lift_points, 2))
                + " / 60 points."
            )
        )

        content.append(
            Paragraph(
                "The two contributions are added together. "
                "The aircraft with the highest total score ranks first."
            )
        )

        content.append(Header("Top Scoring Aircraft Illustration"))

        content.append(
            aircraft_illustration(
                best_plane.wingspan,
                best_plane.chord
            )
        )

        content.append(
            Paragraph(
                "Wingspan: "
                + display_number(best_plane.wingspan)
                + " m"
            )
        )

        content.append(
            Paragraph(
                "Chord: "
                + display_number(best_plane.chord)
                + " m"
            )
        )

        content.append(
            Paragraph(
                "A higher score means the aircraft performs better "
                "according to AeroLab's simplified formula. It does "
                "not prove real-world flight performance or safety."
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
# LEARN PAGE - BEGINNER LEVEL
# -----------------------------

@route
def learn(state: State) -> Page:
    state.current_page = "learn"

    content = [
        Header("Aircraft Design Basics"),

        Paragraph(
            "Welcome to the beginner learning page! This page introduces "
            "the main ideas behind aircraft design without going too "
            "deep into the mathematics. You can use these concepts "
            "to understand the measurements in the Aircraft Designer."
        ),

        Header("What Makes an Aircraft Fly?"),

        Paragraph(
            "An aircraft flies because several forces work together. "
            "The four main forces are lift, weight, thrust, and drag."
        ),

        Paragraph(
            "Lift is the aerodynamic force that helps support the aircraft. "
            "Weight is the force of gravity pulling it downward. Thrust "
            "pushes the aircraft forward, while drag is air resistance "
            "that opposes its movement."
        ),

        Paragraph(
            "During steady, level flight, lift balances weight and "
            "thrust balances drag."
        ),

        Header("Wingspan"),

        Paragraph(
            "Wingspan is the distance from one wingtip to the other. "
            "Longer wings can help improve aerodynamic efficiency, "
            "although they may also require stronger structures."
        ),

        Header("Chord"),

        Paragraph(
            "Chord is the distance from the front edge of the wing "
            "to its back edge. A wider chord creates a deeper wing."
        ),

        Header("Wing Area"),

        Paragraph(
            "Wing area describes how much surface the wing covers "
            "when viewed from above. A larger wing area can help "
            "produce more lift under similar conditions."
        ),

        Paragraph("Wing Area = Wingspan × Chord"),

        Header("Aspect Ratio"),

        Paragraph(
            "Aspect ratio describes whether a wing is long and narrow "
            "or short and wide. Long, narrow wings have higher aspect "
            "ratios and are common on gliders."
        ),

        Paragraph("Aspect Ratio = Wingspan² ÷ Wing Area"),

        Header("Lift"),

        Paragraph(
            "Lift is the aerodynamic force that acts on an aircraft's "
            "wings. It depends on factors such as speed, wing area, "
            "air density, and wing shape."
        ),

        Paragraph(
            "AeroLab estimates lift using a simplified equation. "
            "The result is displayed in newtons (N), a unit of force."
        ),

        Header("Mass and Weight"),

        Paragraph(
            "Mass measures how much matter an aircraft contains "
            "and is measured in kilograms. Weight is the force "
            "of gravity acting on that mass."
        ),

        Paragraph(
            "AeroLab estimates weight force by multiplying mass "
            "by 9.81."
        ),

        Header("Center of Gravity"),

        Paragraph(
            "The center of gravity is the point where an aircraft's "
            "weight is balanced. Its position is important for "
            "aircraft stability and control."
        ),

        Header("The AeroLab Score"),

        Paragraph(
            "AeroLab gives each aircraft a score out of 100. The score "
            "uses aspect ratio and lift-to-weight ratio to compare "
            "saved designs."
        ),

        Paragraph(
            "The score is an educational comparison tool, not a real "
            "aircraft safety rating."
        ),

        Header("Want to Learn More?"),

        Paragraph(
            "The Deep Dive page explains the science and mathematics "
            "behind these concepts in more detail. It includes examples "
            "and explains how changing one measurement affects others."
        ),

        Button("Open the Deep Dive", "deep_dive"),
        "\n",
        Button("Start Designing", "designer")
    ]

    return make_page(state, "Learn: Aircraft Basics", content)


# -----------------------------
# DEEP DIVE PAGE - ADVANCED LEVEL
# -----------------------------

@route
def deep_dive(state: State) -> Page:
    state.current_page = "deep_dive"

    content = [
        Header("The Science Behind Aircraft Design"),

        Paragraph(
            "This page explores aircraft design in greater depth. "
            "It explains the physical ideas, mathematical relationships, "
            "and engineering trade-offs behind the calculations used "
            "in AeroLab."
        ),

        Paragraph(
            "The goal is to understand not only what each measurement "
            "means, but also why it matters and how it interacts "
            "with the other parts of an aircraft."
        ),

        Header("1. The Four Forces of Flight"),

        Paragraph(
            "Aircraft flight involves four major forces: lift, weight, "
            "thrust, and drag. These forces determine how an aircraft "
            "moves through the air."
        ),

        Paragraph(
            "Lift is an aerodynamic force generated by the wings. "
            "It acts approximately perpendicular to the oncoming airflow."
        ),

        Paragraph(
            "Weight is the force of gravity acting on the aircraft. "
            "It acts downward toward Earth's center."
        ),

        Paragraph(
            "Thrust is the forward force produced by an engine or "
            "another propulsion system. Drag is the aerodynamic "
            "resistance that opposes movement through the air."
        ),

        Paragraph(
            "During steady, level flight, the vertical forces balance "
            "and the horizontal forces balance. During climbing, turning, "
            "accelerating, or slowing down, the forces are not necessarily "
            "balanced."
        ),

        Header("2. Wingspan and Wing Geometry"),

        Paragraph(
            "Wingspan is the distance from one wingtip to the other. "
            "It is one of the main dimensions used to describe a wing."
        ),

        Paragraph(
            "A wing's geometry affects its aerodynamic performance. "
            "Longer wings can reduce induced drag for comparable lift "
            "conditions, which is one reason gliders often have long, "
            "narrow wings."
        ),

        Paragraph(
            "However, increasing wingspan can also increase bending "
            "loads on the wing structure. The wing must be strong "
            "enough to handle the forces created during flight."
        ),

        Paragraph(
            "Engineers therefore consider both aerodynamic efficiency "
            "and structural requirements when choosing a wingspan."
        ),

        Header("3. Chord and Wing Shape"),

        Paragraph(
            "Chord is the distance between the leading edge and trailing "
            "edge of a wing. The leading edge is the front of the wing, "
            "and the trailing edge is the back."
        ),

        Paragraph(
            "A wing with a larger chord is deeper from front to back. "
            "For a rectangular wing, increasing chord while keeping "
            "wingspan constant increases the total wing area."
        ),

        Paragraph(
            "Real aircraft wings may have different chord lengths "
            "at different positions. Some wings are tapered, swept, "
            "or curved. AeroLab uses a simplified rectangular wing "
            "so that the geometry is easier to understand."
        ),

        Header("4. Wing Area and Its Importance"),

        Paragraph(
            "Wing area is the surface area of the wing when viewed "
            "from above. It is an important factor in determining "
            "how much lift a wing can produce."
        ),

        Paragraph(
            "AeroLab uses the following rectangular-wing formula:"
        ),

        Paragraph("Wing Area = Wingspan × Chord"),

        Paragraph(
            "For example, a wing with a 10-meter wingspan and "
            "a 2-meter chord has an estimated area of 20 square meters."
        ),

        Paragraph(
            "If the chord is increased to 3 meters while wingspan "
            "remains 10 meters, the estimated wing area becomes "
            "30 square meters."
        ),

        Paragraph(
            "A larger wing area can produce more lift at the same "
            "speed and under otherwise similar conditions. However, "
            "it may also increase drag and structural weight."
        ),

        Header("5. Aspect Ratio and Aerodynamic Efficiency"),

        Paragraph(
            "Aspect ratio describes how long and narrow a wing is. "
            "It compares wingspan squared with wing area."
        ),

        Paragraph("Aspect Ratio = Wingspan² ÷ Wing Area"),

        Paragraph(
            "For a rectangular wing, the formula can also be simplified "
            "to wingspan divided by chord."
        ),

        Paragraph(
            "Consider two rectangular wings with the same area. "
            "A wing that is longer and narrower will have a higher "
            "aspect ratio than a wing that is shorter and wider."
        ),

        Paragraph(
            "A higher aspect ratio is often associated with lower "
            "induced drag for comparable lift conditions. Induced drag "
            "is a type of aerodynamic drag that occurs as a consequence "
            "of producing lift."
        ),

        Paragraph(
            "This helps explain why gliders often use long, narrow wings. "
            "Reducing induced drag can help them travel farther while "
            "losing less altitude."
        ),

        Paragraph(
            "However, a high aspect ratio is not always the best choice. "
            "Long wings can create structural challenges and may not "
            "suit every aircraft's speed, maneuverability, or mission."
        ),

        Header("6. How Lift Is Generated"),

        Paragraph(
            "Lift is generated when a wing interacts with the air. "
            "The wing changes the airflow around it, producing pressure "
            "differences and changing the momentum of the air. These "
            "effects create an aerodynamic force."
        ),

        Paragraph(
            "One important concept is angle of attack. This is the angle "
            "between the wing's reference line and the direction of "
            "the oncoming airflow."
        ),

        Paragraph(
            "Changing the angle of attack changes the way air flows "
            "around the wing and affects the lift it produces. "
            "If the angle becomes too large, the wing can stall, "
            "causing a major loss of lift."
        ),

        Header("7. The Lift Equation"),

        Paragraph(
            "A common aerodynamic equation for lift is:"
        ),

        Paragraph(
            "Lift = 0.5 × Air Density × Speed² × Wing Area × Lift Coefficient"
        ),

        Paragraph(
            "Air density describes how much air mass is contained "
            "in a given volume. It changes with altitude, temperature, "
            "and atmospheric pressure."
        ),

        Paragraph(
            "Speed is squared in the equation. This means that if "
            "speed doubles while all other factors remain constant, "
            "the predicted lift becomes four times as large."
        ),

        Paragraph(
            "Wing area affects lift directly. If wing area doubles "
            "while all other factors remain constant, predicted "
            "lift doubles."
        ),

        Paragraph(
            "The lift coefficient represents how effectively a wing "
            "produces lift under particular conditions. It depends "
            "on factors such as wing shape and angle of attack."
        ),

        Paragraph(
            "AeroLab uses an air density of 1.225 kg/m³ and does not "
            "ask for a lift coefficient. Its simplified calculation "
            "effectively assumes a coefficient of 1."
        ),

        Paragraph(
            "This makes the calculation easier to explore, but it "
            "does not represent the complete aerodynamic behavior "
            "of a real wing."
        ),

        Header("8. Mass, Weight, and Gravity"),

        Paragraph(
            "Mass and weight are related, but they describe different "
            "physical quantities. Mass measures the amount of matter "
            "in an object and is measured in kilograms."
        ),

        Paragraph(
            "Weight is the gravitational force acting on an object "
            "and is measured in newtons."
        ),

        Paragraph("Weight Force = Mass × Gravitational Acceleration"),

        Paragraph(
            "AeroLab uses approximately 9.81 m/s² for gravitational "
            "acceleration near Earth's surface."
        ),

        Paragraph(
            "For example, an aircraft with a mass of 100 kg has "
            "an estimated weight force of 981 N."
        ),

        Paragraph(
            "When aircraft mass increases, the aircraft's weight "
            "force increases. The wings must generate enough lift "
            "to support that weight during steady, level flight."
        ),

        Header("9. Lift-to-Weight Ratio"),

        Paragraph(
            "The lift-to-weight ratio compares the estimated lift "
            "force with the aircraft's estimated weight force."
        ),

        Paragraph(
            "Lift-to-Weight Ratio = Estimated Lift ÷ Weight Force"
        ),

        Paragraph(
            "A ratio of 1 means the estimated lift equals the estimated "
            "weight force. A ratio greater than 1 means the estimated "
            "lift is greater than the weight force. A ratio below 1 "
            "means estimated lift is less than weight force."
        ),

        Paragraph(
            "This ratio is useful for exploring how an aircraft's "
            "estimated lift compares with its weight. It does not "
            "by itself determine whether an aircraft can take off "
            "or maintain safe flight."
        ),

        Paragraph(
            "Real flight also depends on thrust, drag, stability, "
            "control, and changing conditions."
        ),

        Header("10. Center of Gravity and Stability"),

        Paragraph(
            "The center of gravity is the point at which the aircraft's "
            "total weight can be considered to act. Its position has "
            "a major influence on aircraft balance and stability."
        ),

        Paragraph(
            "An aircraft's center of gravity depends on the location "
            "and mass of its components. These can include the engine, "
            "wings, fuel, passengers, and equipment."
        ),

        Paragraph(
            "If the center of gravity is too far forward or too far "
            "backward, the aircraft may become difficult to control "
            "or may have unsafe stability characteristics."
        ),

        Paragraph(
            "AeroLab estimates the center of gravity as 25% of the "
            "wing chord. This is only a simplified reference estimate. "
            "It does not calculate the actual center of gravity of "
            "a complete aircraft."
        ),

        Header("11. How the Variables Affect Each Other"),

        Paragraph(
            "Aircraft measurements are connected. Changing one "
            "measurement can affect several calculations at the "
            "same time."
        ),

        Paragraph(
            "For example, increasing wingspan while keeping chord "
            "constant increases wing area. It also changes aspect ratio. "
            "This affects both the estimated lift and the aspect-ratio "
            "part of the AeroLab score."
        ),

        Paragraph(
            "Increasing chord while keeping wingspan constant increases "
            "wing area but decreases aspect ratio. This shows that "
            "a change that improves one measurement does not necessarily "
            "improve every other measurement."
        ),

        Paragraph(
            "Increasing speed has a particularly strong effect on "
            "the lift estimate because speed is squared. Doubling "
            "speed produces four times the estimated lift when the "
            "other factors stay the same."
        ),

        Paragraph(
            "Increasing mass increases weight force. If estimated "
            "lift stays the same, the lift-to-weight ratio decreases."
        ),

        Paragraph(
            "This is why aircraft design involves balancing many "
            "different factors rather than maximizing one measurement."
        ),

        Header("12. Understanding the AeroLab Score"),

        Paragraph(
            "AeroLab uses a score out of 100 to compare saved designs. "
            "It uses two contributions: aspect ratio and lift-to-weight ratio."
        ),

        Paragraph(
            "Aspect ratio contributes up to 40 points. The app "
            "multiplies aspect ratio by 5 and limits the result "
            "to a maximum of 40 points."
        ),

        Paragraph(
            "Lift-to-weight ratio contributes up to 60 points. "
            "The app multiplies the ratio by 30 and limits the "
            "result to a maximum of 60 points."
        ),

        Paragraph(
            "The two contributions are added together to calculate "
            "the final score. The final result cannot exceed 100."
        ),

        Paragraph(
            "The score is designed to help users compare their own "
            "designs using the same simplified rules. It is not "
            "a scientifically validated measure of aircraft quality."
        ),

        Header("13. Limitations of AeroLab's Model"),

        Paragraph(
            "Real aircraft engineering involves many more variables "
            "than the ones included in AeroLab."
        ),

        Paragraph(
            "The app assumes a rectangular wing, uses a fixed air "
            "density, and does not calculate a changing lift coefficient."
        ),

        Paragraph(
            "It also does not fully model drag, thrust, engine power, "
            "structural strength, material properties, control surfaces, "
            "stability, weather, or different flight conditions."
        ),

        Paragraph(
            "The center of gravity calculation is also simplified. "
            "A real aircraft's balance must be calculated using the "
            "locations and masses of its individual components."
        ),

        Paragraph(
            "For these reasons, AeroLab is an educational tool for "
            "exploring basic relationships. Its results should not "
            "be used to build, certify, or determine the safety "
            "of a real aircraft."
        ),

        Header("14. Experiment Like an Engineer"),

        Paragraph(
            "A useful way to learn about aircraft design is to change "
            "one variable at a time. This makes it easier to see "
            "which calculations are affected by each change."
        ),

        Paragraph(
            "Experiment 1: Increase wingspan while keeping chord, "
            "mass, and speed the same. Observe how wing area, "
            "aspect ratio, and score change."
        ),

        Paragraph(
            "Experiment 2: Increase chord while keeping the other "
            "measurements the same. Compare the changes in wing "
            "area and aspect ratio."
        ),

        Paragraph(
            "Experiment 3: Double the speed. Compare the estimated "
            "lift with your original design. Think about why the "
            "change is much larger than a simple doubling."
        ),

        Paragraph(
            "Experiment 4: Increase mass without changing the wing "
            "measurements or speed. Observe how the lift-to-weight "
            "ratio changes."
        ),

        Paragraph(
            "After each experiment, explain what changed and why. "
            "This is similar to how engineers use calculations and "
            "testing to understand design decisions."
        ),

        Button("Try These Ideas in the Designer", "designer"),
        "\n",
        Button("Return to Beginner Learning", "learn")
    ]

    return make_page(state, "Deep Dive: Aircraft Engineering", content)


# -----------------------------
# RESET DESIGN
# -----------------------------

@route
def reset(state: State) -> Page:
    state.current_plane = {
        "name": "My Aircraft",
        "wingspan": 10,
        "chord": 2,
        "weight": 100,
        "speed": 20
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
    assert plane.score <= 100
    assert plane.score >= 0
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

    zero_weight_plane = calculate_plane(
        "Zero Weight Test",
        10,
        2,
        0,
        20
    )

    assert zero_weight_plane.lift_weight_ratio == 0

    # Test number formatting.
    assert display_number(10.0) == "10"
    assert display_number(2.0) == "2"
    assert display_number(10.5) == "10.5"


# -----------------------------
# START APPLICATION
# -----------------------------

run_tests()
start_server(make_state())
