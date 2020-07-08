import random
import pygame, math

pygame.init()
screen = pygame.display.set_mode([1200, 900])
caption = pygame.display.set_caption("Tre i rad mot dator")

# colors
black = (0, 0, 0)
white = (255, 255, 255)
dark_white = (122, 122, 122)
green = (38, 142, 0)
light_green = (82, 216, 34)
red = (175, 8, 8)
light_red = (216, 0, 0)
blue = (0, 70, 255)
light_blue = (51, 153, 255)
orange = (255, 128, 0)
light_orange = (255, 153, 51)

# variables
run = True
points_player = 0
points_computer = 0
ties = 0
box_font = pygame.font.SysFont(None, 200)
game = None
turn = "player"
round_num = 0
shown_color = green
p_points_controller = "yes"
c_points_controller = "yes"
ties_controller = "yes"
win_player = None
btn_color = orange
quit_btn_color = red
settings_image = pygame.image.load(r"C:\Users\Henrik\PycharmProjects\PYTHON\settingswheel.png")
bright_settings_image = pygame.image.load(r"C:\Users\Henrik\PycharmProjects\PYTHON\settingswheel_bright.png")
click = "no"
resume_color = white

# classes

# defining buttons
class button:
    def __init__(self, x, y, width, height, text, text_color, color, color_hover, text_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        self.color = color
        self.color_hover = color_hover
        self.text_size = text_size

        # drawing the button
        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, shown_color, (self.x, self.y, self.width, self.height), 0)
        font = pygame.font.SysFont(None, self.text_size)
        text = font.render(self.text, True, self.text_color)
        screen.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def reset_game(self):
        global mouse_pos
        global mouse_click
        global shown_color
        global points_computer
        global points_player
        global round_num
        global ties
        global turn
        global p_points_controller
        global c_points_controller
        global ties_controller
        global win_player
        # interacting with the button
        if self.x + self.width > mouse_pos[0] > self.x and self.y + self.height > mouse_pos[1] > self.y:
            shown_color = light_green
            if mouse_click:
                points_computer = 0
                points_player = 0
                round_num = 0
                ties = 0
                turn = "player"
                p_points_controller = "yes"
                c_points_controller = "yes"
                ties_controller = "yes"
                win_player = None
                for x in boxes:
                    x.text = "X"
                    x.text_color = black

        else:
            shown_color = green


# defining the squared invisible buttons for the board
class box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.text = "X"
        self.width = 190
        self.height = 190
        self.text_color = black

    def mechanism(self):
        global turn
        global round_num
        mouse_pos = pygame.mouse.get_pos()
        if turn == "player":
            if (self.x + self.width) > mouse_pos[0] > self.x and (self.y + self.height) > mouse_pos[1] > self.y:
                # hovering mechanism
                if self.text_color == black:
                    self.text = "O"
                    self.text_color = light_blue

                # clicking mechanism
                if mouse_click and self.text_color == light_blue:
                    self.text_color = blue
                    self.text = "O"
                    turn = "computer"
                    round_num += 1

            # resetting color after hovering
            elif self.text_color != blue and self.text_color != red:
                self.text_color = black
                self.text = "X"

    def is_blank(self):
        if self.text_color == black:
            return True
        else:
            return False

    def draw(self):
        pygame.draw.rect(screen, black, (self.x, self.y, self.width, self.height), )
        screen.blit(box_font.render(self.text, True, self.text_color), \
 \
                    ((self.x + (self.width / 2) - \
                      box_font.render(self.text, True,
                                      self.text_color).get_rect().width / 2),
                     (self.y + (self.height / 2)) - \
                     box_font.render(self.text, True, self.text_color).get_rect().height / 2))


def board_is_full():
    result = True
    for thing in boxes:
        if thing.is_blank():
            result = False
    return result


