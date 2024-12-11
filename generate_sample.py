import os
import json

# 默认的 options 结构（你可以根据需要修改）
default_options = {
    "level_2": ["wearing", "has"],  # 固定的 level_2 内容
    "level_3": {
        "wearing": ["wearing",
    "wearing all",
    "wearing pair of",
    "wearing same",
    "wearing striped"],
        "has": ["has"]
    }
}

# 提取文件名中的 pair_name，并拆分为 subject 和 object
def extract_subject_object(pair_name):
    # 假设pair_name是由下划线分隔的两个部分，例如 box_donut
    parts = pair_name.split('_')
    subject = parts[0]  # 第一部分是 subject
    obj = parts[1]  # 第二部分是 object
    return subject, obj

# 提取文件名中的 pair_name
def extract_pair_name(filename):
    # 移除文件扩展名
    base_name = os.path.splitext(filename)[0]
    
    # 分割文件名
    parts = base_name.split('_')
    
    # 假设文件名格式是：image_{image_id}_pair_{pair_id}_{pair_name}
    pair_name = "_".join(parts[4:])  # 从第四个部分开始拼接后面的部分
    
    return pair_name

# 批量生成 sample.json
def generate_sample_json(image_folder, output_json_path):
    # 获取文件夹中的所有图片文件
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

    # 为每个图片生成一个元素
    sample_data = []
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)  # 获取图片的完整路径
        pair_name = extract_pair_name(image_file)  # 提取pair name
        subject, obj = extract_subject_object(pair_name)  # 拆分成subject和object
        
        item = {
            "image_path": image_path,
            "options": default_options,
            "subject": subject,  # 添加subject
            "object": obj  # 添加object
        }
        sample_data.append(item)
    
    # 将生成的列表写入 output.json 文件
    with open(output_json_path, 'w') as json_file:
        json.dump(sample_data, json_file, indent=4)
    
    print(f"sample.json has been generated with {len(sample_data)} images.")

# 使用示例
if __name__ == "__main__":
    # 图片文件夹路径
    image_folder = 'output_images_2'
    
    # 输出的 JSON 文件路径
    output_json_path = 'generated_sample.json'
    
    # 调用函数生成 sample.json
    generate_sample_json(image_folder, output_json_path)

