import easyocr
from PIL import Image
import os
import cv2
import numpy as np

def preprocess_image(image_path):
    # قراءة الصورة باستخدام OpenCV
    image = cv2.imread(image_path)
    
    # تحويل الصورة إلى grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # تحسين التباين باستخدام CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_enhanced = clahe.apply(gray)
    
    # إزالة الضوضاء باستخدام مرشح ثنائي
    denoised = cv2.bilateralFilter(contrast_enhanced, 9, 75, 75)
    
    # تحسين حواف النص
    kernel = np.ones((1, 1), np.uint8)
    sharpened = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)
    
    # حفظ الصورة المعالجة مؤقتاً
    temp_path = "temp_processed.png"
    cv2.imwrite(temp_path, sharpened)
    
    return temp_path

def extract_text(image_path, reader):
    # معالجة الصورة
    processed_image_path = preprocess_image(image_path)
    
    # قراءة النص مع تحسين الإعدادات
    results = reader.readtext(
        processed_image_path,
        paragraph=True,
        contrast_ths=0.2,
        adjust_contrast=0.5,
        width_ths=0.7,
        height_ths=0.7
    )
    
    # حذف الصورة المؤقتة
    if os.path.exists(processed_image_path):
        os.remove(processed_image_path)
        
    return results

# تهيئة EasyOCR
reader = easyocr.Reader(['en', 'ar'])

# المسار الرئيسي للصور
folder_path = r"C:\Users\plane\Downloads\OCR\Images"

# مسار حفظ النصوص
folder_path2 = r"C:\Users\plane\Downloads\OCR\Extracted_Texts" # قابل للتغيير

# التحقق من وجود مجلد النصوص أو إنشائه
if not os.path.exists(folder_path2):
    os.makedirs(folder_path2)

# معالجة كل الصور
for image_name in os.listdir(folder_path):
    if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.gif', '.webp', '.jpeg_large')):
        image_path = os.path.join(folder_path, image_name)
        
        try:
            # استخراج النص
            results = extract_text(image_path, reader)
            
            # حفظ النص في ملف داخل المجلد الثاني
            txt_filename = os.path.splitext(image_name)[0] + ".txt"
            txt_filepath = os.path.join(folder_path2, txt_filename)
            
            with open(txt_filepath, "w", encoding="utf-8") as file:
                for result in results:
                    # التحقق من طول النتيجة وأخذ النص منها
                    if len(result) >= 2:
                        text = result[1]  # النص دائماً في العنصر الثاني
                        file.write(f"{text}\n")
        
        except Exception as e:
            print(f"حدث خطأ في معالجة الصورة {image_name}: {str(e)}")
            continue