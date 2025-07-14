import pygame, random, argparse, sys

class Symbol:
    def __init__(self, x, y, glyph, font, glow_color, base_color):
        self.x = x
        self.y = y
        self.glyph = glyph
        self.font = font
        self.glow_color = glow_color
        self.base_color = base_color
        self.age = 0

    def update(self, speed):
        self.y += speed
        self.age += 1

    def draw(self, surface, is_head=False):
        color = self.glow_color if is_head else self.base_color
        alpha = 255 if is_head else max(255 - int(self.age * (255 / 40)), 0)
        rendered = self.font.render(self.glyph, True, color)
        rendered.set_alpha(alpha)
        surface.blit(rendered, (self.x, self.y))

class Column:
    def __init__(self, x, font, font_size, glyph_range, glow_color, base_color, screen_h, rain_speed, active=False):
        self.x = x
        self.font = font
        self.font_size = font_size
        self.glyph_range = glyph_range
        self.glow_color = glow_color
        self.base_color = base_color
        self.screen_h = screen_h
        self.rain_speed = rain_speed
        self.active = active
        self.glyph_height = self.font.size("𓀀")[1]
        self.symbols = []
        self.age = 0
        self.wait_time = random.randint(60, 240)
        self.reset_column()

    def reset_column(self):
        visible_rows = self.screen_h // self.glyph_height
        self.max_length = random.randint(int(visible_rows * 0.6), int(visible_rows * 1.2))
        self.y_offset = random.randint(-300, 0)
        self.symbols.clear()
        self.age = 0
        self.speed = (1.2 + (36 - self.font_size) * 0.1) * self.rain_speed

    def update(self):
        if self.active:
            if len(self.symbols) < self.max_length:
                y = self.symbols[-1].y + self.glyph_height if self.symbols else self.y_offset
                code = random.randint(self.glyph_range[0], self.glyph_range[1])
                glyph = chr(code)
                self.symbols.append(Symbol(self.x, y, glyph, self.font, self.glow_color, self.base_color))
            else:
                for s in self.symbols:
                    s.update(self.speed)
                self.symbols = [s for s in self.symbols if s.y < self.screen_h + self.glyph_height and s.age < 50]
                if not self.symbols:
                    self.active = False
        else:
            self.age += 1
            if self.age > self.wait_time:
                self.active = True
                self.reset_column()

    def draw(self, surface, debug=False):
        for i, s in enumerate(self.symbols):
            s.draw(surface, is_head=(i == len(self.symbols) - 1 and self.active))
        if debug and self.active:
            pygame.draw.line(surface, (50, 50, 50), (self.x, 0), (self.x, self.screen_h), 1)

def parse_unicode_range(rng):
    try:
        a, b = rng.split("-")
        return int(a, 16), int(b, 16)
    except:
        print(f"⚠️ Invalid glyph range: {rng}. Expected format: 13000-1342F")
        sys.exit()

def main():
    parser = argparse.ArgumentParser(
        description="Egyptian Hieroglyph Screensaver (rotation-free)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--color", choices=["green", "blue"], default="green")
    parser.add_argument("--font", default="NotoSansEgyptianHieroglyphs-Regular.ttf")
    parser.add_argument("--glyph_range", default="13000-1342F")
    parser.add_argument("--min_font", type=int, default=12)
    parser.add_argument("--max_font", type=int, default=36)
    parser.add_argument("--rows", type=int, default=6)
    parser.add_argument("--rain_speed", type=float, default=1.0)
    parser.add_argument("--watermark", default=None)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    pygame.init()
    info = pygame.display.Info()
    W, H = info.current_w, info.current_h
    screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
    pygame.display.set_caption("Hieroglyph Matrix Screensaver")

    glyph_range = parse_unicode_range(args.glyph_range)

    base_color = pygame.Color(0, 255, 70) if args.color == "green" else pygame.Color(0, 120, 255)
    glow_color = pygame.Color(180, 255, 180) if args.color == "green" else pygame.Color(80, 200, 255)

    grid = []
    for r in range(args.rows):
        size = args.max_font - int((r / max(args.rows - 1, 1)) * (args.max_font - args.min_font))
        font = pygame.font.Font(args.font, size)
        spacing = size + random.randint(8, 16)
        offset = random.randint(0, spacing)
        cols = W // spacing
        row = []
        for c in range(cols):
            x = c * spacing + offset
            active = random.random() < 0.3
            row.append(Column(x, font, size, glyph_range, glow_color, base_color, H, args.rain_speed, active))
        grid.append(row)

    wm = None
    wx = wy = dx = dy = 0
    if args.watermark:
        try:
            wm = pygame.image.load(args.watermark).convert_alpha()
            scale = (H // 3) / wm.get_height()
            wm = pygame.transform.smoothscale(wm, (int(wm.get_width() * scale), int(wm.get_height() * scale)))
            wm.set_alpha(100)
            wx = (W - wm.get_width()) // 2
            wy = (H - wm.get_height()) // 2
            dx = dy = 1
        except Exception as e:
            print(f"⚠️ Failed to load watermark: {args.watermark}")

    clock = pygame.time.Clock()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                running = False

        screen.fill((0, 0, 0))
        temp = pygame.Surface((W, H), pygame.SRCALPHA)
        temp.fill((0, 0, 0))

        if wm:
            wx += dx
            wy += dy
            if wx <= 0 or wx + wm.get_width() >= W: dx = -dx
            if wy <= 0 or wy + wm.get_height() >= H: dy = -dy
            temp.blit(wm, (wx, wy))

        fade_surface = pygame.Surface((W, H), pygame.SRCALPHA)
        fade_surface.fill((0, 0, 0, 40))
        temp.blit(fade_surface, (0, 0))

        for row in grid:
            for col in row:
                col.update()
                col.draw(temp, debug=args.debug)

        screen.blit(temp, (0, 0))
        pygame.display.flip()
        clock.tick(args.fps)

    pygame.quit()

if __name__ == "__main__":
    main()
    