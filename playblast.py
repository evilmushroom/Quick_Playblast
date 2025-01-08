
# playblast.py
# Blender Addon: Quick Playblast
# Author: Evilmushroom
# Description: This addon provides a quick way to create viewport animation previews (playblasts) with optional audio.
# Version: 1.1
# Blender Compatibility: 3.6.0+

bl_info = {
    "name": "Quick Playblast",
    "author": "Evilmushroom",
    "version": (1, 1),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Tool > Playblast",
    "description": "Create quick viewport animation previews with audio",
    "doc_url": "",
}

import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty, 
                      CollectionProperty, FloatProperty, EnumProperty)
from bpy.types import Panel, Operator, PropertyGroup, UIList, Menu
from mathutils import Vector
import os
from datetime import datetime

FILE_FORMATS = [
    ('AVI_JPEG', "AVI JPEG", "AVI video with JPEG encoding"),
    ('AVI_RAW', "AVI Raw", "AVI video without encoding"),
    ('FFMPEG', "MP4 (H264)", "MPEG4 video with H264 encoding"),
    ('JPEG', "JPEG Sequence", "Sequence of JPEG images"),
    ('PNG', "PNG Sequence", "Sequence of PNG images")
]


# This class defines the settings for the Playblast addon.
# It stores various properties for output configuration, including file format, resolution, frame range, etc.
class PLAYBLAST_PG_settings(PropertyGroup):

    output_path: StringProperty(
        name="Output Path",
        default="//playblast",
        subtype='DIR_PATH',
        description="Directory to save playblast files"
    )
    file_format: EnumProperty(
        name="Format",
        items=FILE_FORMATS,
        default='FFMPEG',
        description="Output file format"
    )
    use_scene_frames: BoolProperty(
        name="Use Scene Frame Range",
        default=True,
        description="Use scene's start and end frames"
    )
    start_frame: IntProperty(
        name="Start Frame",
        default=1,
        min=0
    )
    end_frame: IntProperty(
        name="End Frame",
        default=250,
        min=0
    )
    resolution_percentage: IntProperty(
        name="Resolution %",
        default=50,
        min=1,
        max=100,
        description="Percentage of current viewport resolution"
    )
    use_scene_camera: BoolProperty(
        name="Use Scene Camera",
        default=False,
        description="Use active scene camera instead of current viewport"
    )
    use_overlays: BoolProperty(
        name="Show Overlays",
        default=True,
        description="Show viewport overlays in playblast"
    )
    show_background: BoolProperty(
        name="Show Background",
        default=True,
        description="Show world background"
    )
    use_stamp: BoolProperty(
        name="Use Stamp",
        default=True,
        description="Add frame number and other info overlay"
    )
    # New audio properties
    include_audio: BoolProperty(
        name="Include Audio",
        default=True,
        description="Include scene audio in the playblast"
    )
    audio_volume: FloatProperty(
        name="Volume",
        default=1.0,
        min=0.0,
        max=1.0,
        description="Audio volume for playblast"
    )


