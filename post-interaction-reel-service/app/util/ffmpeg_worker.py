import ffmpeg
import os
import tempfile
from typing import Tuple, Optional
from app.config.settings import settings

class FFmpegWorker:
    def __init__(self):
        self.max_duration = settings.MAX_REEL_DURATION
    
    def process_video(self, input_path: str, output_path: str) -> bool:
        """Process video: compress, convert format, and generate thumbnail"""
        try:
            # Get video info
            probe = ffmpeg.probe(input_path)
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            duration = float(video_info['duration'])
            
            # Check duration limit
            if duration > self.max_duration:
                raise ValueError(f"Video duration ({duration}s) exceeds maximum allowed duration ({self.max_duration}s)")
            
            # Process video: compress and convert to MP4
            (
                ffmpeg
                .input(input_path)
                .output(
                    output_path,
                    vcodec='libx264',
                    acodec='aac',
                    preset='medium',
                    crf=23,
                    maxrate='2M',
                    bufsize='4M',
                    pix_fmt='yuv420p'
                )
                .overwrite_output()
                .run(quiet=True)
            )
            
            return True
        except Exception as e:
            print(f"FFmpeg processing error: {e}")
            return False
    
    def generate_thumbnail(self, video_path: str, thumbnail_path: str, time_offset: float = 1.0) -> bool:
        """Generate thumbnail from video at specified time offset"""
        try:
            (
                ffmpeg
                .input(video_path, ss=time_offset)
                .output(thumbnail_path, vframes=1, format='image2')
                .overwrite_output()
                .run(quiet=True)
            )
            return True
        except Exception as e:
            print(f"Thumbnail generation error: {e}")
            return False
    
    def extract_audio(self, video_path: str, audio_path: str) -> bool:
        """Extract audio from video"""
        try:
            (
                ffmpeg
                .input(video_path)
                .output(audio_path, acodec='mp3', ac=2, ar='44100')
                .overwrite_output()
                .run(quiet=True)
            )
            return True
        except Exception as e:
            print(f"Audio extraction error: {e}")
            return False
    
    def get_video_info(self, video_path: str) -> dict:
        """Get video information"""
        try:
            probe = ffmpeg.probe(video_path)
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            audio_info = next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)
            
            return {
                'duration': float(video_info['duration']),
                'width': int(video_info['width']),
                'height': int(video_info['height']),
                'fps': eval(video_info['r_frame_rate']),
                'has_audio': audio_info is not None,
                'codec': video_info['codec_name']
            }
        except Exception as e:
            print(f"Video info extraction error: {e}")
            return {}
    
    def process_reel_video(self, input_path: str) -> Tuple[Optional[str], Optional[str], Optional[str], dict]:
        """Process reel video: compress, generate thumbnail, extract audio"""
        try:
            # Create temporary files
            with tempfile.TemporaryDirectory() as temp_dir:
                video_output = os.path.join(temp_dir, "processed_video.mp4")
                thumbnail_output = os.path.join(temp_dir, "thumbnail.jpg")
                audio_output = os.path.join(temp_dir, "audio.mp3")
                
                # Get video info
                video_info = self.get_video_info(input_path)
                
                # Process video
                if not self.process_video(input_path, video_output):
                    return None, None, None, {}
                
                # Generate thumbnail
                thumbnail_generated = self.generate_thumbnail(video_output, thumbnail_output)
                
                # Extract audio if present
                audio_generated = False
                if video_info.get('has_audio', False):
                    audio_generated = self.extract_audio(video_output, audio_output)
                
                # Upload processed files
                s3_helper = S3Helper()
                
                # Upload video
                with open(video_output, 'rb') as f:
                    video_url = s3_helper.upload_file(f, "processed_video.mp4", "video/mp4")
                
                # Upload thumbnail
                thumbnail_url = None
                if thumbnail_generated:
                    with open(thumbnail_output, 'rb') as f:
                        thumbnail_url = s3_helper.upload_file(f, "thumbnail.jpg", "image/jpeg")
                
                # Upload audio
                audio_url = None
                if audio_generated:
                    with open(audio_output, 'rb') as f:
                        audio_url = s3_helper.upload_file(f, "audio.mp3", "audio/mpeg")
                
                return video_url, thumbnail_url, audio_url, video_info
                
        except Exception as e:
            print(f"Reel processing error: {e}")
            return None, None, None, {}

