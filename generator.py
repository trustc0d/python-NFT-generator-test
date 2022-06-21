# this is the actual file that generates the nft's
import os
import random
from datetime import datetime
from PIL import Image
from layer import Layer


class Generator:
    # the constructor for the file, what we do on class call
    # takes in self, and a path for the images
    def __init__(self, images_path):
        # set the directory for all of the nft's we create
        # this is the output folder / the current batch timestampped
        self.output_path = f"./output/{datetime.now()}"
        # set the layers using the load_layers funciton passing in the images path
        self.layers = self.load_layers(images_path)

        # set the chance of getting a rare background
        self.rare_bg_chance = 0.05
        # set the background colors for each normal, and rare nft we render
        self.bg_color = (120, 150, 180)
        self.rare_bg_color = (225, 225, 150)

        # first, create the output folder for the nfts, if it already exists, dont crash
        # takes in the output directory name, and we give it the flag exist_ok = true
        os.makedirs(self.output_path, exist_ok=True)

    # our function for generating nfts, takes in "n" for the number of nft's to create
    # we declared layers in self using the above funciton, so can access them here using self.layers
    def gen_nft(self, n=1):
        # output a message
        print("Creating nft(s). Please wait...")

        # generate n number of nft's
        for i in range(n):
            # set the random image paths for the nft parts using the function below
            img_path_seq = self.gen_img_seq()
            # call the funciton to render the image, passing in our img_path_seq
            image = self.render_img(img_path_seq)

            # save the generated image to our output folder
            self.save_img(image, i)

        # output success message when done
        print("\nSuccess!")

    # the function for loading our image layers form image path
    def load_layers(self, images_path):
        # all of our image path layers
        layers = []

        # get all of the sub paths, and return them sorted
        sub_paths = sorted(os.listdir(images_path))

        # loop over the sub_paths list
        for sub_path in sub_paths:
            # first, get the absolute path by joining image path and sub path
            layer_path = os.path.join(images_path, sub_path)
            # then, create a new layer object, passing in that path
            layer = Layer(layer_path)
            # finally, add that layer to our layers array
            layers.append(layer)

        # set the rarities for each layer
        layers[0].rarity = 1
        layers[1].rarity = 1
        layers[2].rarity = 0.8
        layers[3].rarity = 0.15

        return layers

    # function for getting the random paths of the images for each part of the nft
    def gen_img_seq(self):
        # an array for our the paths for each part of our nft (each image path)
        img_path_seq = []

        # loop over each layer
        for layer in self.layers:
            # first, use the check_gen function to see if layer should be generated
            # --> checks rarity level to determine if so
            # so, if the check_gen function returns true, add the layer to the sequence
            if layer.check_gen():
                # call the funciton in class to get a random image from the layer
                image_path = layer.get_rand()
                # append the image path of the nft part to the sequence array
                img_path_seq.append(image_path)

        return img_path_seq

    # the function to actually return the image using the image path sequence we generated
    def render_img(self, img_path_seq):
        # first, we have to create a blank image

        # the first step is to decide what the background color is
        # if the random number is < chance, then the bg_color is the rare one
        # -->  otherwise, it is the normal one
        bg_color = self.rare_bg_color if (
            random.random() < self.rare_bg_chance) else self.bg_color

        # takes in our colours, the image size, and the image background
        # --> we pass in (red, green, blue, tranpsarent), (24px * 24px), (self.bg_color)
        image = Image.new("RGBA", (24, 24), bg_color)

        # loop over the img_path_seq, so we can add each image from path onto the background
        for img_path in img_path_seq:
            # open the image from the path at the looped indice
            layer_img = Image.open(img_path)
            # add the layer_img onto our current img
            image = Image.alpha_composite(image, layer_img)

        return image

    # the function to save our image to our output folder
    def save_img(self, image, i):
        # create a padded index (0000i), which will allow help avoid index
        index = str(i).zfill(5)
        # our image name is nft_(index).png
        img_name = f"nft_{i}.png"
        # save our image to the path of self.output_path/img_name
        image.save(os.path.join(self.output_path, img_name))
