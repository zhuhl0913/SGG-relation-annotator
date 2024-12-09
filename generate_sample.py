import os
import json

# 默认的 options 结构（你可以根据需要修改）
default_options = {
    "level_1": ["A", "B", "C", "D"],
    "level_2": {
        "A": ["1", "2"],
        "B": ["3", "4"],
        "C": ["5", "6"],
        "D": ["7", "8"]
    },
    "level_3": {
        "1": ["a", "b"],
        "2": ["c", "d"],
        "3": ["e", "f"],
        "4": ["h", "i"],
        "5": ["j", "k"],
        "6": ["l", "m"],
        "7": ["n", "o"],
        "8": ["p", "q"]
    }
}

# 批量生成 sample.json
def generate_sample_json(image_folder, output_json_path):
    # 获取文件夹中的所有图片文件
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

    # 为每个图片生成一个元素
    sample_data = []
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)  # 获取图片的完整路径
        item = {
            "image_path": image_path,
            "options": default_options
        }
        sample_data.append(item)
    
    # 将生成的列表写入 output.json 文件
    with open(output_json_path, 'w') as json_file:
        json.dump(sample_data, json_file, indent=4)
    
    print(f"sample.json has been generated with {len(sample_data)} images.")

# 使用示例
if __name__ == "__main__":
    # 图片文件夹路径
    image_folder = 'sample_folder'
    
    # 输出的 JSON 文件路径
    output_json_path = 'generated_sample.json'
    
    # 调用函数生成 sample.json
    generate_sample_json(image_folder, output_json_path)
