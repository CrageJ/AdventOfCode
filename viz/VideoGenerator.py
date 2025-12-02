from pathlib import Path
import shutil
from collections import defaultdict
from PIL import Image
import utils
import numpy as np
import vizUtils


class VideoGenerator:
    def __init__(self, name, colour_scheme=None, output_folder="gifs"):
        """
        Parameters
        :param name: name of the video
        :param colour_scheme: dictionary which sets a numerical value to RGB value e.g 0: (0,100,255)
        :param output_folder: folder to output video
        :param frame_folder: temporary folder to store frames
        """
        self.name = name

        self.colour_scheme = defaultdict(lambda:vizUtils.DEFAULT_COLOUR)
        if colour_scheme:
            for k,v in colour_scheme.items():
                self.colour_scheme[k] = v

        self.root_folder = utils.get_root_folder()
        self.output_folder = self.root_folder / output_folder
        self.frames = []


        self.output_folder.mkdir(parents=True, exist_ok=True)

        self.frame_count = 0


    @staticmethod
    def clear_folder(folder_path, delete_folder=False):
        if not folder_path.exists():
            return  # Nothing to clear

        if delete_folder:
            # Remove the entire folder safely
            shutil.rmtree(folder_path)
            return

        # Otherwise, delete all contents but keep the folder
        for item in folder_path.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

    def add_frame(self,array):
        array = [[self.colour_scheme[cell] for cell in row] for row in array]
        array = np.array(array)
        # Convert to numpy array (ensure dtype = uint8)
        array = np.array(array, dtype=np.uint8)

        # Create an image (expects H×W×3 for RGB)
        img = Image.fromarray(array, mode="RGB")
        self.frames.append(img)

    def render_gif(self,millis=100): # secs per frame
        self.frames[0].save(
            self.output_folder/f"{self.name}.gif",
            save_all=True,
            append_images=self.frames[1:],
            duration=millis,
            loop=0,
        )