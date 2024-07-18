#импорт необходимых библиотек
from googletrans import Translator # библиотека для API Google Translate
import pytesseract # библиотека с обученной нейросетью
import easyocr # ИНС для распознавания текста
from tkinter import * #библиотека для GUI
from tkinter import ttk # дополнение к основной библиотеке по графике
from PIL import ImageTk, Image, ImageFilter # библиотека для работы с картинками
from tkinter.filedialog import askopenfile # библиотека для работы с файлами
from urllib.request import urlopen # для открытия изображения по ссылке

is_chosen = False # глобальная переменная, выьрано ли изображение для анализа?
rus = 'Rus'  
eng = 'Eng'
both = 'both'
lang = rus  # глобальная переменная, язык для обработки
str = None # глобальная переменная для корректной работы переводчика
# набор сокращенных названий языков для работы с переводчиком
languages_short = ["af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "ny", "zh-cn", "zh-tw", "co", 
             "hr", "cs", "da", "nl", "en", "eo", "et", "tl", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw",
             "iw", "hi", "hmn", "hu", "is", "ig", "id", "ga", "it", "ja", "jw", "kn", "kk", "km", "ko", "ku", "ky", "lo", "la", 
             "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "ps", "fa", "pl", "pt", "pa", 
             "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tg", "ta", "te", 
             "th", "tr", "uk", "ur", "uz", "vi", "cy", "xh", "yi", "yo", "zu", "fil", "he"]
#полные названия языков для перевода
languages_full = ["afrikaans", "shqip", "አማርኛ", "العربية", "հայերեն", "azərbaycanlı", "euskalduna", "беларускі",
    "বাংলা", "bosanski", "български", "català", "Cebuano", "chichewa", "简体中文）", "c漢語 (繁體)","Corsu", "Hrvatski",
    "čeština", "dansk", "Nederlands", "english", "esperanto", "eestlane", "pilipino", "Suomalainen","français", 
    "frisian", "galego", "ქართველი", "Deutsch", "Ελληνικά", "ગુજરાતી", "kreyol ayisyen", "hausa", "ʻŌlelo Hawaiʻi",
    "עִברִית", "हिंदी", "hmoob", "Magyar", "íslensku", "igbo", "bahasa Indonesia", "Gaeilge", "italiano", "日本語", 
    "basa jawa", "ಕನ್ನಡ", "қазақ", "ខ្មែរ", "한국인", "kurdî (kurmancî)", "Кыргызча", "ລາວ", "latin", "latviski", 
    "lietuvis", "lëtzebuergesch", "македонски", "malagasy", "melayu", "മലയാളം", "malti", "maori", "मराठी", "монгол", 
    "မြန်မာ (ဗမာ)", "नेपाली", "norsk", "پښتو", "فارسی", "polski", "português", "punjabi", "Română", "русский", "samoa",
    "Gàidhlig na h-Alba", "Српски", "sesotho", "shona", "سنڌي", "සිංහල", "slovenský", "Slovenščina", "somaliyeed", "español",
    "basa sunda", "kiswahili", "svenska", "тоҷикӣ", "தமிழ்", "తెలుగు", "แบบไทย", "Türkçe", "український", "اردو", "o'zbek",
    "Tiếng Việt", "cymraeg", "isiXhosa", "ייִדיש", "yoruba", "zulu", "Filipino"]

#дополнительная фильтрация перед обработкой
def filter():
  global image  # преобоазование изображения в формат RGB
  if image.mode == "P":
    image = image.convert("RGB")
  filtered_image = image.filter(ImageFilter.MedianFilter(size=1))
  gray_image = filtered_image.convert("L") # сначала используется медианный фильтр с ядром равным 1
  threshold = 150
  img_binary = gray_image.point(lambda p: p > threshold and 255)
  image = img_binary  # затем изображение переводится в черно-белый формат