def check_for_win():
    global win_player
    global points_computer
    global points_player
    # checking columns
    for column in range(3):
        if board[column][0].text == board[column][1].text == board[column][2].text:
            if board[column][0].text_color == board[column][1].text_color == board[column][2].text_color:
                if board[column][0].text_color == blue:
                    win_player = "player"
                    pygame.draw.line(screen, blue, [board[column][0].x, board[column][0].y + 95],
                                     [board[column][2].x + 190, board[column][2].y + 95], 5)
                    return True
                if board[column][0].text_color == red:
                    win_player = "computer"
                    pygame.draw.line(screen, red, [board[column][0].x, board[column][0].y + 95],
                                     [board[column][2].x + 190, board[column][2].y + 95], 5)
                    return True
    # checking rows
    for row in range(3):
        if board[0][row].text == board[1][row].text == board[2][row].text:
            if board[0][row].text_color == board[1][row].text_color == board[2][row].text_color:
                if board[0][row].text_color == blue:
                    win_player = "player"
                    pygame.draw.line(screen, blue, [board[0][row].x + 95, board[0][row].y], [board[0][row].x + 95, 800],
                                     5)
                    return True
                if board[0][row].text_color == red:
                    win_player = "computer"
                    pygame.draw.line(screen, red, [board[0][row].x + 95, board[0][row].y], [board[0][row].x + 95, 800],
                                     5)
                    return True
    # checking diagonals
    if board[0][0].text == board[1][1].text == board[2][2].text:
        if board[0][0].text_color == board[1][1].text_color == board[2][2].text_color:
            if board[0][0].text_color == blue:
                win_player = "player"
                pygame.draw.line(screen, blue, [300, 200], [900, 800], 5)
                return True
            if board[0][0].text_color == red:
                win_player = "computer"
                pygame.draw.line(screen, red, [300, 200], [900, 800], 5)
                return True
    if board[2][0].text == board[1][1].text == board[0][2].text:
        if board[2][0].text_color == board[1][1].text_color == board[0][2].text_color:
            if board[2][0].text_color == blue:
                win_player = "player"
                pygame.draw.line(screen, blue, [300, 800], [900, 200], 5)
                return True
            if board[2][0].text_color == red:
                win_player = "computer"
                pygame.draw.line(screen, red, [300, 800], [900, 200], 5)
                return True


def next_round_button():
    width = 400
    height = 90
    x = 600 - width / 2
    y = 105
    global btn_color
    global turn
    global round_num
    global p_points_controller
    global c_points_controller
    global ties_controller
    global win_player
    pygame.draw.rect(screen, btn_color, (x, y, width, height), 0)
    font = pygame.font.SysFont(None, 90)
    text = font.render("Next round", True, white)
    screen.blit(text, (x + (width / 2 - text.get_width() / 2), y + (height / 2 - text.get_height() / 2)))

    if x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y:
        btn_color = light_orange
        if mouse_click:
            for x in boxes:
                x.text = "X"
                x.text_color = black
            turn = "player"
            round_num = 0
            p_points_controller = "yes"
            c_points_controller = "yes"
            ties_controller = "yes"
            win_player = None
            if (ties + points_player + points_computer) % 2 != 0:
                turn = "computer"
            else:
                turn = "player"
    else:
        btn_color = orange


# button to quit the whole game
def quit_button():
    x_quit = 0
    y_quit = 0
    width_quit = 160
    height_quit = 50
    global quit_btn_color
    global mouse_pos
    global mouse_click
    global run
    pygame.draw.rect(screen, quit_btn_color, (x_quit, y_quit, width_quit, height_quit), 0)
    font_quit = pygame.font.SysFont(None, 40)
    text_quit = font_quit.render("Quit game", True, white)
    screen.blit(text_quit, (
    x_quit + (width_quit / 2 - text_quit.get_width() / 2), y_quit + (height_quit / 2 - text_quit.get_height() / 2)))
    # making the button interacting
    if 0 < mouse_pos[0] < width_quit and 0 < mouse_pos[1] < height_quit:
        quit_btn_color = light_red
        if mouse_click:
            run = False
    else:
        quit_btn_color = red


