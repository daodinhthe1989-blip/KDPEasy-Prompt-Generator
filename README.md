# KDPEasy Prompt Generator

Part of the KDPEasy Suite — free/paid tools for KDP creators.

Turns a list of scene ideas into ready-to-paste ChatGPT / image-AI prompts for activity book illustrations — black-and-white line art scenes that double as both a coloring page and a "find the hidden object" activity.

## Features (v1)
- 6 preset theme banks (Farm Animals, Ocean & Sea Life, Dinosaurs, Space & Astronauts, Jungle & Safari, Fairy Tale & Castle), each with 8 ready-made scene ideas — or write your own from scratch
- Complexity/age level: Simple (ages 4-7) or Detailed (ages 8+), changes how busy the scene description is
- Portrait or Landscape composition hint
- Choose what to hide in each scene (stars, hearts, custom item...) or leave blank to auto-vary across scenes
- One prompt generated per scene line, each shown in its own copy-to-clipboard code block
- Download all prompts as a single .txt file

## How it works
No AI is called to build the prompts — this is pure template-based text generation (like a smart mail-merge), so it's instant and free to run. The customer pastes the output prompts into ChatGPT (or another image-AI tool) themselves to actually generate the images.

## Planned for v2
- More preset theme banks based on customer demand
- A "spot the difference" / "count the objects" prompt variant
- A+ Content / marketing image prompt mode (different survey demand signal, not built yet)

## Stack
Streamlit only — no fpdf2/PyMuPDF/Pillow needed since this tool outputs text, not a PDF. No paid API, no AI calls, nothing to break on a dependency upgrade.

Password-protected, same pattern as the rest of the KDPEasy Suite. Passwords are checked against `PASSWORD_EXPIRY` in `app.py` — a value of `None` means permanent access, a date means the password stops working after that day (used for time-limited trials).