def openImage(): # функция для открытия изображения
  # открываем файловую систему и получаем изобраxжение
  global last #вспомогательная переменная, показывает последний выбранный способ открытия изображения
  last = "file"
  global f #открываем изображение
  f = askopenfile(mode ='r', filetypes =[('картинки', '*.png'), ('картинки', '*.jpeg'), ('картинки', '*.jpg')])
  if f is not None: # если получено изображение
    h = ttk.Scrollbar(inner_frame, orient=HORIZONTAL) #создаем два скролла
    v = ttk.Scrollbar(inner_frame, orient=VERTICAL)
    canvas = Canvas(inner_frame, width=400, height=300, scrollregion=(0, 0, 1000, 1000), bg="white", yscrollcommand=v.set, xscrollcommand=h.set) # рисуем это изображение
    canvas.grid(row=0, column=0) #добавляем поле на экран
    h.grid(column=0, row=1, sticky=(W,E))
    v.grid(column=1, row=0, sticky=(N,S))
    global image
    image = Image.open(f.name) # переменная для работы с изображением
    canvas.image = ImageTk.PhotoImage(image) #рисуем картинку на экране
    canvas.create_image(0, 0, image=canvas.image, anchor=NW)
    h["command"] = canvas.xview
    v["command"] = canvas.yview
    filter() # применяем фильтры к изображению
    global is_chosen # говорим что выбрано изображение
    is_chosen = True

def load(): # загрузить картинку по ссылке
  global url_str  # получаем ссылку
  url_str = entry.get()
  global last
  last = "url" # устанавливаем, что работали по ссылке
  global image
  image = Image.open(urlopen(url_str)) # получаем изображение
  h = ttk.Scrollbar(inner_frame, orient=HORIZONTAL)
  v = ttk.Scrollbar(inner_frame, orient=VERTICAL)
  canvas = Canvas(inner_frame, width=400, height=300, scrollregion=(0, 0, 1000, 1000), bg="white", yscrollcommand=v.set, xscrollcommand=h.set) # рисуем это изображение
  canvas.grid(row=0, column=0)
  h.grid(column=0, row=1, sticky=(W,E))
  v.grid(column=1, row=0, sticky=(N,S))           # рисуем изображение
  canvas.image = ImageTk.PhotoImage(image)
  canvas.create_image(0, 0, image=canvas.image, anchor=NW)
  h["command"] = canvas.xview
  v["command"] = canvas.yview
  filter()   #применяем фильтры
  global is_chosen # говорим что выбрано изображение
  is_chosen = True

def tesseract(): # функция вызывающая нейросеть PyTesseract
  lang = choisen_label["text"]   #получаем язык 
  param = ''  # в зависимости от выбранного языка вы выбираем как будет работать ИНС
  if lang == 'Eng':   #Даже если выберем оба языка, то ИНС может давать сбои. Ей нужно точно знать
    param = 'eng'
    print("english")    
  elif lang == 'Rus':
    param = 'rus'
    print("russkie")    
  else:
    param = 'rus+eng'
    print("both")
  if is_chosen == False: # если пользователь не выбрал изображение
    text.replace("1.0", END, "Вы не выбрали изображение")
  else: # если пользователь выбрал изображение, то применяем готовую ИНС
    string = pytesseract.image_to_string(image, lang=param)
    text.replace("1.0", END, string) # записываем работу ИНС в текстовое поле

def easyOCR(): #функция вызова нейросети EasyOCR
  lang = choisen_label["text"]  #получаем язык
  param = [""]
  if lang == 'Eng':
    param = ["en"]
    print("english")
  elif lang == 'Rus':
    param = ["ru"]
    print("russki")
  else:
    param = ["en", "ru"]
    print("both")

  if is_chosen == False: # если пользователь не выбрал изображение
    text.replace("1.0", END, "Вы не выбрали изображение")
  else:   #по разному работает для файла и ссылки
    rreader = easyocr.Reader(param)
    if last == "file":
      string = rreader.readtext(f.name, detail=0, paragraph=True)
    else:
      string = rreader.readtext(url_str, detail=0, paragraph=True)
    text.replace("1.0", END, string[0])  #считанный текст добавляем на экран

def translate(): #функция перевода отсканированного текста
  lang_trans = combobox.get() #получаем язык на который будем переводить
  global str
  if str == None:
    str = text.get("1.0", END) #получаем текст который переведем
  translator = Translator() #класс для работы с апи гугла
  index = languages_full.index(lang_trans)
  dest = languages_short[index]
  result = translator.translate(str, dest=dest) #переведенный текст
  text.insert(END, result) # вставляем в конец перевод

