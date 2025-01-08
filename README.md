# Quick Playblast Addon (for Blender 3.6+)

Quick Playblast is a Blender addon that allows you to quickly create viewport animation previews (playblasts) with optional audio. It’s perfect for animators who need fast, high-quality previews directly from the viewport without the hassle of complex rendering setups.

## Features

- **Fast Playblast Creation**: Generate quick animation previews directly from Blender’s viewport.
- **Multiple Output Formats**:
  - AVI JPEG
  - AVI Raw
  - MP4 (H264)
  - JPEG Image Sequence
  - PNG Image Sequence
- **Audio Support**:
  - Include scene audio in your playblast.
  - Adjust audio volume as needed.
- **Customizable Settings**:
  - **Frame Range**: Use the scene default or define a custom start and end frame.
  - **Resolution**: Set the resolution percentage for the output.
  - **Viewport Settings**: Toggle overlays, background visibility, and metadata stamps (frame numbers, etc.).
  - **Camera Options**: Use the active scene camera or the current viewport view.
  - **Automatic File Naming**: Outputs are automatically organized with timestamped filenames for easy management.

## Installation

1. **Download**  
   Download the `playblast.py` file from this repository.
   
2. **Install in Blender**  
   - Open Blender.  
   - Go to `Edit > Preferences > Add-ons`.  
   - Click `Install...` at the top-right corner of the Preferences window.  
   - Navigate to and select the `playblast.py` file.  
   - Enable the addon by checking the box next to "Quick Playblast" in the add-ons list.  

3. **Access the Addon**  
   - The addon will now be available in the 3D Viewport Sidebar under `Tool > Playblast`.

## Usage Instructions

1. Open the 3D Viewport Sidebar and go to `Tool > Playblast`.
2. Configure the playblast settings:
   - **Output Format**: Select MP4, AVI, or an image sequence format.
   - **Resolution**: Set the output resolution as a percentage of the viewport.
   - **Frame Range**: Use the default scene range or specify custom start and end frames.
   - **Audio Options**: Enable or disable audio and adjust its volume.
   - **Viewport Options**: Toggle overlays, metadata stamps, and background visibility.
   - **Output Path**: Define the path where the playblast will be saved.
3. Click **Capture Playblast** to create your preview.
4. Locate the playblast file in the chosen output directory.

## Requirements

- **Blender Version**: 3.6.0 or later

## Known Limitations

- Audio is not supported for AVI formats or image sequences.
- Ensure the output directory is writable to avoid file-saving errors.

## Contribution

Contributions are welcome! If you’d like to suggest improvements, report bugs, or add new features:

1. Fork this repository.
2. Create a new branch for your changes.
3. Submit a pull request.

## License

This addon is licensed under the GNU General Public License v3.
