import gradio as gr
import function as f

iface = gr.Interface(
    fn=f.transcribe,
    inputs=gr.Audio(source="microphone", type="filepath", placeholder="Please start speaking..."),
    outputs=["video","text"],
    title="🐣Talk Buddy🐣",
    description="모든 설정을 마쳤다면 TalkBuddy와 대화를 해보세요!",
    theme=gr.themes.Soft()
)



with gr.Blocks(theme=gr.themes.Soft()) as iface1:
    with gr.Tab("캐릭터 목소리"):
        with gr.Tab("기본 목소리"):
            auth_message= "목소리를 선택하세요"
            choose_adam = gr.Button("Adam")
            choose_antoni = gr.Button("Antoni")
            choose_rachel = gr.Button("Rachel")
        with gr.Tab("목소리 생성"):
            auth_message= "목소리 mp3 파일을 업로드하세요."
            userMp3 = gr.Audio(type="filepath",source="upload",label="mp3", info="Filepath of video/image that contains faces to use")
            choose_create = gr.Button("생성 및 저장")
    choose_adam.click(f.adam)
    choose_antoni.click(f.antoni)
    choose_rachel.click(f.rachel)
    choose_create.click(f.clone_voice, inputs=userMp3)
    
    
    with gr.Tab("캐릭터 외모"):
        with gr.Tab("이미지 업로드"):
            image_input = gr.Image(type='pil',label="Video or Image", info="Filepath of video/image that contains faces to use")
            save_button1 = gr.Button("저장")
        with gr.Tab("이미지 생성"):
            text_input = gr.Textbox(label="생성할 이미지를 묘사하세요.")
            ai_output = gr.Image(type='pil')
            generate_button = gr.Button("생성")
            save_button2 = gr.Button("저장")
        

    save_button1.click(f.image_save, inputs=image_input)
    save_button2.click(f.image_save, inputs=ai_output)
    generate_button.click(f.get_image,inputs=text_input,outputs=ai_output)



tt = gr.TabbedInterface([iface,iface1],["talk","settings"])

tt.launch(auth = ('user','admin'), auth_message= "아이디와 비밀번호를 입력하세요.",share='True')
