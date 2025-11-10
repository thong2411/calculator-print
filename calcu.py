from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import socket
import threading
import json
import os


history = []
printer_ip = '192.168.1.100'
printer_port = 9100
printer_connected = False
config_file = 'printer_config.json'

#widget
display_label = None
expression_label = None
history_label = None
bg_rect = None

#config cấu hình
def load_printer_config():
    """Load cấu hình máy in từ file"""
    global printer_ip, printer_port
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                printer_ip = config.get('ip', '192.168.1.100')
                printer_port = config.get('port', 9100)
        else:
            printer_ip = '192.168.1.100'
            printer_port = 9100
    except:
        printer_ip = '192.168.1.100'
        printer_port = 9100
#Lưu cấu hình vào file máy in
def save_printer_config():
    """Lưu cấu hình máy in vào file"""
    global printer_ip, printer_port
    try:
        config = {'ip': printer_ip, 'port': printer_port}
        with open(config_file, 'w') as f:
            json.dump(config, f)
    except Exception as e:
        print(f"Không thể lưu cấu hình: {e}")

#giao diện
def update_bg(instance, value):
    """Cập nhật background"""
    global bg_rect
    bg_rect.pos = instance.pos
    bg_rect.size = instance.size
#cập nhật bảng lịch sử
def update_history_display():
    """Cập nhật hiển thị lịch sử"""
    global history, history_label
    if history:
        lines = ['[b]Lịch sử tính toán:[/b]']
        for i, calc in enumerate(history, 1):
            lines.append(f"  {i}. {calc}")
        history_label.text = '\n'.join(lines)
    else:
        history_label.text = '[b]Lịch sử tính toán:[/b]'

#hàm xử lý nút bấm
def on_button_press(instance):
    """Xử lý khi bấm nút"""
    global history, display_label, expression_label, printer_connected
    
    button_text = instance.text
    current_display = display_label.text
    #AC reset lịch sử và display
    if button_text == 'AC':
        display_label.text = '0'
        expression_label.text = ''
        history = []
        update_history_display()

    elif button_text == '=':
        try:
            result = eval(current_display)
            calculation = f"{current_display} = {result}"
            history.append(calculation)
            update_history_display()
            expression_label.text = current_display + ' ='
            display_label.text = str(result)
        except:
            display_label.text = 'Lỗi'
            expression_label.text = ''

    elif button_text == 'IN':
        if printer_connected:
            show_print_confirmation()
        else:
            print_history()

    elif button_text == 'C':
        if current_display != '0' and current_display != 'Lỗi':
            if len(current_display) > 1:
                display_label.text = current_display[:-1]
                expression_label.text = display_label.text
            else:
                display_label.text = '0'
                expression_label.text = ''

    elif button_text == 'DH':
        if history:
            history.pop()
            update_history_display()

    elif button_text == '.':
        if '.' not in current_display.split()[-1]:
            if current_display == '0':
                display_label.text = '0.'
            else:
                display_label.text += '.'
            expression_label.text = display_label.text

    else:
        if current_display == '0' or current_display == 'Lỗi':
            display_label.text = button_text
        else:
            display_label.text += button_text
        expression_label.text = display_label.text

#Hiện thị popup để điền IP và xác nhận in
def show_message(title, message):
    """Hiển thị thông báo popup"""
    content = BoxLayout(orientation='vertical', padding=10, spacing=10)
    content.add_widget(Label(
        text=message,
        color=(0, 0, 0, 1),
        size_hint_y=0.7
    ))
    
    popup = Popup(title=title, content=content, size_hint=(0.8, 0.3))
    
    btn = Button(
        text='Đóng',
        size_hint_y=0.3,
        background_color=(0.2, 0.6, 1, 1)
    )
    btn.bind(on_press=popup.dismiss)
    content.add_widget(btn)
    popup.open()

