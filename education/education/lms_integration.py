# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _


COURSE_CURRICULUM_DATA = {
    "Physics": [
        {
            "chapter": "Physical Quantities and Measurement",
            "lessons": [
                {
                    "title": "Fundamental and Derived Physical Quantities",
                    "body": "### Physical Quantities\n\nAnything in the physical world that can be measured is known as a physical quantity. Physical quantities are broadly classified into:\n\n1. **Fundamental Quantities**: Length, mass, time, electric current, thermodynamic temperature, amount of substance, and luminous intensity.\n2. **Derived Quantities**: Velocity, acceleration, force, work, energy, etc.\n\n### Measuring Instruments\n- **Slide Calipers / Vernier Scale**: Vernier Constant $VC = \\frac{s}{n}$.\n- **Screw Gauge**: Least count measurement and pitch calculation.",
                },
                {
                    "title": "Errors in Measurement and Scientific Dimension",
                    "body": "### Measurement Errors\n- Instrumental errors\n- Personal/observational errors\n- Random and systematic errors\n\nDimensional formulas help verify the physical consistency of equations.",
                },
            ],
        },
        {
            "chapter": "Motion and Kinematics",
            "lessons": [
                {
                    "title": "Equations of Linear Motion",
                    "body": "### Equations of Motion under Constant Acceleration\n\n1. $v = u + at$\n2. $s = \\frac{u + v}{2} t$\n3. $s = ut + \\frac{1}{2}at^2$\n4. $v^2 = u^2 + 2as$\n\nWhere:\n- $u$: Initial velocity\n- $v$: Final velocity\n- $a$: Uniform acceleration\n- $t$: Time elapsed\n- $s$: Distance traveled",
                },
                {
                    "title": "Laws of Falling Bodies",
                    "body": "Galileo Galilei formulated three laws for freely falling bodies in vacuum:\n1. All bodies falling from rest traverse equal distances in equal times.\n2. Velocity is directly proportional to time: $v \\propto t$.\n3. Distance is proportional to the square of time: $h \\propto t^2$.",
                },
            ],
        },
        {
            "chapter": "Force and Newton's Laws",
            "lessons": [
                {
                    "title": "Newton's Three Laws of Motion",
                    "body": "### First Law\nEvery body persists in its state of being at rest or of moving uniformly straight forward, unless compelled to change its state by force impressed.\n\n### Second Law\nThe rate of change of momentum is proportional to the impressed force: $F = ma$.\n\n### Third Law\nTo every action there is always an equal and opposite reaction.",
                },
                {
                    "title": "Friction and Momentum Conservation",
                    "body": "### Law of Conservation of Momentum\n$$m_1 u_1 + m_2 u_2 = m_1 v_1 + m_2 v_2$$\n\nTypes of friction: Static, sliding, rolling, and fluid friction.",
                },
            ],
        },
        {
            "chapter": "Work, Power and Energy",
            "lessons": [
                {
                    "title": "Work and Kinetic Energy",
                    "body": "Work done $W = F \\cdot s \\cos \\theta$.\nKinetic Energy: $E_k = \\frac{1}{2}mv^2$.\nPotential Energy: $E_p = mgh$.\n\nPrinciple of conservation of mechanical energy states that the total mechanical energy ($E_k + E_p$) remains constant in a conservative force field.",
                },
            ],
        },
    ],
    "Chemistry": [
        {
            "chapter": "States of Matter",
            "lessons": [
                {
                    "title": "Kinetic Particle Theory of Matter",
                    "body": "All substances are made of particles (atoms, molecules, or ions) held together by forces of attraction. Particles possess kinetic energy, which increases with temperature.\n\n- **Solid**: Fixed shape and volume, closely packed.\n- **Liquid**: Fixed volume, variable shape, sliding particles.\n- **Gas**: Neither fixed shape nor volume, random rapid motion.",
                },
                {
                    "title": "Diffusion and Effusion",
                    "body": "Diffusion is the spontaneous spreading of particles from high to low concentration. Graham's Law dictates that lighter gases diffuse faster than heavier gases: $r \\propto \\frac{1}{\\sqrt{M}}$.",
                },
            ],
        },
        {
            "chapter": "Structure of Atom",
            "lessons": [
                {
                    "title": "Subatomic Particles and Atomic Models",
                    "body": "### Rutherford and Bohr Atomic Models\n- **Electrons**: negatively charged ($e = -1.6 \\times 10^{-19}$ C)\n- **Protons**: positively charged\n- **Neutrons**: neutral charge\n\nBohr's stationary energy levels and electron energy transitions.",
                },
                {
                    "title": "Electronic Configuration and Orbitals",
                    "body": "Electrons are arranged in shells ($n=1, 2, 3...$) and subshells ($s, p, d, f$) following the Aufbau principle, Pauli exclusion principle, and Hund's rule.",
                },
            ],
        },
        {
            "chapter": "Periodic Table",
            "lessons": [
                {
                    "title": "Periodic Law and Periodic Properties",
                    "body": "Properties of elements repeat periodically when arranged in order of atomic number.\n- **Atomic radius**: decreases across a period, increases down a group.\n- **Ionization energy**: increases across a period, decreases down a group.\n- **Electronegativity**: tendency to attract shared electron pairs.",
                },
            ],
        },
        {
            "chapter": "Chemical Bonds",
            "lessons": [
                {
                    "title": "Ionic and Covalent Bonds",
                    "body": "Ionic bonds are formed by electrostatic attraction between cations and anions (electron transfer). Covalent bonds are formed by mutual sharing of electron pairs to achieve stable octet configuration.",
                },
            ],
        },
    ],
    "Biology": [
        {
            "chapter": "Life Lessons and Taxonomy",
            "lessons": [
                {
                    "title": "Five Kingdom Classification & Binomial Nomenclature",
                    "body": "### Whittaker & Margulis 5 Kingdom System\n1. Monera\n2. Protista\n3. Fungi\n4. Plantae\n5. Animalia\n\n### Binomial Nomenclature\nIntroduced by Carolus Linnaeus (e.g., *Homo sapiens*, *Oryza sativa*).",
                },
            ],
        },
        {
            "chapter": "Cells and Tissues",
            "lessons": [
                {
                    "title": "Plant and Animal Cell Organelles",
                    "body": "Major organelles include the Nucleus (genetic command center), Mitochondria (powerhouse of cell), Chloroplasts (photosynthesis site), and Endoplasmic Reticulum.",
                },
                {
                    "title": "Plant & Animal Tissues",
                    "body": "Meristematic vs permanent plant tissues. Epithelial, connective, muscular, and nervous animal tissues.",
                },
            ],
        },
        {
            "chapter": "Cell Division",
            "lessons": [
                {
                    "title": "Mitosis and Meiosis",
                    "body": "Mitosis produces two genetically identical daughter cells for growth and repair. Meiosis produces four haploid gametes, introducing genetic variation through crossing over.",
                },
            ],
        },
    ],
    "General Mathematics": [
        {
            "chapter": "Real Numbers and Sets",
            "lessons": [
                {
                    "title": "Real Number System and Operations",
                    "body": "Rational vs irrational numbers. Terminating and recurring decimals. Set operations: union, intersection, complement, Cartesian product.",
                },
            ],
        },
        {
            "chapter": "Algebraic Expressions",
            "lessons": [
                {
                    "title": "Formulae, Factorization, and LCM/HCF",
                    "body": "Standard algebraic identities:\n- $(a + b)^2 = a^2 + 2ab + b^2$\n- $a^3 + b^3 = (a + b)(a^2 - ab + b^2)$\nFactorization using middle-term split and remainder theorem.",
                },
            ],
        },
        {
            "chapter": "Trigonometry and Geometry",
            "lessons": [
                {
                    "title": "Trigonometric Ratios and Angles",
                    "body": "Values of $\\sin, \\cos, \\tan$ for $0^\\circ, 30^\\circ, 45^\\circ, 60^\\circ, 90^\\circ$.\nBasic identities:\n- $\\sin^2 \\theta + \\cos^2 \\theta = 1$\n- $\\sec^2 \\theta - \\tan^2 \\theta = 1$",
                },
            ],
        },
    ],
    "Higher Mathematics": [
        {
            "chapter": "Set, Functions and Polynomials",
            "lessons": [
                {
                    "title": "Functions, Domain, and Range",
                    "body": "One-to-one (injective) functions, onto (surjective) functions, composite functions $f(g(x))$, and inverse functions $f^{-1}(x)$.",
                },
                {
                    "title": "Polynomials and Partial Fractions",
                    "body": "Remainder Theorem, Factor Theorem, and decomposing rational fractions into partial fractions.",
                },
            ],
        },
        {
            "chapter": "Coordinate Geometry",
            "lessons": [
                {
                    "title": "Distance, Gradient, and Straight Line",
                    "body": "Distance formula: $d = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$.\nSlope of line: $m = \\frac{y_2 - y_1}{x_2 - x_1}$.\nStandard line equation: $y - y_1 = m(x - x_1)$.",
                },
            ],
        },
    ],
    "Bangla": [
        {
            "chapter": "Bangla Sahitya (Literature)",
            "lessons": [
                {
                    "title": "Prose and Poetry Anthology",
                    "body": "Study of selected classic and modern Bangla literature, thematic analysis of essays, short stories, and patriotic poems.",
                },
            ],
        },
        {
            "chapter": "Bangla Byakoron (Grammar)",
            "lessons": [
                {
                    "title": "Shobdo, Karak o Bibhokti",
                    "body": "Detailed breakdown of Bangla phonetics, word formation, sandhi, samas, karak, and bibhokti rules.",
                },
            ],
        },
    ],
    "English": [
        {
            "chapter": "Reading Comprehension & Vocabulary",
            "lessons": [
                {
                    "title": "Contextual Reading and Critical Analysis",
                    "body": "Techniques for skim reading, scan reading, inferring contextual meaning, and summarizing complex English passages.",
                },
            ],
        },
        {
            "chapter": "Grammar and Composition",
            "lessons": [
                {
                    "title": "Transformation of Sentences & Writing Skills",
                    "body": "Rules for active-passive voice, direct-indirect speech, complex-compound sentences, formal emails, and argumentative essays.",
                },
            ],
        },
    ],
    "ICT": [
        {
            "chapter": "Digital Technologies and Society",
            "lessons": [
                {
                    "title": "Computer Networks and Cyber Security",
                    "body": "Network topologies (Bus, Star, Mesh). Data security principles, malware types, encryption, and safe digital citizenship.",
                },
            ],
        },
        {
            "chapter": "Web Development Basics",
            "lessons": [
                {
                    "title": "HTML5 and Responsive Layouts",
                    "body": "Fundamental HTML structure: headings, paragraphs, lists, anchor tags, images, tables, and introductory CSS styling.",
                },
            ],
        },
    ],
    "Bangladesh and Global Studies": [
        {
            "chapter": "History of Bangladesh",
            "lessons": [
                {
                    "title": "Language Movement to Liberation War 1971",
                    "body": "Historical events leading from the 1952 Language Movement, 6-Point Programme of 1966, to the historic 7th March speech and the 1971 War of Liberation.",
                },
            ],
        },
        {
            "chapter": "Constitution and Governance",
            "lessons": [
                {
                    "title": "Fundamental Principles of State Policy",
                    "body": "Structure of the Bangladesh state: Executive, Legislative (Jatiya Sangsad), and Judiciary organs and their constitutional powers.",
                },
            ],
        },
    ],
    "Islam and Moral Education": [
        {
            "chapter": "Aqeedah and Beliefs",
            "lessons": [
                {
                    "title": "Tawheed, Risalat and Akhirah",
                    "body": "Core tenets of Islamic faith: Belief in Oneness of Allah (Tawheed), Prophets (Risalat), Angels, Revealed Books, and the Day of Judgment (Akhirah).",
                },
            ],
        },
        {
            "chapter": "Akhlaq (Moral Values)",
            "lessons": [
                {
                    "title": "Truthfulness, Integrity and Civic Responsibility",
                    "body": "Personal and social morality: Honesty in transactions, kindness to parents, neighbors, and respect for diversity and human dignity.",
                },
            ],
        },
    ],
}


