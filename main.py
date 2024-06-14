import tkinter as tk
from inputs import get_gamepad
import math
from PIL import Image, ImageTk

update_delay = 1

class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self, root):
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.root = root
        self._monitor_controller()

    def read(self):
        lt = self.LeftTrigger
        rt = self.RightTrigger
        lyx = self.LeftJoystickX
        lyy = self.LeftJoystickY
        return [lt, rt, lyx, lyy]

    def _monitor_controller(self):
        events = get_gamepad()
        for event in events:
            if event.ev_type == 'Absolute':
                if event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL
                elif event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL
            elif event.ev_type == 'Key':
                if event.code == 'BTN_WEST':
                    self.X = event.state
                    if self.X == 1:
                        canvas.itemconfig(x_pressed_bg, state="normal")
                        canvas.itemconfig(x_pressed_text, state="normal")
                    else:
                        canvas.itemconfig(x_pressed_bg, state="hidden")
                        canvas.itemconfig(x_pressed_text, state="hidden")
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                    if self.B == 1:
                        canvas.itemconfig(b_pressed_bg, state="normal")
                        canvas.itemconfig(b_pressed_text, state="normal")
                    else:
                        canvas.itemconfig(b_pressed_bg, state="hidden")
                        canvas.itemconfig(b_pressed_text, state="hidden")

        self.root.after(update_delay, self._monitor_controller)

def update_ui(lt_value, rt_value, lyx, lyy):
    lt_bar_height = int(lt_value * HEIGHT)
    rt_bar_height = int(rt_value * HEIGHT)

    canvas.coords(lt_bar, LT_BAR_X, HEIGHT - lt_bar_height, LT_BAR_X + BAR_WIDTH, HEIGHT)
    canvas.coords(rt_bar, RT_BAR_X, HEIGHT - rt_bar_height, RT_BAR_X + BAR_WIDTH, HEIGHT)

    new_angle = (math.degrees(math.atan2(lyx, -lyy)) + 180) % 360
    global angle
    if new_angle != angle:
        angle = new_angle
        rotated_image = image.rotate(angle)
        tk_image = ImageTk.PhotoImage(rotated_image)
        canvas.itemconfig(steering_wheel, image=tk_image)
        canvas.image = tk_image

WIDTH, HEIGHT = 600, 300
BAR_WIDTH = 50
SPACING = 100
LT_BAR_X = WIDTH // 4 - BAR_WIDTH // 2
RT_BAR_X = 3 * WIDTH // 4 - BAR_WIDTH // 2

root = tk.Tk()
root.title("STUPID PROJECT BY luxz#8403")
root.wm_attributes("-transparentcolor", root['bg'])
root.attributes('-topmost', True)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT+50, bg=root['bg'], highlightthickness=0)
canvas.pack()

image_path = "image.png"
image = Image.open(image_path)
image = image.resize((150, 150), Image.Resampling.LANCZOS)

lt_bar = canvas.create_rectangle(LT_BAR_X, HEIGHT, LT_BAR_X + BAR_WIDTH, HEIGHT, fill="red", outline="black", tags="lt_bar")
rt_bar = canvas.create_rectangle(RT_BAR_X, HEIGHT, RT_BAR_X + BAR_WIDTH, HEIGHT, fill="green", outline="black", tags="rt_bar")

steering_wheel = canvas.create_image(WIDTH // 2, HEIGHT // 2, image=None, tags="steering_wheel")

x_pressed_text = canvas.create_text(WIDTH // 2, HEIGHT, text="ลดเกียร์", fill="indianred3", font=('Tahoma', 15))
x_pressed_bg = canvas.create_rectangle(canvas.bbox(x_pressed_text), fill="black")
canvas.tag_lower(x_pressed_bg, x_pressed_text)
canvas.itemconfig(x_pressed_bg, state="hidden")
canvas.itemconfig(x_pressed_text, state="hidden")

b_pressed_text = canvas.create_text(WIDTH // 2, HEIGHT, text="เพิ่มเกียร์", fill="seagreen2", font=('Tahoma', 15))
b_pressed_bg = canvas.create_rectangle(canvas.bbox(b_pressed_text), fill="black")
canvas.tag_lower(b_pressed_bg, b_pressed_text)
canvas.itemconfig(b_pressed_bg, state="hidden")
canvas.itemconfig(b_pressed_text, state="hidden")

joy = XboxController(root)

angle = 0

def update():
    lt_value, rt_value, lyx, lyy = joy.read()
    update_ui(lt_value, rt_value, lyx, lyy)
    root.after(update_delay, update)

update()

lt_label = canvas.create_text(LT_BAR_X + BAR_WIDTH // 2, HEIGHT + 20 , text="เบรก", fill="white", font=('Tahoma', 15))
lt_label_bg = canvas.create_rectangle(canvas.bbox(lt_label), fill="black")
canvas.tag_lower(lt_label_bg, lt_label)
rt_label = canvas.create_text(RT_BAR_X + BAR_WIDTH // 2, HEIGHT + 20, text="คันเร่ง", fill="white", font=('Tahoma', 15))
rt_label_bg = canvas.create_rectangle(canvas.bbox(rt_label), fill="black")
canvas.tag_lower(rt_label_bg, rt_label)

root.mainloop()