box1 = box(300, 200)
box2 = box(500, 200)
box3 = box(700, 200)
box4 = box(300, 400)
box5 = box(500, 400)
box6 = box(700, 400)
box7 = box(300, 600)
box8 = box(500, 600)
box9 = box(700, 600)
board = [
    [box1, box2, box3],
    [box4, box5, box6],
    [box7, box8, box9]
]
boxes = [box1, box2, box3, box4, box5, box6, box7, box8, box9]
corners = [box1, box3, box7, box9]



# AI start


def random_AI():
    global turn
    global round_num
    if turn == "computer" and not check_for_win():
        if not board_is_full():
            for item in boxes:
                if item.is_blank():
                    empty_boxes.append(item)
            random.choice(empty_boxes).text_color = red
            turn = "player"
            round_num += 1


def impossible_AI():
    global turn
    global round_num
    global red
    global blue
    if turn == "computer" and not check_for_win():
        if not board_is_full():

            if round_num == 0:
                random.choice(corners).text_color = red
                turn = "player"
                round_num += 1

            # red row 1
            elif box1.text_color == red and box2.text_color == red and box3.is_blank():
                box3.text_color = red
                turn = "player"
                round_num += 1
            elif box1.text_color == red and box3.text_color == red and box2.is_blank():
                box2.text_color = red
                turn = "player"
                round_num += 1
            elif box3.text_color == red and box2.text_color == red and box1.is_blank():
                box1.text_color = red
                turn = "player"
                round_num += 1

            # red row 2
            elif box4.text_color == red and box5.text_color == red and box6.is_blank():
                box6.text_color = red
                turn = "player"
                round_num += 1
            elif box5.text_color == red and box6.text_color == red and box4.is_blank():
                box4.text_color = red
                turn = "player"
                round_num += 1
            elif box4.text_color == red and box6.text_color == red and box5.is_blank():
                box5.text_color = red
                turn = "player"
                round_num += 1

            # red row 3
            elif box7.text_color == red and box8.text_color == red and box9.is_blank():
                box9.text_color = red
                turn = "player"
                round_num += 1
            elif box7.text_color == red and box9.text_color == red and box8.is_blank():
                box8.text_color = red
                turn = "player"
                round_num += 1
            elif box8.text_color == red and box9.text_color == red and box7.is_blank():
                box7.text_color = red
                turn = "player"
                round_num += 1

            # red column 1
            elif box1.text_color == red and box4.text_color == red and box7.is_blank():
                box7.text_color = red
                turn = "player"
                round_num += 1
            elif box1.text_color == red and box7.text_color == red and box4.is_blank():
                box4.text_color = red
                turn = "player"
                round_num += 1
            elif box4.text_color == red and box7.text_color == red and box1.is_blank():
                box1.text_color = red
                turn = "player"
                round_num += 1

            # red column 2
            elif box2.text_color == red and box5.text_color == red and box8.is_blank():
                box8.text_color = red
                turn = "player"
                round_num += 1
            elif box2.text_color == red and box8.text_color == red and box5.is_blank():
                box5.text_color = red
                turn = "player"
                round_num += 1
            elif box5.text_color == red and box8.text_color == red and box2.is_blank():
                box2.text_color = red
                turn = "player"
                round_num += 1

            # red column 3
            elif box3.text_color == red and box6.text_color == red and box9.is_blank():
                box9.text_color = red
                turn = "player"
                round_num += 1
            elif box3.text_color == red and box9.text_color == red and box6.is_blank():
                box6.text_color = red
                turn = "player"
                round_num += 1
            elif box6.text_color == red and box9.text_color == red and box3.is_blank():
                box3.text_color = red
                turn = "player"
                round_num += 1

            # red diagonal 1
            elif box1.text_color == red and box5.text_color == red and box9.is_blank():
                box9.text_color = red
                turn = "player"
                round_num += 1
            elif box1.text_color == red and box9.text_color == red and box5.is_blank():
                box5.text_color = red
                turn = "player"
                round_num += 1
            elif box5.text_color == red and box9.text_color == red and box1.is_blank():
                box1.text_color = red
                turn = "player"
                round_num += 1

            # red diagonal 2
            elif box3.text_color == red and box5.text_color == red and box7.is_blank():
                box7.text_color = red
                turn = "player"
                round_num += 1
            elif box3.text_color == red and box7.text_color == red and box5.is_blank():
                box5.text_color = red
                turn = "player"
                round_num += 1
            elif box5.text_color == red and box7.text_color == red and box3.is_blank():
                box3.text_color = red
                turn = "player"
                round_num += 1

            # blue row 1
            elif box1.text_color == blue and box2.text_color == blue and box3.is_blank():
                box3.text_color = red
                turn = "player"
                round_num += 1
            elif box1.text_color == blue and box3.text_color == blue and box2.is_blank():
                box2.text_color = red
                turn = "player"
                round_num += 1
            elif box3.text_color == blue and box2.text_color == blue and box1.is_blank():
                box1.text_color = red
                turn = "player"
                round_num += 1

            # blue row 2
            elif box4.text_color == blue and box5.text_color == blue and box6.is_blank():
                box6.text_color = red
                turn = "player"
                round_num += 1
            elif box5.text_color == blue and box6.text_color == blue and box4.is_blank():
                box4.text_color = red
                turn = "player"
                round_num += 1
            elif box4.text_color == blue and box6.text_color == blue and box5.is_blank():
                box5.text_color = red
                turn = "player"
                round_num += 1

            # blue row 3
            elif box7.text_color == blue and box8.text_color == blue and box9.is_blank():
                box9.text_color = red
                turn = "player"
                round_num += 1
            elif box7.text_color == blue and box9.text_color == blue and box8.is_blank():
                box8.text_color = red
                turn = "player"
                round_num += 1
            elif box8.text_color == blue and box9.text_color == blue and box7.is_blank():
                box7.text_color = red
                turn = "player"
                round_num += 1

            # blue column 1
            elif box1.text_color == blue and box4.text_color == blue and box7.is_blank():
                box7.text_color = red
                turn = "player"
                round_num += 1
            elif box1.text_color == blue and box7.text_color == blue and box4.is_blank():
                box4.text_color = red
                turn = "player"
                round_num += 1
            elif box4.text_color == blue and box7.text_color == blue and box1.is_blank():
                box1.text_color = red
                turn = "player"
                round_num += 1

            # blue column 2
            elif box2.text_color == blue and box5.text_color == blue and box8.is_blank():
                box8.text_color = red
                turn = "player"
                round_num += 1
            elif box2.text_color == blue and box8.text_color == blue and box5.is_blank():
                box5.text_color = red
                turn = "player"
                round_num += 1
            elif box5.text_color == blue and box8.text_color == blue and box2.is_blank():
                box2.text_color = red
                turn = "player"
                round_num += 1

            # blue column 3
            elif box3.text_color == blue and box6.text_color == blue and box9.is_blank():
                box9.text_color = red
                turn = "player"
                round_num += 1
            elif box3.text_color == blue and box9.text_color == blue and box6.is_blank():
                box6.text_color = red
                turn = "player"
                round_num += 1
            elif box6.text_color == blue and box9.text_color == blue and box3.is_blank():
                box3.text_color = red
                turn = "player"
                round_num += 1

            # blue diagonal 1
            elif box1.text_color == blue and box5.text_color == blue and box9.is_blank():
                box9.text_color = red
                turn = "player"
                round_num += 1
            elif box1.text_color == blue and box9.text_color == blue and box5.is_blank():
                box5.text_color = red
                turn = "player"
                round_num += 1
            elif box5.text_color == blue and box9.text_color == blue and box1.is_blank():
                box1.text_color = red
                turn = "player"
                round_num += 1

            # blue diagonal 2
            elif box3.text_color == blue and box5.text_color == blue and box7.is_blank():
                box7.text_color = red
                turn = "player"
                round_num += 1
            elif box3.text_color == blue and box7.text_color == blue and box5.is_blank():
                box5.text_color = red
                turn = "player"
                round_num += 1
            elif box5.text_color == blue and box7.text_color == blue and box3.is_blank():
                box3.text_color = red
                turn = "player"
                round_num += 1

            elif round_num == 2 and box5.is_blank():
                for item in corners:
                    if item.is_blank():
                        empty_boxes.append(item)
                random.choice(empty_boxes).text_color = red
                turn = "player"
                round_num += 1

            elif box5.is_blank():
                box5.text_color = red
                turn = "player"
                round_num += 1

            else:
                for item in boxes:
                    if item.is_blank():
                        empty_boxes.append(item)
                random.choice(empty_boxes).text_color = red
                turn = "player"
                round_num += 1

    # AI end

