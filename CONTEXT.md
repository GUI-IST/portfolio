# CONTEXT.md: Guilherme Candeias Martins portfolio

Facts the website is to be built from. Everything here was confirmed by the site's subject. Do not add facts that are not in this file. Facts marked *(as of Nov 2026)* are time-sensitive.

---

## 1. The site

- **What it is:** the personal portfolio website of **Guilherme Candeias Martins**. It is a full rebuild of the existing portfolio in this repository.
- **Who it serves:**
  - Industry recruiters and hiring managers (semiconductor, test & characterization, quantum hardware)
  - Companies or groups that could host his TU Delft industry internship or MSc thesis
  - Academic research groups
  - His general and personal network
- **Primary visitor action:** **send him an email** (to the TU Delft address below). This is the main call to action.
- **Languages:** English and Portuguese, with an **EN | PT** toggle.
- **Sections, in order:** About · Education · Experience · Projects & Achievements · Skills & Languages · Volunteering · Hobbies · Contact
- **Experience depth:** each role shows a short **summary by default**. The full technical detail sits behind an expandable "more" control, for visitors who want it.
- **Images to reuse from the repo:**
  - `perfil.jpg` (profile photo)
  - Organization logos: `IST_Logo.png` (Instituto Superior Técnico), `it.png` (Instituto de Telecomunicações), `AEIST.png`, `golp.png`, `silicongate.png`
  - Hobby photos: `guitar.jpg`, `gym.JPG`, `travel.png`
  - `almond_blossoms.png` (artwork; about 23 MB)
  - There is no TU Delft or Celera Semiconductor logo in the repo yet.

---

## 2. Identity & contact

- **Name:** Guilherme Candeias Martins
- **Headline:** Electrical and Computer Engineer · MSc Electrical Engineering (Microelectronics, quantum themed), TU Delft
- **Location:** Based in Delft, the Netherlands (since August 2026) · from Cascais, Portugal
- **Age:** 22 *(as of Nov 2026)*
- **Public contact (only these):**
  - Email: **gcandeiasmarti@tudelft.nl**
  - LinkedIn: https://www.linkedin.com/in/guilherme-candeias-martins/
- **Not to be published:** personal Gmail address, phone number.

### About (substance)
- Electrical and Computer Engineer with a BSc from Instituto Superior Técnico, now pursuing an MSc in Electrical Engineering at TU Delft (Microelectronics track, quantum themed).
- Interested in where hardware, physics and computation meet: quantum engineering, semiconductors and microelectronics.
- Experience in semiconductor testing in industry and in quantum simulation research.
- Motivated by challenging problems, multidisciplinary environments, and turning theoretical knowledge into practical solutions while growing as an engineer and as a person.

---

## 3. Education

### Technische Universiteit Delft (TU Delft): Delft, the Netherlands
- **MSc Electrical Engineering**, Microelectronics track, quantum themed
- **Aug 2026 – Present**
- **Example courses:** Electronic Device Fundamentals, Semiconductor Devices and Circuits for Quantum, Advanced Semiconductor Devices, Microfabrication Fundamentals, Fundamentals of Photonic Integrated Circuits, Superconducting Quantum Sensors for Astronomy
- The programme's final year is built around industry experience.
- Link: TU Delft MSc Electrical Engineering programme page (**URL to be supplied**)

### Instituto Superior Técnico (IST), University of Lisbon: Lisbon, Portugal
- **BSc Electrical and Computer Engineering**
- **Sep 2022 – Jul 2025** · Final grade **16/20**
- Relevant coursework: Microelectronics, Circuit Analysis, Propagation and Radiation of Electromagnetic Waves, Telecommunications, Computer Architecture, Algorithms and Data Structures
- Link: IST BSc Electrical and Computer Engineering programme page (**URL to be supplied**)

### Liceu São João do Estoril (São João do Estoril High School): Cascais, Portugal
- **2019 – 2022**
- Class Representative & Honor Student · Average grade **19/20**

### Amor de Deus School: Cascais, Portugal
- **Before 2019**
- Honor Student

---

## 4. Experience

### Test Engineer Intern, Test & Laboratory team: Lisbon, Portugal
- **Aug 2025 – Jul 2026**, full time
  - **SiliconGate:** Aug 2025 – Jun 2026
  - **Celera Semiconductor:** Jun 2026 – Jul 2026

**Summary (shown by default):**
Validation and characterization of semiconductor IP devices for power management: developing and automating test setups, performing hardware measurements, soldering and assembling circuits, and writing code to control and analyze test systems.