def show_print_confirmation():
    """Hiện popup xác nhận in"""
    global history, printer_ip, printer_port
    
    if not history:
        show_message("Thông báo", "Không có lịch sử để in!")
        return
        
    content = BoxLayout(orientation='vertical', padding=10, spacing=10)
    
    content.add_widget(Label(
        text=f'Bạn có muốn in {len(history)} phép tính?',
        size_hint_y=0.4,
        color=(0, 0, 0, 1),
        font_size='20sp',
        bold=True
    ))
    
    content.add_widget(Label(
        text=f'Máy in: {printer_ip}:{printer_port}',
        size_hint_y=0.3,
        color=(0.3, 0.3, 0.3, 1),
        font_size='16sp'
    ))
    
    btn_layout = BoxLayout(size_hint_y=0.3, spacing=10)
    popup = Popup(title='Xác nhận in', content=content, size_hint=(0.85, 0.35))
    #In ra lịch sử
    def on_confirm(instance):
        popup.dismiss()
        print_history()
    
    btn_print = Button(text='In ngay', background_color=(0.2, 0.8, 0.2, 1), font_size='18sp', bold=True)
    btn_print.bind(on_press=on_confirm)
    
    btn_cancel = Button(text='Hủy', background_color=(1, 0.3, 0.3, 1), font_size='18sp')
    btn_cancel.bind(on_press=popup.dismiss)
    
    btn_layout.add_widget(btn_cancel)
    btn_layout.add_widget(btn_print)
    content.add_widget(btn_layout)
    popup.open()

def show_printer_config_on_error(error_msg):
    """Hiển thị popup cấu hình khi có lỗi"""
    global printer_ip, printer_port
    
    content = BoxLayout(orientation='vertical', padding=10, spacing=10)
    
    content.add_widget(Label(
        text=f'[color=ff0000]Lỗi kết nối:[/color]\n{error_msg}\n\nVui lòng kiểm tra lại:',
        size_hint_y=0.3,
        color=(1, 0, 0, 1),
        markup=True
    ))
    
    content.add_widget(Label(text='Địa chỉ IP máy in:', size_hint_y=0.2, color=(0, 0, 0, 1)))
    ip_input = TextInput(text=printer_ip, multiline=False, size_hint_y=0.25, font_size='20sp')
    content.add_widget(ip_input)
    
    content.add_widget(Label(text='Cổng (Port):', size_hint_y=0.2, color=(0, 0, 0, 1)))
    port_input = TextInput(text=str(printer_port), multiline=False, size_hint_y=0.25, font_size='20sp')
    content.add_widget(port_input)

    btn_layout = BoxLayout(size_hint_y=0.3, spacing=10)
    popup = Popup(title='Cấu hình lại máy in', content=content, size_hint=(0.9, 0.7))
    
    def on_retry(instance):
        global printer_ip, printer_port
        printer_ip = ip_input.text
        try:
            printer_port = int(port_input.text)
        except:
            show_message("Lỗi", "Port phải là số!")
            return
        save_printer_config()
        popup.dismiss()
        print_history()
    
    btn_retry = Button(text='Thử lại', background_color=(0.2, 0.8, 0.2, 1))
    btn_retry.bind(on_press=on_retry)
    
    btn_cancel = Button(text='Hủy', background_color=(1, 0.3, 0.3, 1))
    btn_cancel.bind(on_press=popup.dismiss)
    
    btn_layout.add_widget(btn_cancel)
    btn_layout.add_widget(btn_retry)
    content.add_widget(btn_layout)
    popup.open()

# ========== HÀM IN ==========
def print_history():
    """Gửi lịch sử qua mạng LAN"""
    global history
    
    if not history:
        show_message("Thông báo", "Không có lịch sử để in!")
        return

    thread = threading.Thread(target=send_to_printer)
    thread.daemon = True
    thread.start()

def send_to_printer():
    """Gửi dữ liệu qua socket TCP"""
    global printer_ip, printer_port, printer_connected, history
    
    try:
        content = format_print_content()
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((printer_ip, printer_port))
        
        sock.sendall(content.encode('utf-8'))
        sock.close()
        
        printer_connected = True
        Clock.schedule_once(lambda dt: show_message("Thành công", f"Đã gửi {len(history)} phép tính đến máy in!"), 0)
        
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        printer_connected = False
        error_msg = str(e)
        Clock.schedule_once(lambda dt: show_printer_config_on_error(error_msg), 0)
    except Exception as e:
        printer_connected = False
        error_msg = str(e)
        Clock.schedule_once(lambda dt: show_printer_config_on_error(error_msg), 0)

