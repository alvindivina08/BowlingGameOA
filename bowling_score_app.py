import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 600
FRAME_WIDTH = 100
FRAME_HEIGHT = 100
FRAME_MARGIN = 50
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
            frame_rect = pygame.Rect(
                FRAME_MARGIN + i * (FRAME_WIDTH + FRAME_MARGIN),
                FRAME_MARGIN,
                FRAME_WIDTH,
                FRAME_HEIGHT
            )
            self.frames.append(frame_rect)
            self.frame_scores.append(["", ""])  # List to store two scores per frame

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
                elif event.unicode.lower() == 'x' and self.current_shot == 1:
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
        if self.current_frame < 10:
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

    def calculate_frame_score(self, frame_index):
        # Calculate score for a given frame
        if frame_index < 10:
            first_score = self.frame_scores[frame_index][0]
            second_score = self.frame_scores[frame_index][1]

           # Convert empty scores to '0'
            if first_score == '':
                first_score = '0'
            if second_score == '':
                second_score = '0'

            # Previous frame score
            previous_frame_score = 0
            if frame_index > 0:
                previous_frame_score = self.calculate_frame_score(frame_index - 1)

            if first_score == 'X':
                # Strike
                current_score = 10
                next_first = 0
                next_second = 0

                if frame_index + 1 < 10:  # Ensure next frame exists
                    next_first = self.frame_scores[frame_index + 1][0]

                    if next_first == 'X':
                        next_first = "10"

                    if frame_index + 1 < 9:  # Check for second next frame if within bounds
                        if next_first != '10':
                            next_second = self.frame_scores[frame_index + 1][1]
                        else:
                            next_second = self.frame_scores[frame_index + 2][0]
                            print(next_second)
                            if next_second == 'X':
                                next_second = "10"


                # Convert next scores to integers if they are digits
                next_first = int(next_first) if next_first.isdigit() else 0
                next_second = int(next_second) if next_second.isdigit() else 0


                return previous_frame_score + current_score + next_first + next_second
            elif second_score == '/':
                # Spare
                if frame_index + 1 < 10:  # Ensure next frame exists
                    next_score = self.frame_scores[frame_index + 1][0]
                    if next_score == '':
                        next_score = 0
                    elif next_score == 'X':
                        next_score = '10'
                    
                    print(next_score)
                    return previous_frame_score + 10 + int(next_score)
            else:
                # Regular scores
                return previous_frame_score + int(first_score) + int(second_score)
        
        else:
            return 0 
            
        # elif frame_index == 10:
        #     # Tenth frame calculation
        #     first_score = self.frame_scores[frame_index][0]
        #     second_score = self.frame_scores[frame_index][1]
        #     third_score = self.frame_scores[frame_index][2] if len(self.frame_scores[frame_index]) > 2 else ''
        #     total = 0
        #     if first_score == 'X':
        #         total += 10
        #         if second_score == 'X':
        #             total += 10
        #             if third_score == 'X':
        #                 total += 10
        #             elif third_score.isdigit():
        #                 total += int(third_score)
        #         elif second_score == '/':
        #             total += 10
        #             if third_score == 'X':
        #                 total += 10
        #             elif third_score.isdigit():
        #                 total += int(third_score)
        #         elif second_score.isdigit():
        #             total += int(second_score)
        #             if third_score == '/':
        #                 total += 10
        #             elif third_score.isdigit():
        #                 total += int(third_score)
        #     elif second_score == '/':
        #         total += 10
        #         if third_score == 'X':
        #             total += 10
        #         elif third_score.isdigit():
        #             total += int(third_score)
        #     elif first_score.isdigit():
        #         total += int(first_score)
        #         if second_score == '/':
        #             total += 10
        #         elif second_score.isdigit():
        #             total += int(second_score)
        #     return total

    def reset_scores(self):
        # Reset all scores and current frame index
        self.frame_scores = [["", ""] for _ in range(10)]
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