def get_lms_course_for_education_course(course_name: str) -> str | None:
    """Find the LMS Course name corresponding to an Education Course."""
    if not course_name:
        return None
    lms_course = frappe.db.get_value("Course", course_name, "lms_course")
    if lms_course and frappe.db.exists("LMS Course", lms_course):
        return lms_course
    # Check by title
    existing = frappe.db.get_value("LMS Course", {"title": course_name}, "name")
    if existing:
        return existing
    if frappe.db.exists("LMS Course", course_name):
        return course_name
    return None


@frappe.whitelist()
def create_or_link_lms_course(course_name: str) -> str:
    """Explicitly link or generate an LMS Course from Education Course."""
    return sync_course_to_lms(course_name)


def sync_course_to_lms(course_doc, method=None) -> str | None:
    """Sync Course from Education to LMS Course."""
    if "lms" not in frappe.get_installed_apps():
        return None

    course_name = course_doc.name if hasattr(course_doc, "name") else course_doc
    if isinstance(course_doc, str):
        if not frappe.db.exists("Course", course_name):
            return None
        course_doc = frappe.get_doc("Course", course_name)

    existing_lms = get_lms_course_for_education_course(course_doc.course_name)
    if existing_lms:
        if course_doc.get("lms_course") != existing_lms:
            frappe.db.set_value("Course", course_doc.name, "lms_course", existing_lms)
        return existing_lms

    # Get instructors to assign
    instructor_users = []
    instructors = frappe.get_all("Instructor", fields=["name", "employee"])
    for ins in instructors:
        if ins.employee:
            uid = frappe.db.get_value("Employee", ins.employee, "user_id")
            if uid and frappe.db.exists("User", uid):
                instructor_users.append(uid)

    # Create new LMS Course
    lms_doc = frappe.new_doc("LMS Course")
    lms_doc.title = course_doc.course_name
    lms_doc.published = 1
    lms_doc.short_introduction = f"Curriculum coursework for {course_doc.course_name}."
    lms_doc.description = (
        course_doc.description
        or f"Comprehensive lessons, notes, and exercises for {course_doc.course_name}."
    )
    for u in set(instructor_users):
        lms_doc.append("instructors", {"instructor": u})

    lms_doc.insert(ignore_permissions=True)
    frappe.db.set_value("Course", course_doc.name, "lms_course", lms_doc.name)

    # Populate curriculum chapters & lessons
    populate_course_curriculum(lms_doc.name, course_doc.course_name)
    return lms_doc.name


