import shutil

file_path = 'src/ESP32_radio_evo3.22/Arduino/src/ESP32_radio_evo3.22.01.ino'
backup_path = file_path + '.bak2'

# Делаем второй бэкап
shutil.copy(file_path, backup_path)
print("Backup created:", backup_path)

with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

mock_class = '''
// --- MOCK U8G2 CLASS FOR LCD 2004 ---
class MockU8g2 {
public:
    void begin() {}
    void clearBuffer() { lcd.clear(); }
    void sendBuffer() {}
    void setFont(const uint8_t* font) {}
    void setDrawColor(int c) {}
    void drawBox(int x, int y, int w, int h) {}
    void drawFrame(int x, int y, int w, int h) {}
    void drawLine(int x1, int y1, int x2, int y2) {}
    void setCursor(int x, int y) {}
    void setPowerSave(int p) { if(p) lcd.noBacklight(); else lcd.backlight(); }
    
    // Главный метод вывода текста
    void drawStr(int x, int y, const char* str) {
        // Перевод графических координат (256x64) в текстовые (20x4)
        int row = y / 16; 
        if (row > 3) row = 3;
        int col = x / 13; 
        if (col > 19) col = 19;
        
        lcd.setCursor(col, row);
        lcd.print(str);
        // Очистка остатка строки
        for(int i=0; i<5; i++) lcd.print(" "); 
    }
    void drawUTF8(int x, int y, const char* str) { drawStr(x, y, str); }
};
MockU8g2 u8g2;
// ------------------------------------
'''

# Внедряем заглушку сразу после библиотек
target_include = '#include <LiquidCrystal_I2C.h>'
assert target_include in code, "LCD include not found"
code = code.replace(target_include, target_include + '\n' + mock_class)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Mock U8g2 class injected successfully!")
