# we are going to use this class to map each images/sub_folder
# each folder and its files are a layer --> each layer is an object in here
import os
import random


class Layer:
    # our layer takes in itself, and the layer path from our generator
    def __init__(self, path):
        # we have two variables, path, and rarity (determines if layer exists)
        self.path = path
        # our rarity is 1 (100%) by default, but we also set them in our generator.py
        self.rarity = 1.0

    def get_rand(self):
        # get all of the images from the layer self.path
        image_files = os.listdir(self.path)
        # get a random image from all of the image_files above
        image_path = random.choice(image_files)
        # get the path of the image file with the layer path
        path = os.path.join(self.path, image_path)

        return path

# this funciton checks whether or not the layer should be genreated based on the rarity
    def check_gen(self):
        # returns a boolean, if it is true (i.e rarity is greater than random number)
        # --> that means we generate the layer, otherwise, we dont generate it
        return random.random() < self.rarity
