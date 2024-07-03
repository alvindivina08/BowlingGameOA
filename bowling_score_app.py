import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 600
FRAME_WIDTH = 100
FRAME_HEIGHT = 100
FRAME_MARGIN = 30
FONT_SIZE = 24

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)


class BowlingGame:
    def __init__(self):
        self.full_screen = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bowling Score Calculator")
        self.clock = pygame.time.Clock()

        self.frames = []
        self.frame_scores = []
        self.current_frame = 0
        self.current_shot = 1  # 1 for first shot, 2 for second shot
        self.font = pygame.font.Font(None, FONT_SIZE)

        # Initialize frames
        self.init_frames()

        # Initialize reset button rect
        self.reset_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 50,
            SCREEN_HEIGHT - 50,
            100,
            40
        )

    def init_frames(self):
        for i in range(10):
            print(i)
            frame_rect = pygame.Rect(
                FRAME_MARGIN + i * (FRAME_WIDTH + FRAME_MARGIN),
                FRAME_MARGIN,
                FRAME_WIDTH,
                FRAME_HEIGHT
            )
            self.frames.append(frame_rect)
            self.frame_scores.append(["", ""])
            # to be fixed later
            if i == 8:
                self.frame_scores.append(["", "", ""])  # List to store two scores per frame
            print(self.frame_scores, i)

    def draw(self):
        self.screen.fill(WHITE)

        # Draw frames
        for i, frame in enumerate(self.frames):
            pygame.draw.rect(self.screen, GRAY, frame)
            text_surface = self.font.render(f"Frame {i + 1}", True, BLACK)
            self.screen.blit(text_surface, (frame.x + 5, frame.y + 5))

            score_text = ""
            for j, score in enumerate(self.frame_scores[i]):
                score_text += f"{score}"
                if j < len(self.frame_scores[i]) - 1:
                    score_text += " | "

                score_surface = self.font.render(score_text, True, BLACK)
                self.screen.blit(score_surface, (frame.x + 10, frame.y + FRAME_HEIGHT // 2))

            # Draw score label
            score_label = self.font.render(f"Score: {self.calculate_frame_score(i)}", True, BLACK)
            self.screen.blit(score_label, (frame.x + 5, frame.y + FRAME_HEIGHT - 30))

        # Draw reset button
        pygame.draw.rect(self.screen, RED, self.reset_rect)
        reset_text = self.font.render("RESET", True, WHITE)
        self.screen.blit(reset_text, (self.reset_rect.x + 20, self.reset_rect.y + 10))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if reset button clicked
                if self.reset_rect.collidepoint(mouse_pos):
                    self.reset_scores()
            elif event.type == pygame.KEYDOWN:
                # Handle key presses for entering scores
                if event.unicode.isdigit():
                    self.enter_score(event.unicode)
                elif event.unicode.lower() == 'x' and self.current_shot in [1, 2, 3]:
                    self.enter_score('X')
                elif event.unicode.lower() == '/' and self.current_shot == 2:
                    self.enter_score('/')

                # Toggle full-screen mode on 'F' key press
                elif event.key == pygame.K_f:
                    self.toggle_full_screen()

    def toggle_full_screen(self):
        self.full_screen = not self.full_screen
        if self.full_screen:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bowling Score Calculator")

    def enter_score(self, score):
        # Add the score to the current frame's appropriate shot
        if self.current_frame < 9:
            if score == 'X' and self.current_shot == 1:
                self.frame_scores[self.current_frame][0] = 'X'
                self.current_frame += 1
                self.current_shot = 1
            elif score == '/' and self.current_shot == 2:
                self.frame_scores[self.current_frame][1] = '/'
                self.current_frame += 1
                self.current_shot = 1
            elif score.isdigit():
                if self.current_shot == 1:
                    self.frame_scores[self.current_frame][0] = score
                    self.current_shot = 2
                elif self.current_shot == 2:
                    self.frame_scores[self.current_frame][1] = score
                    self.current_frame += 1
                    self.current_shot = 1

        else:
        # Special handling for the 10th frame
            self.handle_tenth_frame(score)

    def handle_tenth_frame(self, score):
        if score == 'X':
            self.frame_scores[self.current_frame][self.current_shot - 1] = 'X'
            self.current_shot += 1
        elif score == '/':
            self.frame_scores[self.current_frame][self.current_shot - 1] = '/'
            self.current_shot += 1
        elif score.isdigit():
            self.frame_scores[self.current_frame][self.current_shot - 1] = score
            if self.current_shot == 1:
                self.current_shot = 2
            elif self.current_shot == 2:
                if int(self.frame_scores[self.current_frame][0]) + int(score) >= 10:
                    self.current_shot = 3
                else:
                    self.current_shot = 1
                    self.current_frame += 1
            elif self.current_shot == 3:
                self.current_shot = 1
                self.current_frame += 1
    

    def calculate_frame_score(self, frame_index):
        # Calculate score for a given frame
        previous_frame_score = 0
        if frame_index < 10:
            first_score = self.frame_scores[frame_index][0]
            second_score = self.frame_scores[frame_index][1]

           # Convert empty scores to '0'
            if first_score == '':
                first_score = '0'
            if second_score == '':
                second_score = '0'

            # Previous frame score
            if frame_index > 0:
                previous_frame_score = self.calculate_frame_score(frame_index - 1)

            if first_score == 'X':
                # Strike
                current_score = 10
                next_first, next_second = self.get_next_two_scores(frame_index)

                return previous_frame_score + current_score + next_first + next_second
            
            elif second_score == '/':
                # Spare
                if frame_index + 1 <= 10:  # Ensure next frame exists
                    if frame_index < 9:
                        next_score = self.frame_scores[frame_index + 1][0]
                    else:
                        print(frame_index)
                        next_score = self.frame_scores[frame_index][2]

                    if next_score == '':
                        next_score = 0
                    elif next_score == 'X':
                        next_score = '10'
                    elif next_score == '/':
                        next_score = '10'
                    
                    return previous_frame_score + 10 + int(next_score)
            else:
                # Regular scores
                return previous_frame_score + int(first_score) + int(second_score)
            
            return previous_frame_score

        else:
            return 0 
        
    def get_next_two_scores(self, frame_index):
        # Get the next two scores after a strike
        next_first = 0
        next_second = 0
        next_third = 0
        # next_spare = 0

        if frame_index + 1 <= 10:  # Ensure next frame exists
            if frame_index < 9:
                next_first = self.frame_scores[frame_index + 1][0]
            else:
                next_first = self.frame_scores[frame_index][0]

            if next_first == 'X':
                next_first = "10"

            # frames = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            # frame 9 needs 3 inputs if the first score is strike
            # or if the second score is a spare

            # frame index 8 is fine
            # frame index 9 is where it crashes if the score is X
            if frame_index + 1 <= 10:  # Check for second next frame if within bounds
                # frame index 9 does not continue after this line
                if next_first != '10':
                    next_second = self.frame_scores[frame_index + 1][1]
                    if next_second == "/":
                        next_first = "0"
                        next_second = "10"
                elif frame_index < 8:
                    next_second = self.frame_scores[frame_index + 2][0]
                    if next_second == 'X':
                        next_second = "10"
                # handle frame 9
                elif frame_index == 8:
                    next_first = self.frame_scores[frame_index + 1][0]
                    if next_first == 'X':
                        next_first = "10"
                    next_second = self.frame_scores[frame_index + 1][1]
                    if next_second == 'X':
                        next_second = "10"
                # handle frame 10
                elif frame_index == 9:
                    next_first = self.frame_scores[frame_index][0]
                    if next_first == 'X':
                        next_first = "10"
                    next_second = self.frame_scores[frame_index][1]
                    if next_second in ['X', '/']:
                        next_second = "10"
                    next_third = self.frame_scores[frame_index][2]
                    if next_third == 'X':
                        next_third = "10"
                    
        next_first = int(next_first) if next_first.isdigit() else 0
        next_second = int(next_second) if next_second.isdigit() else 0

        return next_first, next_second

    def reset_scores(self):
        # Reset all scores and current frame index
        self.frame_scores = [["", ""] for _ in range(9)] + [["", "", ""]]
        self.current_frame = 0
        self.current_shot = 1

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(30)


if __name__ == "__main__":
    game = BowlingGame()
    game.run()