# This operator handles the actual playblast capture process.
# It manages settings, configures the viewport, and restores everything after the process.
class PLAYBLAST_OT_preview(Operator):

    bl_idname = "playblast.capture"
    bl_label = "Capture Playblast"
    bl_description = "Capture viewport preview animation"
    
    def get_output_path(self, context):
        base_path = bpy.path.abspath(context.scene.playblast.output_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        os.makedirs(base_path, exist_ok=True)
        
        if context.scene.playblast.file_format in {'JPEG', 'PNG'}:
            folder_name = f"playblast_{timestamp}"
            output_path = os.path.join(base_path, folder_name)
            os.makedirs(output_path, exist_ok=True)
            return os.path.join(output_path, "frame_####")
        else:
            ext = ".mp4" if context.scene.playblast.file_format == 'FFMPEG' else ".avi"
            return os.path.join(base_path, f"playblast_{timestamp}{ext}")

    
    # Main function that gets executed when the user runs the playblast operator.
    # Sets up rendering and restores original settings afterward.
    def execute(self, context):

        scene = context.scene
        playblast = scene.playblast
        
        # Store original render and audio settings
        original_settings = {
            'file_format': scene.render.image_settings.file_format,
            'ffmpeg_constant_rate_factor': scene.render.ffmpeg.constant_rate_factor,
            'resolution_percentage': scene.render.resolution_percentage,
            'use_stamp': scene.render.use_stamp,
            'frame_start': scene.frame_start,
            'frame_end': scene.frame_end,
            'filepath': scene.render.filepath,
            # Audio settings
            'audio_codec': scene.render.ffmpeg.audio_codec,
            'audio_bitrate': scene.render.ffmpeg.audio_bitrate,
            'audio_volume': scene.render.ffmpeg.audio_volume,
            'use_audio': scene.render.ffmpeg.audio_codec != 'NONE'
        }
        
        # Get active 3D viewport
        area = None
        for a in context.screen.areas:
            if a.type == 'VIEW_3D':
                area = a
                break
                
        if not area:
            self.report({'ERROR'}, "No 3D Viewport found!")
            return {'CANCELLED'}
            
        # Store viewport settings
        space = area.spaces.active
        region3d = space.region_3d
        original_viewport = {
            'shading_type': space.shading.type,
            'overlays': space.overlay.show_overlays,
            'background': space.shading.use_scene_world,
            'view_perspective': region3d.view_perspective,
            'view_matrix': region3d.view_matrix.copy(),
            'view_distance': region3d.view_distance,
            'view_location': region3d.view_location.copy(),
            'view_rotation': region3d.view_rotation.copy()
        }
        
        try:
            scene.render.filepath = self.get_output_path(context)
            
            if playblast.file_format == 'FFMPEG':
                scene.render.image_settings.file_format = 'FFMPEG'
                scene.render.ffmpeg.format = 'MPEG4'
                scene.render.ffmpeg.codec = 'H264'
                scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
                
                # Configure audio settings for FFMPEG
                if playblast.include_audio:
                    scene.render.ffmpeg.audio_codec = 'AAC'
                    scene.render.ffmpeg.audio_bitrate = 192
                    scene.render.ffmpeg.audio_volume = playblast.audio_volume
                else:
                    scene.render.ffmpeg.audio_codec = 'NONE'
                    
            elif playblast.file_format in {'AVI_JPEG', 'AVI_RAW'}:
                scene.render.image_settings.file_format = playblast.file_format
                # Note: AVI format in Blender doesn't support audio
                if playblast.include_audio:
                    self.report({'WARNING'}, "Audio is not supported in AVI format")
            else:
                scene.render.image_settings.file_format = playblast.file_format
                # Image sequences don't support audio
                if playblast.include_audio:
                    self.report({'WARNING'}, "Audio is not supported in image sequences")
            
            if not playblast.use_scene_frames:
                scene.frame_start = playblast.start_frame
                scene.frame_end = playblast.end_frame
            
            scene.render.resolution_percentage = playblast.resolution_percentage
            scene.render.use_stamp = playblast.use_stamp
                
            # Apply viewport settings for capture
            if not playblast.use_overlays:
                space.overlay.show_overlays = False
            space.shading.use_scene_world = playblast.show_background
            
            if playblast.use_scene_camera and scene.camera:
                region3d.view_perspective = 'CAMERA'
            
            # Use OpenGL render for viewport capture
            with context.temp_override(area=area):
                bpy.ops.render.opengl(
                    animation=True,
                    render_keyed_only=False,
                    sequencer=False,
                    write_still=False,
                    view_context=True
                )
            
            self.report({'INFO'}, f"Playblast saved to: {scene.render.filepath}")
            
        finally:
            # Restore original settings
            scene.render.image_settings.file_format = original_settings['file_format']
            scene.render.ffmpeg.constant_rate_factor = original_settings['ffmpeg_constant_rate_factor']
            scene.render.resolution_percentage = original_settings['resolution_percentage']
            scene.render.use_stamp = original_settings['use_stamp']
            scene.frame_start = original_settings['frame_start']
            scene.frame_end = original_settings['frame_end']
            scene.render.filepath = original_settings['filepath']
            
            # Restore audio settings
            scene.render.ffmpeg.audio_codec = original_settings['audio_codec']
            scene.render.ffmpeg.audio_bitrate = original_settings['audio_bitrate']
            scene.render.ffmpeg.audio_volume = original_settings['audio_volume']
            
            # Restore viewport settings
            space.shading.type = original_viewport['shading_type']
            space.overlay.show_overlays = original_viewport['overlays']
            space.shading.use_scene_world = original_viewport['background']
            
            # Restore view state
            region3d.view_perspective = original_viewport['view_perspective']
            region3d.view_matrix = original_viewport['view_matrix']
            region3d.view_distance = original_viewport['view_distance']
            region3d.view_location = original_viewport['view_location']
            region3d.view_rotation = original_viewport['view_rotation']
        
        return {'FINISHED'}


# This panel provides the user interface for the Playblast addon.
# It appears in the Blender 3D Viewport sidebar and allows users to configure settings and execute the playblast.
class PLAYBLAST_PT_panel(Panel):

    bl_label = "Playblast"
    bl_idname = "PLAYBLAST_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        playblast = context.scene.playblast
        
        # Output settings
        box = layout.box()
        box.label(text="Output Settings:")
        box.prop(playblast, "output_path")
        box.prop(playblast, "file_format")
        box.prop(playblast, "resolution_percentage")
        
        # Frame range settings
        box = layout.box()
        box.label(text="Frame Range:")
        box.prop(playblast, "use_scene_frames")
        if not playblast.use_scene_frames:
            row = box.row(align=True)
            row.prop(playblast, "start_frame")
            row.prop(playblast, "end_frame")
        
        # Audio settings
        box = layout.box()
        box.label(text="Audio Settings:")
        box.prop(playblast, "include_audio")
        if playblast.include_audio:
            box.prop(playblast, "audio_volume", slider=True)
            # Show warning for incompatible formats
            if playblast.file_format in {'AVI_JPEG', 'AVI_RAW', 'JPEG', 'PNG'}:
                box.label(text="Audio not supported in this format", icon='ERROR')
        
        # Viewport settings
        box = layout.box()
        box.label(text="Viewport Settings:")
        box.prop(playblast, "use_scene_camera")
        box.prop(playblast, "use_overlays")
        box.prop(playblast, "show_background")
        box.prop(playblast, "use_stamp")
        
        # Capture button
        layout.operator("playblast.capture", text="Capture Playblast", icon='RENDER_ANIMATION')

classes = (
    PLAYBLAST_PG_settings,
    PLAYBLAST_OT_preview,
    PLAYBLAST_PT_panel,
)


# Register function to make the addon accessible in Blender.
def register():

    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.playblast = bpy.props.PointerProperty(type=PLAYBLAST_PG_settings)


# Unregister function to remove the addon from Blender.
def unregister():

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.playblast

if __name__ == "__main__":
    register()
