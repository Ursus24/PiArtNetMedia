# Imports from Libraries:
import os
import cv2
import pygame

#MediaEngine from Gemini
class PiMediaEngine:

  def __init__(self):
    pygame.init()
    # Fullscreen setup utilizing Raspberry Pi hardware acceleration
    self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    self.screen_width, self.screen_height = self.screen.get_size()

    # Track current media state
    self.current_path = None
    self.media_type = None  # 'image' or 'video'

    # Image storage
    self.raw_image_surface = None

    # Video playback tracking
    self.video_capture = None
    self.video_fps = 30.0
    self.last_frame_tick = pygame.time.get_ticks()
    self.frame_accumulator = 0.0
    self.cached_video_surface = None

    # Performance optimization caches
    self.last_intensity = -1
    self._last_raw_surface = None
    self.cached_dimmed_surface = None
    self.cached_final_surface = None
    self.last_scaled_size = (0, 0)

  def show(self, media_path: str, intensity: float, playback_speed: float = 1.0):
    """Displays an image or video fullscreen with intensity (0-255)

    and playback speed control. Caches operations for Raspberry Pi performance.
    """
    if not media_path:
      return

    # 1. Switch media source if the path changes
    if media_path != self.current_path:
      self._load_media(media_path)

    # 2. Get the current raw frame surface
    raw_surface = None
    if self.media_type == "image":
      raw_surface = self.raw_image_surface
    elif self.media_type == "video":
      raw_surface = self._get_next_video_frame(playback_speed)

    if raw_surface is None:
      return

    # 3. Apply intensity (0-255) ONLY when values change
    b_val = int(max(0, min(255, intensity)))
    if b_val != self.last_intensity or raw_surface != self._last_raw_surface:
      self.cached_dimmed_surface = raw_surface.copy()
      self.cached_dimmed_surface.fill(
          (b_val, b_val, b_val), special_flags=pygame.BLEND_RGB_MULT
      )
      self.last_intensity = b_val
      self._last_raw_surface = raw_surface
      self.cached_final_surface = None  # Invalidate scale cache

    # 4. Aspect-ratio scaling (Letterboxing / Pillarboxing)
    img_width, img_height = raw_surface.get_size()
    scale = min(self.screen_width / img_width, self.screen_height / img_height)
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)

    if (
        new_width,
        new_height,
    ) != self.last_scaled_size or self.cached_final_surface is None:
      self.cached_final_surface = pygame.transform.smoothscale(
          self.cached_dimmed_surface, (new_width, new_height)
      )
      self.last_scaled_size = (new_width, new_height)

    # 5. Render to HDMI output buffer
    pos_x = (self.screen_width - new_width) // 2
    pos_y = (self.screen_height - new_height) // 2

    self.screen.fill((0, 0, 0))  # Black bars fill
    self.screen.blit(self.cached_final_surface, (pos_x, pos_y))
    pygame.display.flip()

  def _load_media(self, media_path):
    """Internal handler to switch between images and video files cleanly."""
    if self.video_capture:
      self.video_capture.release()
      self.video_capture = None

    self.current_path = media_path
    ext = os.path.splitext(media_path)[1].lower()
    video_extensions = [".mp4", ".avi", ".mov", ".mkv", ".webm"]

    if ext in video_extensions:
      self.media_type = "video"
      self.video_capture = cv2.VideoCapture(media_path)
      self.video_fps = self.video_capture.get(cv2.CAP_PROP_FPS)
      if self.video_fps <= 0:
        self.video_fps = 30.0  # Fallback
      self.frame_accumulator = 0.0
      self.last_frame_tick = pygame.time.get_ticks()
    else:
      self.media_type = "image"
      try:
        self.raw_image_surface = pygame.image.load(media_path).convert()
      except Exception as e:
        print(f"Failed to load image {media_path}: {e}")
        self.raw_image_surface = None

    # Reset caches for new asset
    self.last_intensity = -1
    self.cached_final_surface = None

  def _get_next_video_frame(self, playback_speed):
    """Calculates frame progression based on time delta and playback speed."""
    if not self.video_capture or not self.video_capture.isOpened():
      return None

    current_tick = pygame.time.get_ticks()
    dt = (current_tick - self.last_frame_tick) / 1000.0
    self.last_frame_tick = current_tick

    # If speed is greater than 0, accumulate elapsed time scaled by playback speed
    if playback_speed > 0:
      self.frame_accumulator += dt * self.video_fps * playback_speed

    frames_to_advance = int(self.frame_accumulator)
    if frames_to_advance > 0:
      self.frame_accumulator -= frames_to_advance
      ret = True
      frame = None
      for _ in range(frames_to_advance):
        ret, frame = self.video_capture.read()
        if not ret:
          # Loop video back to beginning
          self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
          ret, frame = self.video_capture.read()
          break
      if ret and frame is not None:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = frame.shape
        self.cached_video_surface = pygame.image.frombuffer(
            frame.tobytes(), (w, h), "RGB"
        )

    return self.cached_video_surface