def settings_btn():
    global x_cursor
    global y_cursor
    global sqx
    global sqy
    global click
    global resume_color
    width_resume = 325
    height_resume = 40
    x_resume = 600 - (width_resume / 2)
    y_resume = 100


    screen.blit(settings_image, (1100, 90))
    x_cursor = mouse_pos[0]
    y_cursor = mouse_pos[1]
    sqx = (x_cursor - 1150) ** 2
    sqy = (y_cursor - 140) ** 2
    if math.sqrt(sqx + sqy) < 50:
        screen.blit(bright_settings_image, (1100, 90))
        if mouse_click:
            click = "yes"
    if click == "yes":
        screen.fill(black)
        pygame.draw.rect(screen, black, (x_resume, y_resume, width_resume, height_resume), 0)
        font_resume = pygame.font.SysFont(None, 70)
        text_resume = font_resume.render("Resume game", True, resume_color)
        screen.blit(text_resume, (
            x_resume + (width_resume / 2 - text_resume.get_width() / 2),
            y_resume + (height_resume / 2 - text_resume.get_height() / 2)))
        if x_resume + width_resume > x_cursor > x_resume and y_resume < y_cursor < y_resume + height_resume:
            resume_color = dark_white
            if mouse_click:
                click = "no"
        else:
            resume_color = white
