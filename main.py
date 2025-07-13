import pygame, random, argparse

class Symbol:
    def __init__(self, x, y, glyph, font, glow_color, base_color):
        self.x, self.y = y, y
        self.glyph = glyph
        self.font = font
        self.glow_color = glow_color
        self.base_color = base_color
        self.age = 0

    def update(self, speed):
        self.y += speed
        self.age += 1

    def draw(self, surf, is_head=False):
        color = self.glow_color if is_head else self.base_color
        alpha = 255 if is_head else max(255 - int(self.age * (255 / 40)), 0)
        text_surf = self.font.render(self.glyph, True, color)
        text_surf.set_alpha(alpha)
        surf.blit(text_surf, (self.x, self.y))

class Column:
    def __init__(self, x, y_offset, font_size, font, glow_color, base_color, screen_h):
        self.x = x
        self.y_offset = y_offset
        self.font_size = font_size
        self.font = font
        self.glow_color = glow_color
        self.base_color = base_color
        self.screen_h = screen_h

        self.symbols = []
        self.max_length = random.randint(10, 30)
        self.active = random.random() < 0.5  # 50% activation at start
        self.age = 0
        self.speed = 1.5 + (36 - font_size) * 0.15  # closer rows fall faster

    def update(self):
        if self.active:
            if len(self.symbols) < self.max_length:
                y = self.symbols[-1].y + self.font_size if self.symbols else self.y_offset
                glyph = chr(random.randint(0x13000, 0x1342F))
                self.symbols.append(Symbol(self.x, y, glyph, self.font, self.glow_color, self.base_color))
            else:
                for s in self.symbols:
                    s.update(self.speed)

                self.symbols = [s for s in self.symbols if s.y < self.screen_h + self.font_size and s.age < 50]

                if not self.symbols:
                    self.active = False
                    self.age = 0
        else:
            self.age += 1
            if self.age > random.randint(60, 180):  # Wait a bit before random reactivation
                self.max_length = random.randint(10, 30)
                self.y_offset = random.randint(-300, 0)
                self.symbols.clear()
                self.active = True

    def draw(self, surf):
        for i, s in enumerate(self.symbols):
            is_head = (i == len(self.symbols) - 1 and self.active)
            s.draw(surf, is_head)

def main():
    parser = argparse.ArgumentParser(description="Dynamic 3D Hieroglyph Matrix Screensaver")
    parser.add_argument("--color", choices=["green", "blue"], default="green")
    parser.add_argument("--font", default="NotoSansEgyptianHieroglyphs-Regular.ttf")
    parser.add_argument("--min_font", type=int, default=12)
    parser.add_argument("--max_font", type=int, default=36)
    parser.add_argument("--rows", type=int, default=6)
    parser.add_argument("--watermark", default=None)
    parser.add_argument("--fps", type=int, default=30)
    args = parser.parse_args()

    # Color themes
    if args.color == "green":
        base_color = pygame.Color(0, 255, 70)
        glow_color = pygame.Color(180, 255, 180)
    else:
        base_color = pygame.Color(0, 120, 255)
        glow_color = pygame.Color(80, 200, 255)

    pygame.init()
    info = pygame.display.Info()
    W, H = info.current_w, info.current_h
    screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
    pygame.display.set_caption("Dynamic Hieroglyph Matrix")

    # Create grid of columns
    row_fonts = []
    grid = []
    depth_range = args.max_font - args.min_font
    for r in range(args.rows):
        size = args.max_font - int((r / (args.rows - 1)) * depth_range)
        font = pygame.font.Font(args.font, size)
        row_fonts.append(font)
        spacing = size + 6  # extra spacing to reduce crowding
        cols = W // spacing
        row = []
        for c in range(cols):
            x = c * spacing
            y_offset = random.randint(-300, 0)
            col = Column(x, y_offset, size, font, glow_color, base_color, H)
            row.append(col)
        grid.append(row)

    # Watermark setup
    wm = None
    wx = wy = dx = dy = 0
    if args.watermark:
        wm = pygame.image.load(args.watermark).convert_alpha()
        scale = (H // 3) / wm.get_height()
        wm = pygame.transform.smoothscale(wm, (int(wm.get_width() * scale), int(wm.get_height() * scale)))
        wm.set_alpha(100)
        wx = (W - wm.get_width()) // 2
        wy = (H - wm.get_height()) // 2
        dx = 1
        dy = 1

    clock = pygame.time.Clock()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                running = False

        screen.fill((0, 0, 0))

        # watermark float
        if wm is not None:
            wx += dx
            wy += dy
            if wx <= 0 or wx + wm.get_width() >= W:
                dx = -dx
            if wy <= 0 or wy + wm.get_height() >= H:
                dy = -dy
            screen.blit(wm, (wx, wy))

        # fade overlay
        fade_surface = pygame.Surface((W, H), pygame.SRCALPHA)
        fade_surface.fill((0, 0, 0, 40))
        screen.blit(fade_surface, (0, 0))

        # update and draw each column
        for row in grid:
            for col in row:
                col.update()
                col.draw(screen)

        pygame.display.flip()
        clock.tick(args.fps)

    pygame.quit()

if __name__ == "__main__":
    main()