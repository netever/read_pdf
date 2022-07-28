import logging
import inspect
import os
import sys
from pdf2image import convert_from_path


def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

def get_books():
    folder = get_script_dir() + '/books/'
    return os.listdir(folder)

def get_image(path, page=None):
    pdf_file = get_script_dir() + '/books/' + path + '.pdf'
    file = ''

    logging.info('Задал переменные')
    if page == None:
        return None
    try:
        logging.info('Пытаюсь конвертить')
        pages = convert_from_path(pdf_file, first_page=page, last_page=page+1)
        logging.info('Успех!')

        for bookpage in pages:
            logging.info('!')
            file = get_script_dir() + '/images/{}{}.jpg'.format(path, page)
            logging.info('Пробую засейвить')
            bookpage.save(file, 'JPEG')
            logging.info('Неудача...')
    except Exception as e:
        logging.info('Какая-то неудача :(')
        return None
   
    return file

def delete_image(file):
    os.remove(file)