def populate_course_curriculum(lms_course_name: str, course_title: str):
    """Generate default chapters and lessons for a course."""
    chapters_data = COURSE_CURRICULUM_DATA.get(course_title, [])
    if not chapters_data:
        # Generic chapter & lesson
        chapters_data = [
            {
                "chapter": f"Introduction to {course_title}",
                "lessons": [
                    {
                        "title": f"Course Overview & Syllabus: {course_title}",
                        "body": f"### Welcome to {course_title}\n\nThis course covers fundamental concepts, core curriculum topics, assignments, and assessments for the academic year.",
                    }
                ],
            }
        ]

    for chap_idx, chap_info in enumerate(chapters_data, start=1):
        chapter_title = chap_info["chapter"]
        # Check if chapter exists for this course
        chapter_name = frappe.db.get_value(
            "Course Chapter",
            {"course": lms_course_name, "title": chapter_title},
            "name",
        )
        if not chapter_name:
            chapter_doc = frappe.new_doc("Course Chapter")
            chapter_doc.course = lms_course_name
            chapter_doc.title = chapter_title
            chapter_doc.insert(ignore_permissions=True)
            chapter_name = chapter_doc.name

            # Add to LMS Course chapters table if not already added
            if not frappe.db.exists(
                "Chapter Reference",
                {"parent": lms_course_name, "chapter": chapter_name},
            ):
                course_record = frappe.get_doc("LMS Course", lms_course_name)
                course_record.append("chapters", {"chapter": chapter_name})
                course_record.save(ignore_permissions=True)

        for lesson_idx, lesson_info in enumerate(chap_info.get("lessons", []), start=1):
            lesson_title = lesson_info["title"]
            if not frappe.db.exists(
                "Course Lesson",
                {"course": lms_course_name, "chapter": chapter_name, "title": lesson_title},
            ):
                lesson_doc = frappe.new_doc("Course Lesson")
                lesson_doc.course = lms_course_name
                lesson_doc.chapter = chapter_name
                lesson_doc.title = lesson_title
                lesson_doc.body = lesson_info.get("body", "")
                lesson_doc.include_in_preview = 1 if lesson_idx == 1 else 0
                lesson_doc.insert(ignore_permissions=True)

                # Link in chapter lessons table
                if not frappe.db.exists(
                    "Lesson Reference",
                    {"parent": chapter_name, "lesson": lesson_doc.name},
                ):
                    chap_rec = frappe.get_doc("Course Chapter", chapter_name)
                    chap_rec.append("lessons", {"lesson": lesson_doc.name})
                    chap_rec.save(ignore_permissions=True)