# main-loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # checking if player has won
    check_for_win()
    if check_for_win():
        if win_player == "player":
            if p_points_controller == "yes":
                points_player += 1
                p_points_controller = "no"
        if win_player == "computer":
            if c_points_controller == "yes":
                points_computer += 1
                c_points_controller = "no"

    if round_num == 9 and not check_for_win():
        if ties_controller == "yes":
            ties += 1
            ties_controller = "no"
    # end for checking if player has won

    empty_boxes = []

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]

    # Draw start
    screen.fill(black)

    board = [
        [box1, box2, box3],
        [box4, box5, box6],
        [box7, box8, box9]
    ]

    boxes = [box1, box2, box3, box4, box5, box6, box7, box8, box9]

    if click == "no":
        if not check_for_win():
            box1.mechanism()
            box2.mechanism()
            box3.mechanism()
            box4.mechanism()
            box5.mechanism()
            box6.mechanism()
            box7.mechanism()
            box8.mechanism()
            box9.mechanism()

    box1.draw()
    box2.draw()
    box3.draw()
    box4.draw()
    box5.draw()
    box6.draw()
    box7.draw()
    box8.draw()
    box9.draw()

    pygame.draw.line(screen, white, [300, 400], [900, 400], 10)
    pygame.draw.line(screen, white, [300, 600], [900, 600], 10)
    pygame.draw.line(screen, white, [500, 200], [500, 800], 10)
    pygame.draw.line(screen, white, [700, 200], [700, 800], 10)

    play_again_btn = button(1040, 0, 160, 50, "Reset game", white, green, light_green, 40)
    if click == "no":
        play_again_btn.reset_game()

    if check_for_win() or (round_num == 9 and not check_for_win()):
        if click == "no":
            next_round_button()

    if click == "no":
        quit_button()

    # AI start
    impossible_AI()

    # AI end

    # score-text start
    font = pygame.font.SysFont(None, 70)

    player_text = font.render("Player: " + str(points_player), True, blue)
    computer_text = font.render("Computer: " + str(points_computer), True, red)
    ties_text = font.render("Ties: " + str(ties), True, white)

    screen.blit(player_text, ((600 - player_text.get_rect().width / 2), 50))
    screen.blit(computer_text, (0, 50))
    screen.blit(ties_text, (1200 - ties_text.get_rect().width, 50))

    # score-text end

    settings_btn()

    pygame.display.update()
# Draw end
