import gradio as gr
import json
from PIL import Image

# 读取 JSON 文件并缓存数据
def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# 保存选择的结果
def save_result(file_path, selected_options, index, coordinates=None):
    result = {
        'index': index,
        'selected_options': selected_options,
        'coordinates': coordinates  # 添加坐标信息
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
        mask = item['mask_path']
        sam = item['SAM_path']
        
        options = item['options']
        level_1_options = options.get("level_1", [])
        level_2_options = options.get("level_2", {})
        level_3_options = options.get("level_3", {})
        return image, mask, sam, level_1_options, level_2_options, level_3_options

    # 初始化数据
    image_path, mask_path, sam_path, level_1_options, level_2_options, level_3_options = get_current_item(current_index)

    # 更新第二级选项（根据第一级选择）
    def update_level_2(level_1_choice):
        if level_1_choice in level_2_options:
            return gr.Dropdown.update(choices=level_2_options[level_1_choice])
        else:
            return gr.Dropdown.update(choices=[])

    # 更新第三级选项（根据第二级选择）
    def update_level_3(level_2_choice):
        if level_2_choice in level_3_options:
            return gr.Dropdown.update(choices=level_3_options[level_2_choice])
        else:
            return gr.Dropdown.update(choices=[])

    # 保存当前选择的结果并返回
    def handle_save(selected_level_1, selected_level_2, selected_level_3, coordinates=None):
        save_result('output.json', {'level_1': selected_level_1, 'level_2': selected_level_2, 'level_3': selected_level_3}, current_index, coordinates)
        return f"Saved options: Level 1 - {selected_level_1}, Level 2 - {selected_level_2}, Level 3 - {selected_level_3}, Coordinates - {coordinates}"

    # 翻到下一个数据
    def handle_next(selected_level_1, selected_level_2, selected_level_3, coordinates=None):
        nonlocal current_index
        # 保存当前结果
        save_result('output.json', {'level_1': selected_level_1, 'level_2': selected_level_2, 'level_3': selected_level_3}, current_index, coordinates)
        # 更新到下一个
        current_index = (current_index + 1) % len(data)
        image_path, mask_path, sam_path, level_1_options, level_2_options, level_3_options = get_current_item(current_index)
        
        # 更新图像
        return (
            gr.Image.update(value=image_path),  # 更新原始图片
            # gr.Image.update(value=mask_path),   # 更新纯掩码图片
            # gr.Image.update(value=sam_path),    # 更新掩码图像
            gr.Dropdown.update(choices=level_1_options),  # 更新第一级选项
            gr.Dropdown.update(choices=[]),  # 重置第二级选项
            gr.Dropdown.update(choices=[]),  # 重置第三级选项
            f"Now displaying: {current_index + 1}/{len(data)}"
        )


    # 捕获点击坐标并显示
    def capture_coordinates(evt: gr.SelectData):
        # 获取鼠标点击坐标
        x, y = evt._data['index']
        data
        return f"Clicked at (x={x}, y={y})"

    # 创建 Gradio 界面
    with gr.Blocks() as blocks:
        with gr.Row():
            save_button = gr.Button("Save Selection")
            next_button = gr.Button("Next Item")
        output = gr.Textbox()

        # 动态更新组件
        with gr.Row():
            img_output = gr.Image(label="Image to be annotated", value=image_path, interactive=True, scale=2)
            img_output2 = gr.Image(label="Pure Mask", value=mask_path)
            img_output3 = gr.Image(label="Masked Image", value=sam_path)
        level_1_dropdown = gr.Dropdown(choices=level_1_options, label="Select Level 1")
        level_2_dropdown = gr.Dropdown(choices=[], label="Select Level 2")  # 初始为空
        level_3_dropdown = gr.Dropdown(choices=[], label="Select Level 3")  # 初始为空

        # 更新第二级选项
        level_1_dropdown.change(
            fn=update_level_2,
            inputs=level_1_dropdown,
            outputs=level_2_dropdown  # 动态更新二级下拉框
        )

        # 更新第三级选项
        level_2_dropdown.change(
            fn=update_level_3,
            inputs=level_2_dropdown,
            outputs=level_3_dropdown  # 动态更新三级下拉框
        )

        # 下一项按钮处理
        next_button.click(
            fn=handle_next,
            inputs=[level_1_dropdown, level_2_dropdown, level_3_dropdown, output],
            outputs=[img_output, level_1_dropdown, level_2_dropdown, level_3_dropdown, output]
        )

        # 保存按钮处理
        save_button.click(
            fn=handle_save,
            inputs=[level_1_dropdown, level_2_dropdown, level_3_dropdown, output],
            outputs=output
        )

        # 捕获鼠标点击坐标并显示
        img_output.select(
            fn=capture_coordinates,
            inputs=[],  # 不需要传递图像数据
            # outputs=[output, output]  # 输出到文本框
            outputs = output
        )

    return blocks


# 启动 Gradio 应用
if __name__ == '__main__':
    gradio_interface('sample.json').launch(share=True)
