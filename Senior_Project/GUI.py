import tkinter
import tkinter.messagebox
#from tkVideoPlayer import TkinterVideo
import customtkinter
import os
from PIL import Image
import AI_generator as gen
from pathlib import Path

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# 0 or 1 for FX: Noise, Implode, Sepia Tone, Sketch, Solarize, Stereogram, Swirl, Wave, Spread

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Setting up variables
        self.display_num = 1

        # Setting up paths
        self.text_path = Path('./generated_text.txt')

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1, 2, 3), weight=0)
        self.grid_columnconfigure((4), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=8,sticky="nsew")
        #self.sidebar_frame.grid_rowconfigure(3, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="AI Generated Art", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="API Key", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create promptBox
        self.promptBox_label = customtkinter.CTkLabel(self, text="Text AI", anchor="w")
        self.promptBox_label.grid(row=0, column=1)
        self.promptBox = customtkinter.CTkTextbox(self)
        self.promptBox.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.prompt_input_button = customtkinter.CTkButton(self, text="Run", command=self.generate_text)
        self.prompt_input_button.grid(row=2, column=1, padx=20, pady=(10, 10))


        # create resultBox
        self.resultBox_label = customtkinter.CTkLabel(self, text="Image AI", anchor="w")
        self.resultBox_label.grid(row=0, column=2)
        self.resultBox = customtkinter.CTkTextbox(self)
        self.resultBox.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.result_input_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.result_input_frame.grid(row=2, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.result_input_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.result_input_frame.grid_rowconfigure((0), weight=1)

        self.left_result_button = customtkinter.CTkButton(self.result_input_frame, text="<--", command=self.prev_image)
        self.left_result_button.grid(row=0, column=0, pady=(10, 10))
        self.result_input_button = customtkinter.CTkButton(self.result_input_frame, text="Generate", command=self.generate_images)
        self.result_input_button.grid(row=0, column=1, pady=(10, 10))
        self.right_result_button = customtkinter.CTkButton(self.result_input_frame, text="-->", command=self.next_image)
        self.right_result_button.grid(row=0, column=2, pady=(10, 10))

        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

        # create images frame
        self.images_frame_label = customtkinter.CTkLabel(self, text="Images", anchor="w")
        self.images_frame_label.grid(row=0, column=3)

        self.image_input_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.image_input_frame.grid(row=2, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.image_input_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.image_input_frame.grid_rowconfigure((0), weight=1)

        self.left_image_button = customtkinter.CTkButton(self.image_input_frame, text="<--", command=self.prev_image)
        self.left_image_button.grid(row=0, column=0, pady=(10, 10))
        self.image_input_button = customtkinter.CTkButton(self.image_input_frame, text="Variation", command=self.generate_variation)
        self.image_input_button.grid(row=0, column=1, pady=(10, 10))
        self.right_image_button = customtkinter.CTkButton(self.image_input_frame, text="-->", command=self.next_image)
        self.right_image_button.grid(row=0, column=2, pady=(10, 10))

        # create songBox
        self.songBox_label = customtkinter.CTkLabel(self, text="Song AI", anchor="w")
        self.songBox_label.grid(row=3, column=1)
        self.songBox = customtkinter.CTkTextbox(self)
        self.songBox.grid(row=4, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.song_input_button = customtkinter.CTkButton(self, text="Generate", command=self.get_prompt)
        self.song_input_button.grid(row=5, column=1, padx=20, pady=(10, 10))

        # create extensionButton frame
        self.extensionButton_frame = customtkinter.CTkFrame(self)
        self.extensionButton_frame.grid(row=4, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.extension_var = tkinter.IntVar(value=0)
        self.label_extension_group = customtkinter.CTkLabel(self, text="Generated Clips")
        self.label_extension_group.grid(row=3, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.extension_button_1 = customtkinter.CTkRadioButton(master=self.extensionButton_frame, text="Clip 1", variable=self.extension_var, value=0)
        self.extension_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.extension_button_2 = customtkinter.CTkRadioButton(master=self.extensionButton_frame, text="Clip 2", variable=self.extension_var, value=1)
        self.extension_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.extension_button_3 = customtkinter.CTkRadioButton(master=self.extensionButton_frame, text="Clip 3", variable=self.extension_var, value=2)
        self.extension_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        self.extend_input_button = customtkinter.CTkButton(self, text="Extend", command=self.get_prompt)
        self.extend_input_button.grid(row=5, column=2, padx=20, pady=(10, 10))

        # create upscaleButton frame
        self.upscaleButton_frame = customtkinter.CTkFrame(self)
        self.upscaleButton_frame.grid(row=4, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.upscale_var = tkinter.IntVar(value=0)
        self.label_upscale_group = customtkinter.CTkLabel(self, text="Extended Songs")
        self.label_upscale_group.grid(row=3, column=3, columnspan=1, padx=10, pady=10, sticky="")
        self.upscale_button_1 = customtkinter.CTkRadioButton(master=self.upscaleButton_frame, text="Song 1", variable=self.upscale_var, value=0)
        self.upscale_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.upscale_button_2 = customtkinter.CTkRadioButton(master=self.upscaleButton_frame, text="Song 2", variable=self.upscale_var, value=1)
        self.upscale_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.upscale_button_3 = customtkinter.CTkRadioButton(master=self.upscaleButton_frame, text="Song 3", variable=self.upscale_var, value=2)
        self.upscale_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")
        
        self.upscale_input_button = customtkinter.CTkButton(self, text="Upscale", command=self.get_prompt)
        self.upscale_input_button.grid(row=5, column=3, padx=20, pady=(10, 10))

        # create video AI frame
        self.video_frame_label = customtkinter.CTkLabel(self, text="Video AI", anchor="w")
        self.video_frame_label.grid(row=0, column=4)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="SpecialFX")
        self.scrollable_frame.grid(row=1, column=4, padx=(20,0), pady=(20,0), sticky="nsew")
        self.scrollable_frame.grid_rowconfigure(4, weight=1)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        # 0 or 1 for FX: Noise, Implode, Sepia Tone, Solarize, Stereogram, Swirl, Wave, Spread
        self.specialFX = []
        self.list = []
        blend = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Blend")
        blend.grid(row=0, column=0, padx=10, pady=(0,20))
        self.specialFX.append(blend)
        noise = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Noise")
        noise.grid(row=1, column=0, padx=10, pady=(0,20))
        self.specialFX.append(noise)
        implode = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Implode")
        implode.grid(row=2, column=0, padx=10, pady=(0,20))
        self.specialFX.append(implode)
        sepiaTone = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Sepia Tone")
        sepiaTone.grid(row=3, column=0, padx=10, pady=(0,20))
        self.specialFX.append(sepiaTone)
        solarize = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Solarize")
        solarize.grid(row=4, column=0, padx=10, pady=(0,20))
        self.specialFX.append(solarize)
        swirl = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Swirl")
        swirl.grid(row=5, column=0, padx=10, pady=(0,20))
        self.specialFX.append(swirl)
        wave = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Wave")
        wave.grid(row=6, column=0, padx=10, pady=(0,20))
        self.specialFX.append(wave)
        spread = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Spread")
        spread.grid(row=7, column=0, padx=10, pady=(0,20))
        self.specialFX.append(spread)



        self.merge_video_button = customtkinter.CTkButton(self, text="Merge", command=self.generate_video)
        self.merge_video_button.grid(row=5, column=4, padx=20, pady=(10, 10))

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")   
        self.promptBox.insert("0.0", "Generate me text prompts for Dall E image model.")     #Input Box Prompt
        self.songBox.insert("0.0", "WAV: \nArtist: \nGenre: \nPrompt Length: \nInitial Song Length: \nTotal Song Length: \nLyrics: ")     #Song Box Prompt
        self.specialFX[0].select()



    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
    
    def generate_text(self):
        self.resultBox.delete("0.0", "1000.0")
        prompt = self.promptBox.get("0.0","1000.0")
        gen.prompt = prompt
        done = gen.generate_text()
        if(done):
            with open(self.text_path) as f:
                lines = f.read()
                str_lines = str(lines)
                str_lines = str_lines.replace("'", "")
                str_lines = str_lines.replace("[", "")
                str_lines = str_lines.replace("]", "")
                str_lines = str_lines.replace(",", "")
                self.resultBox.insert("0.0", str_lines)

    def generate_images(self):
        self.display_num = 1
        gen_true = gen.generate_images()
        if(gen_true):
            # load images with light and dark mode image
            self.display_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "image{}.jpg".format(self.display_num))), size=(500, 500))

            self.image_frame = customtkinter.CTkLabel(self, text="", image=self.display_image)
            self.image_frame.grid(row=1, column=3, padx=20, pady=10)
        
    def generate_variation(self):
        gen.generate_variation("image{}.jpg".format(self.display_num))

    def generate_video(self):
        for i in range(len(self.specialFX)):
            self.list.append(self.specialFX[i].get())
        gen_true = gen.generate_video(self.upscale_var.get(), self.list)
        if(False):
            self.video_frame = customtkinter.CTkLabel(self, text="")
            self.video_frame.grid(row=3, column=4, padx=20, pady=10)

            videoplayer = TkinterVideo(master=self.video_frame)
            videoplayer.load(r"final_video.mp4")
            videoplayer.play()

    def next_image(self):
        if(self.display_num < len([entry for entry in os.listdir(self.image_path) if os.path.isfile(os.path.join(self.image_path, entry))])):
            self.display_num += 1
        self.display_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "image{}.jpg".format(self.display_num))), size=(500, 500))

        self.image_frame = customtkinter.CTkLabel(self, text="", image=self.display_image)
        self.image_frame.grid(row=1, column=3, padx=20, pady=10)

    def prev_image(self):
        if(self.display_num >= 2):
            self.display_num -= 1
        self.display_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "image{}.jpg".format(self.display_num))), size=(500, 500))

        self.image_frame = customtkinter.CTkLabel(self, text="", image=self.display_image)
        self.image_frame.grid(row=1, column=3, padx=20, pady=10)

    def get_prompt(self):
        return


if __name__ == "__main__":
    app = App()
    app.mainloop()
