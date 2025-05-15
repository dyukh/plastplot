import numpy as np

def read_data_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Обработка заголовка
    header = []
    for i in range(5):
        line = lines[i].split('!')[0].strip()  # Игнорируем комментарии
        header.append(line)

    # Извлечение параметров из заголовка
    model_number = int(header[3].strip())
    radius_points, angle_points = map(int, header[4].split())
    N = radius_points
    K = angle_points

    # Пропускаем первые 5 строк
    data_lines = lines[5:]

    blocks = []
    current_line = 0

    for _ in range(model_number):
        if current_line >= len(data_lines):
            break

        # Чтение первой строки блока (толщина и идентификатор)
        first_line = data_lines[current_line].split('!')[0].strip()
        parts = first_line.split()
        thickness = float(parts[0])
        identifier = ' '.join(parts[1:]) if len(parts) > 1 else ''
        current_line += 1

        # Чтение углов (вторая строка блока)
        angles_line = data_lines[current_line].split('!')[0].strip()
        angles = list(map(float, angles_line.split()))
        current_line += 1

        # Чтение данных (N строк по K+1 столбцу)
        data = []
        for _ in range(N):
            if current_line >= len(data_lines):
                break
            data_line = data_lines[current_line].split('!')[0].strip()
            row_data = list(map(float, data_line.split()))
            data.append(row_data)
            current_line += 1

        # Преобразование данных в numpy массив для удобства
        data_array = np.array(data)
        blocks.append({
            'thickness': thickness,
            'identifier': identifier,
            'angles': angles,
            'data': data_array
        })

    return {
        'header': header,
        'model_number': model_number,
        'radius_points': radius_points,
        'angle_points': angle_points,
        'blocks': blocks
    }

# Пример использования
file_path = 'data/Pl2_res_vik2.txt'
data = read_data_file(file_path)

# Вывод информации о данных для проверки
print(f"Количество блоков: {data['model_number']}")
print(f"Количество точек по радиусу: {data['radius_points']}")
print(f"Количество точек по углу: {data['angle_points']}")
for i, block in enumerate(data['blocks']):
    print(f"\nБлок {i + 1}:")
    print(f"  Толщина: {block['thickness']}")
    print(f"  Идентификатор: {block['identifier']}")
    print(f"  Углы: {block['angles']}")
    print(f"  Данные (размер): {block['data'].shape}")