def format_print_content():
    """Định dạng nội dung in"""
    global history
    
    lines = []
    lines.append("=" * 40)
    lines.append("LỊCH SỬ TÍNH TOÁN")
    lines.append("=" * 40)
    
    for i, calc in enumerate(history, 1):
        lines.append(f"{i}. {calc}")
    
    lines.append("=" * 40)
    lines.append(f"Tổng: {len(history)} phép tính")
    lines.append("=" * 40)
    lines.append("\n\n\n")
    
    content = "\n".join(lines)
    content += "\x1B\x6D"
    return content

# ========== KHỞI TẠO GIAO DIỆN ==========
def create_circle_button(text, font_size, color_rgba):
    """Tạo nút tròn"""
    from kivy.graphics import Ellipse
    
    btn = Button(
        text=text,
        font_size=font_size,
        bold=True,
        color=(0, 0, 0, 1),
        background_normal='',
        background_down='',
        background_color=(0, 0, 0, 0)
    )
    
    with btn.canvas.before:
        color_inst = Color(*color_rgba)
        circle = Ellipse(pos=btn.pos, size=btn.size)
    
    def update_circle(instance, value):
        circle.pos = instance.pos
        circle.size = instance.size
    
    btn.bind(pos=update_circle, size=update_circle)
    btn.bind(on_press=on_button_press)
    
    return btn

def build_app():
    """Xây dựng giao diện"""
    global display_label, expression_label, history_label, bg_rect
    
    Window.size = (400, 700)
    load_printer_config()
    
    main_layout = BoxLayout(orientation='vertical', padding=[10, 10, 10, 10], spacing=10)
    with main_layout.canvas.before:
        Color(1, 1, 1, 1)
        bg_rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
    main_layout.bind(size=update_bg, pos=update_bg)

    # Lịch sử
    history_scroll = ScrollView(size_hint_y=0.25, do_scroll_x=False, bar_width=10)
    history_label = Label(
        text='Lịch sử tính toán:',
        size_hint_y=None,
        height=1500,
        halign='left',
        valign='top',
        font_size='18sp',
        color=(0.2, 0.2, 0.2, 1),
        markup=True,
    )
    history_label.bind(size=lambda s, _: setattr(s, 'text_size', (s.width, None)))
    history_label.bind(texture_size=lambda i, v: setattr(i, 'height', v[1]))
    history_scroll.add_widget(history_label)

    # Biểu thức
    expression_label = Label(
        text='',
        size_hint_y=0.07,
        halign='right',
        valign='bottom',
        font_size='20sp',
        color=(0.5, 0.5, 0.5, 1)
    )
    expression_label.bind(size=expression_label.setter('text_size'))

    # Kết quả
    display_label = Label(
        text='0',
        size_hint_y=0.11,
        halign='right',
        valign='middle',
        font_size='48sp',
        bold=True,
        color=(0, 0, 0, 1)
    )
    display_label.bind(size=display_label.setter('text_size'))

    # Nút bấm
    buttons_layout = GridLayout(cols=4, spacing=[10, 10], padding=[5, 5, 5, 5], size_hint_y=0.57)
    
    buttons = [
        ['7', '8', '9', '/'],
        ['4', '5', '6', '*'],
        ['1', '2', '3', '-'],
        ['AC', '0', '=', '+'],
        ['IN', '.', 'C', 'DH']
    ]
    
    color_map = {
        'IN': (0.2, 0.6, 1, 1),
        'AC': (1, 0.3, 0.3, 1),
        '=': (0.2, 0.8, 0.2, 1),
        'C': (1, 0.6, 0.2, 1),
        'DH': (0.9, 0.4, 0.7, 1)
    }

    for row in buttons:
        for button_text in row:
            font = '32sp' if button_text in ['IN', 'C', 'DH'] else '28sp'
            color = color_map.get(button_text, (0.85, 0.85, 0.85, 1))
            btn = create_circle_button(button_text, font, color)
            buttons_layout.add_widget(btn)

    main_layout.add_widget(history_scroll)
    main_layout.add_widget(expression_label)
    main_layout.add_widget(display_label)
    main_layout.add_widget(buttons_layout)
    
    return main_layout

# ========== CHẠY ỨNG DỤNG ==========
class CalculatorApp(App):
    def build(self):
        self.title = 'Máy Tính'
        return build_app()

if __name__ == '__main__':
    CalculatorApp().run()