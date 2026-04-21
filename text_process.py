from docx import Document
from docx.shared import Pt
import time
import pyautogui
import pyperclip
import sys
import os

pyautogui.FAILSAFE = False
def extract_heading_from_block(block):
    
    for line in block.splitlines():
        if line.startswith("---") and line.endswith("---"):  # Проверяем формат "---Заголовок---"
            return line.strip("---")  # Возвращаем текст без "---"
    return None



    doc = Document()
    
    # Пример обработки заголовков, жирного и наклонного шрифта
    paragraphs = text.split('\n')  # Разделяем текст на абзацы

    for para in paragraphs:
        if para.startswith('###'):  # Заголовки 3 уровня
            heading = doc.add_heading(level=3)  # Создаем заголовок уровня 3
            heading.add_run(para[3:].strip())  # Оставляем текст после '###'
        elif '**' in para:  # Обработка жирного текста
            run = doc.add_paragraph().add_run(para.replace('**', ''))
            run.bold = True
        elif '*' in para:  # Обработка наклонного текста
            run = doc.add_paragraph().add_run(para.replace('*', ''))
            run.italic = True
        else:
            doc.add_paragraph(para)  # Добавление обычного абзаца

    return doc

def read_docx_in_blocks(file_path, block_size, min_paragraph_length=30):
    """
    Читает текст из Word-документа, разбивает на блоки и помечает заголовки.
    
    :param file_path: путь к файлу .docx
    :param block_size: количество абзацев в одном блоке
    :param min_paragraph_length: минимальная длина абзаца для включения
    :return: список блоков текста
    """
    document = Document(file_path)
    
    paragraphs = []
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        
        # Пропускаем пустые абзацы или слишком короткие
        if len(text) < min_paragraph_length:
            continue
        
        # Проверяем, является ли абзац заголовком
        if "Heading" in paragraph.style.name or "Заголовок" in paragraph.style.name:
            paragraphs.append(f"---{text}---")
        else:
            paragraphs.append(text)

    # Разбиваем абзацы на блоки
    blocks = [paragraphs[i:i + block_size] for i in range(0, len(paragraphs), block_size)]
    return ["\n".join(block) for block in blocks]  # Объединяем абзацы в блоки

file_path = r"c:\\Users\\Prog8\\Desktop\\Lucien_van_der_Walt,_Michael_Schmidt_Black_Flame_The_Revolutionary.docx"
output_path = r"c:\\Users\\Prog8\\Desktop\\output.docx"


# конспекта называется анализом или сводкой (summary) ключевых моментов текста с выделением основных идей и выводов. Он направлен на выделение важной информации, что облегчает дальнейшее изучение или использование материала. В данном случае это также можно назвать кратким пересказом с акцентом на основные идеи.

# Если нужно более официальное или академическое название, это может быть систематизированный обзор.

# Создаем новый документ или загружаем существующий, если файл уже есть
if os.path.exists(output_path):
    doc = Document(output_path)
else:
    doc = Document()

try:
    text_blocks = read_docx_in_blocks(file_path, 8)
    print(len(text_blocks))
    for i, block in enumerate(text_blocks):
        heading = extract_heading_from_block(block)
        
        if (i < 23):
             continue
        print(i)
        time.sleep(2)
        combined_arr = [
        f"make conspect (на русском пункты). 7 пунктов в них 3 подпункта. Также дополнительно к пункту одна цитата из текста (английский) Приводи цифры, исследователей, факты, имена\n{block}"
        , 
        f"сделай анализ (summary), разбив на темы и подтемы. Не упусти ничего что касается цифр, исслоедований, дат и основных фактов и имен \n{block}"]


        combined_text = combined_arr[1]
        pyperclip.copy(combined_text)


        time.sleep(2)
        pyautogui.click(908, 953)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.click(908, 954)
        time.sleep(2)
        # print(pyautogui.position())
        pyautogui.press('enter')

        time.sleep(80)
        x, y = pyautogui.position()
        print(f"Текущая позиция курсора: ({x}, {y})")
        pyautogui.click(1077, 888)
        time.sleep(2)
        
        print(f"Текущая позиция курсора: ({x}, {y})")
        time.sleep(2)
        pyautogui.click(807, 848)
        time.sleep(1)
        text = pyperclip.paste()

        if heading:
            doc.add_heading(heading, level=1)

        # Добавляем индекс i в начало
        doc.add_paragraph(f"Индекс {i}:", style="Heading 2")

        # Разделяем текст по строкам и добавляем их с форматированием
        for line in text.split("\n"):
            if line.startswith("###"):  # Заголовок третьего уровня
                cleaned_line = line.replace("**", "").replace("#", "").replace("###", "").replace("---", "").strip()
                doc.add_paragraph(cleaned_line, style="Heading 3")
            elif line.startswith("####"):  # Заголовок четвертого уровня
                cleaned_line = line.replace("**", "").replace("#", "").replace("####", "").replace("---", "").strip()
                doc.add_paragraph(cleaned_line, style="Heading 4")
            else:
                # Создаем параграф для строки
                par = doc.add_paragraph()
                words = line.split("**")  # Разбиваем строку для обработки жирного текста
                for idx, word in enumerate(words):
                    if idx % 2 == 1:  # Это жирный текст
                        par.add_run(word).bold = True
                    else:
                        subwords = word.split("*")  # Разбиваем для обработки курсива
                        for j, subword in enumerate(subwords):
                            if j % 2 == 1:  # Это наклонный текст
                                par.add_run(subword).italic = True
                            else:  # Обычный текст
                                par.add_run(subword)

        # Сохраняем изменения после обработки каждого блока
        doc.save(output_path)

except KeyboardInterrupt:
    print("Прерывание программы пользователем. Сохраняем изменения...")
    doc.save(output_path)
    raise

except Exception as e:
    print(f"Ошибка: {e}")
    # Сохраняем прогресс в случае ошибки
    doc.save(output_path)
