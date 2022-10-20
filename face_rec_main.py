import face_recognition
from imutils import paths
from excel_func import create_book, add_info_to_book
from varname import nameof
import time
import json


def percent(num: int or float, total: int or float) -> float:
    result = (num * 100) / total
    return float("{:.2f}".format(result))


def compare_faces(img1_path: str, imgs_path: list, name_sheets: str, create_xlsx=False) -> dict:
    """
    Функция ищет лицо определенное на изображении img1_path, во всех изображениях расположенных по imgs_path.
    Принимает на вход изображения, декодирует их в 128-мерную кодировку лица и сравнивает с
    кодировками кандидатов.

    При значении переменной create_xlsx=True, функция записывает в книгу новый лист, со строкой в виде:
    Фотография - путь до фотографии - результат сравнения

    :param img1_path: Путь до базовой фотографии с лицом
    :param imgs_path: Список состоящий из путей до фотографий-кандидатов на сравнение
    :param name_sheets: Название листа в xlsx-документе
    :param create_xlsx: Булево значение для определения необходимости создания xlsx-документа

    :return:  {
        "count_True": int, - Количество найденных совпадений
        "counter_True_precent": float, Процент совпадений от общего числа фотографий
        "count_False": int, Количество не найденных совпадений
        "counter_False_precent": float, Процент не найденных совпадений от общего числа фотографий
        "count_Not-found": int, - Случаи не распознанных лиц на фотографии
        "counter_Not-found_precent": float, - Количество не распознанных лиц на фотографиях от общего числа фотографий
        "time_to_end": class=time, - Время выполнения скрипта
        "result": {
            "Path to image": "NOT FOUND",
            "Path to image": "True",     - Результирующий словарь
            "Path to image": "False",

        }
    """

    start_time = time.time()

    counter_true = 0
    counter_false = 0
    counter_not_found = 0

    img1 = face_recognition.load_image_file(img1_path)
    img1_encodings = face_recognition.face_encodings(img1)[0]

    intemediate_dict = {}
    result_dict = {}

    for i, image in enumerate(imgs_path, start=1):

        img2 = face_recognition.load_image_file(image)
        img2_encodings = face_recognition.face_encodings(img2)

        if len(img2_encodings) == 1:
            result = face_recognition.compare_faces([img1_encodings], img2_encodings[0])
            if True in result:
                counter_true += 1
            else:
                counter_false += 1
            intemediate_dict.setdefault(str(image), str(result[0]))
            if create_xlsx:
                add_info_to_book(name_sheets, image, i, str(result[0]))

        elif len(img2_encodings) > 1:
            result_list = []
            for img2_enc in img2_encodings:
                result = face_recognition.compare_faces([img1_encodings], img2_enc)
                result_list.append(result)

            if [True] in result_list:
                result = [True]
                if create_xlsx:
                    add_info_to_book(name_sheets, image, i, str(result[0]))
                counter_true += 1
                intemediate_dict.setdefault(str(image), str(result[0]))

            else:
                result = [False]
                if create_xlsx:
                    add_info_to_book(name_sheets, image, i, str(result[0]))
                counter_false += 1
                intemediate_dict.setdefault(str(image), str(result[0]))

        else:
            if create_xlsx:
                add_info_to_book(name_sheets, image, i, 'NOT FOUND')
            intemediate_dict.setdefault(str(image), 'NOT FOUND')
            counter_not_found += 1

    end_time = time.time() - start_time

    result_dict.setdefault('count_True', counter_true)
    result_dict.setdefault('counter_True_percent', percent(counter_true, len(imgs_path)))
    result_dict.setdefault('count_False', counter_false)
    result_dict.setdefault('counter_False_percent', percent(counter_false, len(imgs_path)))
    result_dict.setdefault('count_Not-found', counter_not_found)
    result_dict.setdefault('counter_Not-found_percent', percent(counter_not_found, len(imgs_path)))
    result_dict.setdefault('time_to_end', end_time)
    result_dict.setdefault('result', intemediate_dict)

    return result_dict


def main(create_xlsx=False) -> dict:
    """
    Функция выполняет роль скрипта, который запускает функцию compare_faces для каждого Персонажа указанного внутри
    функции.

    Если значение переменной create_xlsx=True, функция создает xlsx-документ "Result.xlsx".

    Так же, записывает json-файл с результирующим словарем.
    :param create_xlsx: bool
    :return: результирующий словарь
    """
    if create_xlsx:

        create_book()

    result_dict = {}

    image_base_path = 'base_face/placename.jpg'
    images_path = list(paths.list_images('placeman/assist'))

    placeman_assist = compare_faces(image_base_path, images_path, 'placeman_assist', create_xlsx=create_xlsx)

    result_dict[nameof(placeman_assist)] = placeman_assist

    images_path = list(paths.list_images('placeman/not_assist'))
    placeman_not_assist = compare_faces(image_base_path, images_path, 'placeman_not_assist', create_xlsx=create_xlsx)
    result_dict[nameof(placeman_not_assist)] = placeman_not_assist

    image_base_path = 'base_face/sportsman.jpg'
    images_path = list(paths.list_images('sportsman/assist'))

    sportsman_assist = compare_faces(image_base_path, images_path, 'sportsman_assist', create_xlsx=create_xlsx)
    result_dict[nameof(sportsman_assist)] = sportsman_assist

    images_path = list(paths.list_images('sportsman/not_assist'))
    sportsman_not_assist = compare_faces(image_base_path, images_path, 'sportsman_not_assist', create_xlsx=create_xlsx)
    result_dict[nameof(sportsman_not_assist)] = sportsman_not_assist

    image_base_path = 'base_face/blogger.jpg'
    images_path = list(paths.list_images('blogger/assist'))

    blogger_assist = compare_faces(image_base_path, images_path, 'blogger_assist', create_xlsx=create_xlsx)
    result_dict[nameof(blogger_assist)] = blogger_assist

    images_path = list(paths.list_images('blogger/not_assist'))
    blogger_not_assist = compare_faces(image_base_path, images_path, 'blogger_not_assist', create_xlsx=create_xlsx)
    result_dict[nameof(blogger_not_assist)] = blogger_not_assist

    with open('Result.json', 'w', encoding='utf8') as file:
        json.dump(result_dict, file, indent=4, ensure_ascii=False)

    return result_dict


if __name__ == "__main__":
    main()