def sync_course_enrollment_to_lms(doc, method=None):
    """Triggered on Course Enrollment insertion/update."""
    if "lms" not in frappe.get_installed_apps():
        return

    student = frappe.get_doc("Student", doc.student)
    user = student.user or student.student_email_id
    if not user or not frappe.db.exists("User", user):
        return

    lms_course = get_lms_course_for_education_course(doc.course)
    if not lms_course:
        lms_course = sync_course_to_lms(doc.course)

    if not lms_course:
        return

    if not frappe.db.exists("LMS Enrollment", {"member": user, "course": lms_course}):
        enrollment = frappe.new_doc("LMS Enrollment")
        enrollment.member = user
        enrollment.course = lms_course
        enrollment.member_type = "Student"
        enrollment.insert(ignore_permissions=True)


def remove_course_enrollment_from_lms(doc, method=None):
    """Triggered on Course Enrollment deletion."""
    if "lms" not in frappe.get_installed_apps():
        return

    student = frappe.get_doc("Student", doc.student)
    user = student.user or student.student_email_id
    if not user:
        return

    lms_course = get_lms_course_for_education_course(doc.course)
    if not lms_course:
        return

    enrollments = frappe.get_all(
        "LMS Enrollment",
        filters={"member": user, "course": lms_course},
        pluck="name",
    )
    for enr in enrollments:
        frappe.delete_doc("LMS Enrollment", enr, ignore_permissions=True)


