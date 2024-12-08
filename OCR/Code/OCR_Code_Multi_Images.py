import easyocr
from PIL import Image
import os

# تحديد قارئ EasyOCR مع اللغة
reader = easyocr.Reader(['en', 'ar'])

# تحديد مسار مجلد الصور
folder_path = r"C:\Users\plane\Downloads\OCR\Images" # قابل للتغيير

# تحديد مسار مجلد حفظ النصوص
folder_path2 = r"C:\Users\plane\Downloads\OCR\Extracted_Texts" # قابل للتغيير

# التحقق من وجود المجلد الثاني، وإن لم يكن موجودًا يتم إنشاؤه
if not os.path.exists(folder_path2):
    os.makedirs(folder_path2)

# استخراج النصوص من جميع الصور في المجلد
for image_name in os.listdir(folder_path):
    # التحقق من أن الملف هو صورة
    if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(folder_path, image_name)
        image = Image.open(image_path)

        # استخراج النصوص من الصورة
        results = reader.readtext(image_path)

        # تحديد اسم الملف النصي بناءً على اسم الصورة
        txt_filename = os.path.splitext(image_name)[0] + ".txt"
        txt_filepath = os.path.join(folder_path2, txt_filename)

        # حفظ النصوص المستخرجة في الملف النصي
        with open(txt_filepath, "w", encoding="utf-8") as file:
            for (_, text, _) in results:
                file.write(f"{text}\n")

        print(f"تم حفظ النصوص في الملف: {txt_filepath}")