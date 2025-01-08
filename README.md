Quick Playblast Addon for Blender
Overview
Quick Playblast is a Blender addon designed to streamline the process of creating viewport animation previews (playblasts). With support for customizable settings and optional audio, this tool is ideal for animators who want fast and efficient previews of their work without diving into complex rendering pipelines.

Features
Create quick viewport animation previews directly from Blender.
Support for multiple output formats:
AVI JPEG
AVI Raw
MP4 (H264)
JPEG image sequence
PNG image sequence
Include scene audio in your playblasts with adjustable volume settings.
Customize settings:
Resolution percentage
Frame range (scene default or custom)
Viewport overlays and background visibility
Scene camera or viewport view
Metadata stamps (frame numbers, etc.)
Automatic organization of playblast outputs with timestamps for easy management.
Installation
Download the addon file (playblast.py) from this repository.
Open Blender.
Go to Edit > Preferences > Add-ons.
Click Install..., then select the playblast.py file.
Enable the addon by checking the box next to Quick Playblast.
Access the addon from the 3D Viewport Sidebar under the Tool tab.
How to Use
Navigate to View3D > Sidebar > Tool > Playblast in Blender.
Customize the settings in the addon panel:
Choose output format and resolution.
Specify frame range and audio options.
Toggle viewport overlays, background, and camera settings.
Click Capture Playblast to generate your preview.
The playblast file will be saved in the specified output directory.
Requirements
Blender Version: 3.6.0 or later
Known Limitations
Audio is not supported for AVI formats or image sequences.
Ensure your output directory is writable to avoid file saving errors.
Contribution
Contributions are welcome! If you'd like to suggest improvements, report bugs, or add new features:

Fork this repository.
Create a new branch for your changes.
Submit a pull request.
License
This addon is distributed under the MIT License. Feel free to use, modify, and share it.
