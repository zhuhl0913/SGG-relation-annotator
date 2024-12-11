import gradio as gr
import json
from PIL import Image

# 读取 JSON 文件并缓存数据
def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# 保存选择的结果
def save_result(file_path, subject, obj, predicate, index, selected_options):
    result = {
        'index': index,
        'subject': subject,  # 保存 subject
        'object': obj,  # 保存 object
        'predicate': predicate,  # 保存 predicate
        'selected_options': selected_options  # 保存选择的选项
    }
    with open(file_path, 'a') as f:  # 以追加的方式保存结果
        f.write(json.dumps(result, indent=4) + '\n')

# Gradio 应用函数
def gradio_interface(json_file_path):
    # 读取数据并缓存
    data = read_json(json_file_path)
    current_index = 0  # 当前显示的图片的索引

    # 显示当前索引的图片和选项
    def get_current_item(index):
        item = data[index]
        image = item['image_path']  # 返回图片路径
        
        subject = item['subject']  # 获取 subject
        obj = item['object']  # 获取 object

        options = item['options']
        level_2_options = options.get("level_2", {})
        level_3_options = options.get("level_3", {})
        return image, subject, obj, level_2_options, level_3_options

    # 获取当前项
    image_path, subject, obj, level_2_options, level_3_options = get_current_item(current_index)

    # 更新第三级选项（根据第二级选择）
    def update_level_3(level_2_choice):
        return gr.Dropdown(choices=level_3_options.get(level_2_choice, []))  # 返回新的 Dropdown 对象

    # 保存当前选择的结果并返回
    def handle_save(selected_level_2, selected_level_3, coordinates=None):
        # 生成 predicate（你可以根据需要更改生成逻辑）
        predicate = f"{selected_level_2}-{selected_level_3}"  # 这是一个示例，你可以按需修改生成逻辑
        save_result('output.json', subject, obj, predicate, current_index, {'level_2': selected_level_2, 'level_3': selected_level_3})
        return f"Saved: Subject - {subject}, Object - {obj}, Predicate - {predicate}"

    # 翻到下一个数据
    def handle_next(selected_level_2, selected_level_3, coordinates=None):
        nonlocal current_index
        # 保存当前结果
        # predicate = f"{selected_level_2}-{selected_level_3}"
        # save_result('output.json', subject, obj, predicate, current_index, {'level_2': selected_level_2, 'level_3': selected_level_3})
        
        # 更新到下一个
        current_index = (current_index + 1) % len(data)
        image_path, subject, obj, level_2_options, level_3_options = get_current_item(current_index)
        
        # 更新图像（返回多个图像）
        return (
            gr.Image.update(value=image_path),  # 更新原始图片
            gr.Dropdown.update(choices=level_2_options),  # 更新第二级选项
            gr.Dropdown.update(choices=[]),  # 重置第三级选项
            f"Now displaying: {current_index + 1}/{len(data)}",
            f"Subject: {subject}, Object: {obj}"  # 更新显示当前的subject和object
        )

    # 返回上一个数据
    def handle_previous(selected_level_2, selected_level_3, coordinates=None):
        nonlocal current_index
        # 保存当前结果
        # predicate = f"{selected_level_2}-{selected_level_3}"
        # save_result('output.json', subject, obj, predicate, current_index, {'level_2': selected_level_2, 'level_3': selected_level_3})
        
        # 更新到上一个
        current_index = (current_index - 1) % len(data)
        image_path, subject, obj, level_2_options, level_3_options = get_current_item(current_index)
        
        # 更新图像（返回多个图像）
        return (
            gr.Image.update(value=image_path),  # 更新原始图片
            gr.Dropdown.update(choices=level_2_options),  # 更新第二级选项
            gr.Dropdown.update(choices=[]),  # 重置第三级选项
            f"Now displaying: {current_index + 1}/{len(data)}",
            f"Subject: {subject}, Object: {obj}"  # 更新显示当前的subject和object
        )

    # 创建 Gradio 界面
    with gr.Blocks() as blocks:
        with gr.Row():
            save_button = gr.Button("Save Selection")
            next_button = gr.Button("Next Item")
            prev_button = gr.Button("Previous Item")  # 添加上一项按钮
        output = gr.Textbox(value=f"Subject: {subject}, Object: {obj}", interactive=False)  # 初始化显示 Subject 和 Object

        # 动态更新组件
        img_output = gr.Image(value=image_path)
        
        level_2_dropdown = gr.Dropdown(choices=level_2_options, label="Select Level 2")
        level_3_dropdown = gr.Dropdown(choices=[], label="Select Level 3")  # 初始为空

        # 更新第三级选项
        level_2_dropdown.change(
            fn=update_level_3,
            inputs=level_2_dropdown,
            outputs=level_3_dropdown  # 动态更新三级下拉框
        )

        # 下一项按钮处理
        next_button.click(
            fn=handle_next,
            inputs=[level_2_dropdown, level_3_dropdown, output],
            outputs=[img_output, level_2_dropdown, level_3_dropdown, output, output]
        )

        # 上一项按钮处理
        prev_button.click(
            fn=handle_previous,
            inputs=[level_2_dropdown, level_3_dropdown, output],
            outputs=[img_output, level_2_dropdown, level_3_dropdown, output, output]
        )

        # 保存按钮处理
        save_button.click(
            fn=handle_save,
            inputs=[level_2_dropdown, level_3_dropdown, output],
            outputs=output
        )

    return blocks


# 启动 Gradio 应用
if __name__ == '__main__':
    gradio_interface('generated_sample.json').launch(share=True)
