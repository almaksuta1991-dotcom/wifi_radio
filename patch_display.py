import shutil
import re

file_path = 'src/ESP32_radio_evo3.22/Arduino/src/ESP32_radio_evo3.22.01.ino'
backup_path = file_path + '.bak'

# 1. Делаем бэкап
shutil.copy(file_path, backup_path)
print("Backup created:", backup_path)

with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 2. Меняем библиотеку
assert '#include <U8g2lib.h>' in code, "U8g2 include not found"
code = code.replace('#include <U8g2lib.h>', '#include <Wire.h>\n#include <LiquidCrystal_I2C.h>')

# 3. Заменяем создание объекта OLED на LCD
# Ищем строку с инициализацией SH1122 (строка 592)
oled_pattern = re.compile(r'U8G2_SH1122_256X64_F_4W_HW_SPI u8g2\([^;]+\);')
assert oled_pattern.search(code), "OLED init string not found"
lcd_init = "LiquidCrystal_I2C lcd(0x27, 20, 4); // I2C addr 0x27, 20 chars, 4 lines"
code = oled_pattern.sub(lcd_init, code)

# 4. Добавляем Wire.begin(8, 9) и lcd.init() в функцию setup()
# Ищем void setup() { и вставляем после скобки
setup_pattern = re.compile(r'void setup\(\)\s*\{')
assert setup_pattern.search(code), "setup() not found"
setup_injection = "void setup() {\n  Wire.begin(8, 9); // SDA=8, SCL=9\n  lcd.init();\n  lcd.backlight();\n"
code = setup_pattern.sub(setup_injection, code, count=1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Patch applied successfully!")