# описание главного окна
root = Tk()    # создаем корневой объект - окно
root.title("Распознование текста на изображении")     # устанавливаем заголовок окна
#root.iconbitmap("@./icon.xbm") # иконка (не работает)
root.geometry("1200x510+200+200")    # устанавливаем размеры окна
root.resizable(True, False) # блокируем изменение размеров окна
lang_trans = "english" #по умолчанию ставим английский

# контейнеры для удобства расположения элементов управления
left_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10], height=450) #левый контейнер для кнопок
center_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10]) # по центру будет изображение
right_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10]) # справа полученный текст
inner_frame = ttk.Frame(center_frame, borderwidth=1, relief=SOLID, width=410, height=310) # доп контейнер для канваса

#комбобох для выбора языка на который переведем
combobox = ttk.Combobox(left_frame, values=languages_full, textvariable=lang_trans, state="readonly") 

#кнопка по которой мы вызываем команду перевести
translate_btn = Button(left_frame, text='Перевести', command=translate)

#описание кнопки открытия изображения из файловой системы компьютера
open_button = Button(left_frame, text="открыть картинку", command=openImage) 

# кнопка вызова PyTesseract
PyTesseract_button = Button(center_frame, text="PyTesseract", command=tesseract)

# кнопка вызова EasyOCR
MyNN_button = Button(center_frame, text="EasyOCR", command=easyOCR)

# описание надписей
Greeting_label = Label(left_frame, text="Выберите изображение для обработки") #  выберите
label = Label(left_frame, text='Или вставьте ссылку на изображение') # ссылка
img_label = Label(center_frame, text='Ваше изображение')
recieved_text = Label(right_frame, text='Полученный текст с изображения')
text = Text(right_frame, width=50) # содержит текст, полученный после работы ИНС
choise_label = Label(left_frame, text='Выберите язык, который присутствует на картинке', wraplength=280)
choisen_label = Label(left_frame, textvariable=lang) # показывает язык который присутствует на картинке
translate_label = Label(left_frame, text='Выберите язык, на который хотите перевести текст', wraplength=250)
chosenLang_label = Label(left_frame, textvariable=lang_trans)

# кнопки выбора языка который есть на изобраэении
Rus_btn = ttk.Radiobutton(left_frame, text='Русский', value=rus, variable=lang)
Eng_btn = ttk.Radiobutton(left_frame, text='Английский', value=eng, variable=lang)
Both_btn = ttk.Radiobutton(left_frame, text='Оба языка', value=both, variable=lang)

# поле ввода ссылки на изображение
entry = ttk.Entry(left_frame)

# кнопка загрузки изображения из интернета
url_button = Button(left_frame, text="Загрузить картинку", command=load)

# устанавливаем элементы на окне
left_frame.grid(row=0, column=0, padx=5, pady=5, sticky=NS)
Greeting_label.pack(side=TOP)
open_button.pack(fill=X, pady=[0, 30])
label.pack()
entry.pack(fill=X)
url_button.pack(fill=X)
choise_label.pack(pady=[30, 20])
Rus_btn.pack()
Eng_btn.pack()
Both_btn.pack()
choisen_label.pack()
translate_label.pack(pady=5)
combobox.pack(pady=5)
translate_btn.pack()
chosenLang_label.pack()

center_frame.grid(row=0, column=1, padx=5, pady=5, sticky=NS)
img_label.grid(row=0, column=0, ipadx=6, ipady=6, padx=4, pady=4, sticky=EW)
inner_frame.grid(row=1, column=0, ipadx=6, ipady=6, padx=4, pady=4, sticky=EW)
PyTesseract_button.grid(row=2, column=0, ipadx=6, ipady=6, padx=4, pady=4, sticky=EW)
MyNN_button.grid(row=3, column=0, ipadx=6, ipady=6, padx=4, pady=4, sticky=EW)

right_frame.grid(row=0, column=2, padx=5, pady=5, sticky=NSEW)
recieved_text.pack(side=TOP)
text.pack()

root.update_idletasks() # применяем изменения дизайна принудительно
root.mainloop() # запускаем главное окно