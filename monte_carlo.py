import pygame
import sys
import random

class MonteCarloPi:
  def __init__(self, width=1000, height=1000, frame_size=700, dart_rate=5):
    self.background_color = "#1E1E2E"
    self.frame_color = "#322A40"
    self.circle_color = "#241F2E"
    self.inside_color = "#87B0F9"
    self.outside_color = "#F38BA8"
    self.font_color = "#C9BDDE"

    self.width = width
    self.height = height
    self.center_width = self.width//2
    self.center_height = self.width//2
    self.square_length = frame_size
    self.circle_radius = frame_size//2
    self.vertical_margin = 50
    self.horizontal_margin = self.center_width - (frame_size//2)
    self.center = (self.center_width, (frame_size//2) + self.vertical_margin)
    self.inside_count = 0
    self.total_sample_count = 0
    self.dart_rate = dart_rate

    pygame.init()
    pygame.font.init()
    self.display = pygame.display.set_mode((self.width, self.height))
    self.dot_surface = pygame.Surface((frame_size, frame_size), pygame.SRCALPHA)
    self.roman = pygame.font.SysFont("timesnewroman", 50)
    self.roboto = pygame.font.SysFont("roboto", 21)
    pygame.display.set_caption("Monte Carlo Pi Approximation")
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
  
  
  def frame(self):
    sq = pygame.Rect(self.horizontal_margin, self.vertical_margin, self.square_length, self.square_length)
    pygame.draw.rect(self.display, self.frame_color, sq)

  def inscribed_circle(self):
    pygame.draw.circle(self.display, self.circle_color, self.center, self.circle_radius)

  def dot(self):
    coord = self.random_coord()
    # Make the center of the circle the origin of the coordinate system
    dist_x = self.circle_radius - coord[0]
    dist_y = self.circle_radius - coord[1]

    if (dist_x)**2 + (dist_y)**2 < (self.circle_radius)**2:
      color = self.inside_color
      self.inside_count += 1
      self.total_sample_count += 1
    else:
      color = self.outside_color
      self.total_sample_count += 1
    pygame.draw.circle(self.dot_surface, color, coord, 2)

  def dart(self):
    for i in range(self.dart_rate):
      self.dot()

  def random_coord(self):
    x = random.uniform(0, self.square_length)
    y = random.uniform(0, self.square_length)
    return (x, y)
  
  def display_approx(self):
    pi = (self.inside_count/self.total_sample_count)*4
    num = self.roman.render(f"π = {pi:.23f}", True, self.font_color)
    self.display.blit(num, (self.horizontal_margin, self.square_length + self.vertical_margin))
  
  def display_ratio(self):
    container = pygame.Surface((self.square_length, 100))
    top_text = self.roboto.render(f"Dots inside the circle:", True, self.inside_color)
    bottom_text = self.roboto.render(f"Total count of dots:", True, self.outside_color)
    numerator = self.roboto.render(f"{self.inside_count:,}", True, self.inside_color)
    denominator = self.roboto.render(f"{self.total_sample_count:,}", True, self.outside_color)
    container.blit(top_text, (10, 10))
    container.blit(numerator, (self.square_length - 200, 10))
    container.blit(bottom_text, (10, 60))
    container.blit(denominator, (self.square_length - 200, 60))
    self.display.blit(container, (self.horizontal_margin, self.square_length + self.vertical_margin * 3))

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()
          
      self.display.fill(self.background_color)
      self.frame()
      self.inscribed_circle()
      self.dart()
      self.display.blit(self.dot_surface, (self.horizontal_margin, self.vertical_margin))
      self.display_approx()
      self.display_ratio()
    
      pygame.display.update()

simulator = MonteCarloPi()
simulator.run()