def sync_program_enrollment_to_lms(doc, method=None):
    """Triggered on Program Enrollment insertion/update."""
    if "lms" not in frappe.get_installed_apps():
        return

    student = frappe.get_doc("Student", doc.student)
    user = student.user or student.student_email_id
    if not user or not frappe.db.exists("User", user):
        return

    # Ensure LMS Program exists
    lms_prog = frappe.db.get_value("LMS Program", {"title": doc.program}, "name")
    if not lms_prog and frappe.db.exists("LMS Program", doc.program):
        lms_prog = doc.program

    if not lms_prog:
        lms_p = frappe.new_doc("LMS Program")
        lms_p.title = doc.program
        lms_p.published = 1
        lms_p.insert(ignore_permissions=True)
        lms_prog = lms_p.name

    # Add member to LMS Program
    if not frappe.db.exists(
        "LMS Program Member",
        {"parent": lms_prog, "member": user},
    ):
        prog_doc = frappe.get_doc("LMS Program", lms_prog)
        prog_doc.append("program_members", {"member": user})
        prog_doc.save(ignore_permissions=True)

    # Enroll in all program courses
    courses = frappe.get_all(
        "Program Course",
        filters={"parent": doc.program},
        pluck="course",
    )
    for c in courses:
        lms_c = get_lms_course_for_education_course(c) or sync_course_to_lms(c)
        if lms_c:
            # Ensure in LMS Program courses
            if not frappe.db.exists(
                "LMS Program Course",
                {"parent": lms_prog, "course": lms_c},
            ):
                prog_doc = frappe.get_doc("LMS Program", lms_prog)
                prog_doc.append("program_courses", {"course": lms_c})
                prog_doc.save(ignore_permissions=True)

            # Ensure LMS Enrollment
            if not frappe.db.exists(
                "LMS Enrollment",
                {"member": user, "course": lms_c},
            ):
                frappe.get_doc(
                    {
                        "doctype": "LMS Enrollment",
                        "member": user,
                        "course": lms_c,
                        "member_type": "Student",
                    }
                ).insert(ignore_permissions=True)


def sync_student_group_to_lms(doc, method=None):
    """Triggered on Student Group insertion/update."""
    if "lms" not in frappe.get_installed_apps():
        return

    group_name = doc.student_group_name or doc.name
    batch_name = frappe.db.get_value("LMS Batch", {"title": group_name}, "name")
    if not batch_name:
        lms_batch = frappe.new_doc("LMS Batch")
        lms_batch.title = group_name
        lms_batch.start_date = frappe.utils.today()
        lms_batch.medium = "Offline"
        lms_batch.description = f"Batch class group for {group_name}"

        # Link courses
        course_names = []
        if doc.program:
            course_names = frappe.get_all(
                "Program Course", filters={"parent": doc.program}, pluck="course"
            )
        for c in course_names:
            lms_c = get_lms_course_for_education_course(c) or sync_course_to_lms(c)
            if lms_c:
                lms_batch.append("courses", {"course": lms_c})

        lms_batch.insert(ignore_permissions=True)
        batch_name = lms_batch.name

    # Enroll students
    for st_row in doc.students:
        user_id = frappe.db.get_value("Student", st_row.student, "user")
        if user_id and frappe.db.exists("User", user_id):
            if not frappe.db.exists(
                "LMS Batch Enrollment",
                {"member": user_id, "batch": batch_name},
            ):
                frappe.get_doc(
                    {
                        "doctype": "LMS Batch Enrollment",
                        "member": user_id,
                        "batch": batch_name,
                    }
                ).insert(ignore_permissions=True)