**Full detail (behind "more"):**
- About **1,500 hours** of hands-on lab work.
- Characterized and validated power-management semiconductor IP on silicon: startup sequencing, line transients, AC and DC measurements, and temperature-dependent tests with a thermal stream system.
- Powered fragile engineering samples safely: sequenced supplies to each block of the IC through relays and programmable sources, sourcing and measuring with Keithley SourceMeter units (SMUs).
- Trimmed on-chip clock, temperature, voltage and current settings through JTAG/IJTAG, and controlled electronic and programmable loads during measurements.
- Wrote Python drivers for two arbitrary waveform generators from their programming manuals (SCPI over GPIB with PyVISA): binary waveform upload, multi-segment sequences with trigger and marker logic, hardware limit checks and input validation, and a GUI instrument panel. The drivers are integrated into the company's automated test framework.
- Adapted the team's existing Python data processing and visualization code (pandas, Matplotlib) to each new instrument and sample, keeping results organized and consistent.
- Hand-soldered and assembled test circuits, including small SMD components under a microscope.
- Used Git daily for all driver and test code.
- **Equipment:** Keithley SourceMeters (SMU), LCR meter, laboratory power amplifiers, oscilloscopes and current probes, arbitrary waveform and function generators, frequency counter, signal source analyzer, programmable DC power supplies, electronic and programmable loads, battery chargers, relays, JTAG/IJTAG, thermal stream system.

### Research Intern, GOLP (Group for Lasers and Plasmas), IPFN: Lisbon, Portugal
- **Sep 2025 – Mar 2026** · Instituto Superior Técnico, University of Lisbon
- Research on **quantum simulation of Maxwell's equations**, at the intersection of quantum physics and electromagnetism.
- Deepened understanding of Hamiltonian mechanics, quantum systems and numerical modeling, and of how fundamental physics can be simulated and experimentally studied.

### Instituto de Telecomunicações, Quantum and Photonics Department: Lisbon, Portugal
- **Feb 2025 – Jul 2025** · Instituto Superior Técnico, University of Lisbon
- Attended weekly department meetings, tracking 8 research projects, taking notes, and learning about real-world applications of quantum and photonics technologies.

### Business Relations Collaborator, Students' Association of IST (AEIST): Lisbon, Portugal
- **Oct 2024 – Sep 2025**
- Developed and nurtured relationships with external organizations, securing funding and sponsorships for AEIST's activities.
- Skills gained: partnership development, communication, project management, sales negotiation.

---

## 5. Projects & Achievements

### Sentinel: Anti-Drone Detection System for Communication Jamming
- **Dec 2024 – Jul 2025** · Lisbon, Portugal
- BSc final-year project at Instituto Superior Técnico. **Guilherme led the team.**
- Uses machine learning to identify drones and distinguish them from other flying objects, to improve security in sensitive areas.
- Developed in collaboration with the **Portuguese Air Force, Thales and Mauser**.
- Goal: give security forces a reliable, efficient tool to detect and respond to drone threats.
- Project website: https://sentinel-anti-drone.vercel.app/

### Erasmus+ SINCRON SUSTENABIL: Romania
- **Oct 2025**
- One-week sustainability programme in the Apuseni Mountains, in a diverse multinational team.
- Hands-on eco-friendly practices: solar cooking, rainwater harvesting, composting, natural-material construction.
- Strengthened intercultural communication, collaboration and problem-solving.

### Scholarships & awards
- IST Academic Merit Diploma: 2022/2023
- BONDALTI & Fundação Amélia de Mello Scholarship: 2023/2024 and 2024/2025
- Santander Scholarship (Técnico Santander): 2022/2023
- School Merit Scholarship, Alcabideche Parish: 2022
- School Merit Award, Cascais Municipal Council: 2022

---

## 6. Skills & Languages

- **Programming:** Python (pandas, Matplotlib, PyVISA), C, C++, Java, Assembly, MATLAB, Qiskit
- **Tools:** Git, Cadence Virtuoso (Spectre), LaTeX (Overleaf), Excel
- **Lab:** SMUs, LCR meter, oscilloscopes, waveform generators, programmable supplies and loads, JTAG/IJTAG, thermal stream, soldering and microscope work
- **Electrical engineering knowledge:** Microelectronics, Propagation and Radiation of Electromagnetic Waves, Telecommunications, Circuit Analysis, Computer Architecture, Algorithms and Data Structures, Differential and Integral Calculus, Linear Algebra
- **Soft skills:** Leadership, communication, conflict resolution, teamwork, proactivity, analytical thinking, adaptability and flexibility, problem solving, learning agility
- **Languages:** Portuguese (native) · English (proficient, C1) · Spanish (fluent)

---

## 7. Volunteering

### Volunteer Tutor: Cascais, Portugal
- **2024 – 2026**
- Gave educational support to around 15 children, from preschool to secondary school, adapting explanations of fundamental concepts to each child's level.
- Discovered a passion for teaching, which played a significant role in his decision to take a gap year, both to explore new experiences and to dedicate time to sharing knowledge and helping others grow academically.

### Volunteer, Cascais Jovem: Cascais, Portugal
- **2021 – 2026**
- Supported events and community programmes, including:
  - Occupational Safety and Health Conference: logistical support and event organization
  - Children's Festival: engaging with children and families
  - Safe Beaches Initiative: promoting beach safety and environmental awareness
  - Portuguese elections: helping organize and coordinate electoral processes
- Developed teamwork, communication and problem-solving skills, and gained experience in event support and community engagement.

---

## 8. Hobbies

- **Guitar:** plays in his own band, with 6 concerts
- **Travel:** has visited 18 countries on 4 continents
- **Physical exercise:** climbing, gym, padel, sailing

---

## 9. Open items

- Exact URL of the TU Delft MSc Electrical Engineering programme page
- Exact URL of the IST BSc Electrical and Computer Engineering programme page
