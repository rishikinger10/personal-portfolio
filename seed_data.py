"""
One-off script to load my resume content into sqlite.
Run it again anytime, it wipes and reinserts (except messages).
"""

from database import get_conn, init_db

profile = {
    "full_name": "Rishi Kinger",
    "headline": "Electronics & Instrumentation Engineer",
    "tagline": "Embedded Systems · Computer Vision · Linux Internals",
    "email": "rishikinger10@gmail.com",
    "phone": "+91 9916947028",
    "location": "Bengaluru, India",
    "about": (
        "I'm a 2nd year B.Tech student at VIT Vellore who likes working close to the metal. "
        "Most of my projects live somewhere between hardware and software: writing Linux "
        "device drivers, getting YOLOv8 to run in real time on a Raspberry Pi, or designing "
        "my own telemetry protocol over raw TCP sockets. I care about making things work "
        "on constrained hardware, and I debug with dmesg and Wireshark more than with print statements."
    ),
    "education": "Vellore Institute of Technology (VIT), Vellore. B.Tech, Electronics and Instrumentation Engineering (2024 to 2028)",
    "cgpa": "8.43 / 10",
}

skills = [
    ("Languages", "C, C++, Python"),
    ("Core CS", "Data Structures & Algorithms, OOP, Operating Systems, Computer Networks"),
    ("Networking", "TCP/IP, OSI Model, Routing & Switching, HTTP/HTTPS, DNS, DHCP"),
    ("AI / Vision", "YOLOv8, OpenCV"),
    ("Embedded", "Raspberry Pi 5, Arduino UNO/Nano, GPIO, MPU6050, HC-SR04"),
    ("Tools", "Git, GitHub, Linux, VS Code, Arduino IDE, Wireshark"),
    ("Electronics", "Digital Electronics, Analog Circuits"),
]

experience = [
    {
        "role": "Summer Intern",
        "org": "Wipro GE Healthcare",
        "period": "June to July 2026",
        "bullets": "\n".join([
            "Built an AI powered surveillance application with Python, OpenCV, YOLOv8 and a Raspberry Pi 5.",
            "Integrated live CCTV streams and wrote ROI based object monitoring for real time event detection.",
            "Squeezed better performance out of constrained hardware through model optimization and smarter video processing.",
            "Debugged Linux software, camera interfaces, and the boundary between hardware and software in general.",
        ]),
    },
    {
        "role": "Makeathon Coordinator",
        "org": "VIT Vellore",
        "period": "2024",
        "bullets": "\n".join([
            "Handled participant coordination, access control and live queries during the event.",
            "Organised hardware distribution and helped teams with soldering and technical setup.",
        ]),
    },
]

projects = [
    {
        "title": "AI Powered CCTV Theft Detection",
        "summary": "Theft detection in real time on a Raspberry Pi 5, with YOLOv8 Nano and OpenCV watching ROIs on live CCTV feeds.",
        "stack": "Python, Raspberry Pi 5, OpenCV, YOLOv8, Linux",
        "highlights": "\n".join([
            "ROI based object monitoring to flag potential theft events on live video",
            "Tuned for real time inference on constrained hardware with the YOLOv8 Nano model",
            "Debugged camera integration and streaming issues on the Linux deployment",
        ]),
        "sort_order": 1,
    },
    {
        "title": "Linux Device Driver for Hardware Events",
        "summary": "A character device driver in C that bridges GPIO hardware on a Pi 5 with user space.",
        "stack": "C, Linux Kernel Modules, GPIO, sysfs",
        "highlights": "\n".join([
            "Implemented file_operations so user space can talk to the kernel module",
            "GPIO interrupts for hardware events, device info exposed through sysfs",
            "Companion app in user space processes events in real time, debugged with dmesg and printk",
        ]),
        "sort_order": 2,
    },
    {
        "title": "Custom Socket Telemetry Protocol",
        "summary": "My own lightweight application layer protocol over TCP, with a server that handles multiple clients and a Pi client.",
        "stack": "C, Linux, TCP/IP, Sockets, Wireshark",
        "highlights": "\n".join([
            "Packet formatting, sequence handling and heartbeat messages for reliability",
            "Server handling multiple clients plus a Raspberry Pi client exchanging telemetry in real time",
            "Verified protocol behaviour on the wire with Wireshark captures",
        ]),
        "sort_order": 3,
    },
    {
        "title": "Hand Tremor Detector (Parkinson's)",
        "summary": "Arduino and MPU6050 system that watches accelerometer and gyro data for abnormal tremor patterns.",
        "stack": "Arduino UNO, MPU6050, Embedded C",
        "highlights": "\n".join([
            "Threshold detection logic in Embedded C for continuous monitoring",
            "Live acquisition of accel and gyro data over I2C",
            "Serial comms used for live testing and debugging",
        ]),
        "sort_order": 4,
    },
]


def run():
    init_db()
    conn = get_conn()
    cur = conn.cursor()

    # wipe everything except contact messages
    for t in ("profile", "projects", "skills", "experience"):
        cur.execute(f"DELETE FROM {t}")

    cur.execute(
        """INSERT INTO profile
           (id, full_name, headline, tagline, email, phone, location, about, education, cgpa)
           VALUES (1,?,?,?,?,?,?,?,?,?)""",
        (profile["full_name"], profile["headline"], profile["tagline"],
         profile["email"], profile["phone"], profile["location"],
         profile["about"], profile["education"], profile["cgpa"]),
    )

    for cat, items in skills:
        cur.execute("INSERT INTO skills (category, items) VALUES (?,?)", (cat, items))

    for e in experience:
        cur.execute(
            "INSERT INTO experience (role, org, period, bullets) VALUES (?,?,?,?)",
            (e["role"], e["org"], e["period"], e["bullets"]),
        )

    for p in projects:
        cur.execute(
            "INSERT INTO projects (title, summary, stack, highlights, sort_order) VALUES (?,?,?,?,?)",
            (p["title"], p["summary"], p["stack"], p["highlights"], p["sort_order"]),
        )

    conn.commit()
    conn.close()
    print("seeded: 1 profile, %d skills, %d projects, %d experience rows"
          % (len(skills), len(projects), len(experience)))


if __name__ == "__main__":
    run()