def sync_all_education_lms():
    """Run full synchronization of Education data into LMS."""
    if "lms" not in frappe.get_installed_apps():
        return

    # 1. Ensure Teachers have Course Creator role
    instructors = frappe.get_all("Instructor", fields=["name", "employee"])
    for ins in instructors:
        if ins.employee:
            user_id = frappe.db.get_value("Employee", ins.employee, "user_id")
            if user_id and frappe.db.exists("User", user_id):
                u = frappe.get_doc("User", user_id)
                roles = [r.role for r in u.roles]
                added = False
                for role_to_add in ("Course Creator", "Instructor"):
                    if role_to_add not in roles and frappe.db.exists("Role", role_to_add):
                        u.append("roles", {"role": role_to_add})
                        added = True
                if added:
                    u.save(ignore_permissions=True)

    # 2. Sync All Courses
    courses = frappe.get_all("Course", fields=["name", "course_name"])
    for c in courses:
        sync_course_to_lms(c.name)

    # 3. Sync Programs
    programs = frappe.get_all("Program", fields=["name", "program_name"])
    for p in programs:
        prog_courses = frappe.get_all(
            "Program Course", filters={"parent": p.name}, pluck="course"
        )
        lms_prog = frappe.db.get_value("LMS Program", {"title": p.name}, "name")
        if not lms_prog:
            lp = frappe.new_doc("LMS Program")
            lp.title = p.name
            lp.published = 1
            for pc in prog_courses:
                lms_c = get_lms_course_for_education_course(pc) or sync_course_to_lms(pc)
                if lms_c:
                    lp.append("program_courses", {"course": lms_c})
            lp.insert(ignore_permissions=True)
            lms_prog = lp.name
        else:
            lp = frappe.get_doc("LMS Program", lms_prog)
            existing_c = [row.course for row in lp.program_courses]
            changed = False
            for pc in prog_courses:
                lms_c = get_lms_course_for_education_course(pc) or sync_course_to_lms(pc)
                if lms_c and lms_c not in existing_c:
                    lp.append("program_courses", {"course": lms_c})
                    changed = True
            if changed:
                lp.save(ignore_permissions=True)

    # 4. Sync Student Groups to Batches
    groups = frappe.get_all("Student Group", pluck="name")
    for g in groups:
        g_doc = frappe.get_doc("Student Group", g)
        sync_student_group_to_lms(g_doc)

    # 5. Sync Course Enrollments to LMS Enrollments
    enrollments = frappe.get_all("Course Enrollment", fields=["student", "course"])
    for enr in enrollments:
        student_user = frappe.db.get_value("Student", enr.student, "user")
        if not student_user or not frappe.db.exists("User", student_user):
            continue

        lms_c = get_lms_course_for_education_course(enr.course) or sync_course_to_lms(enr.course)
        if lms_c:
            if not frappe.db.exists(
                "LMS Enrollment",
                {"member": student_user, "course": lms_c},
            ):
                frappe.get_doc(
                    {
                        "doctype": "LMS Enrollment",
                        "member": student_user,
                        "course": lms_c,
                        "member_type": "Student",
                    }
                ).insert(ignore_permissions=True)

    # 6. Sync Program Enrollments
    penrs = frappe.get_all("Program Enrollment", fields=["name", "student", "program"])
    for pe in penrs:
        student_user = frappe.db.get_value("Student", pe.student, "user")
        if not student_user or not frappe.db.exists("User", student_user):
            continue
        lms_prog = frappe.db.get_value("LMS Program", {"title": pe.program}, "name")
        if lms_prog:
            if not frappe.db.exists(
                "LMS Program Member",
                {"parent": lms_prog, "member": student_user},
            ):
                lp = frappe.get_doc("LMS Program", lms_prog)
                lp.append("program_members", {"member": student_user})
                lp.save(ignore_permissions=True)
