# our main script for generating the avatars, imports our generator class
from generator import Generator


def gen():
    # first, create a new instance of our generator class
    generator = Generator("./images")
    # then, call the generate nft function, takes in a number
    # --> this is the number of nft's to generate
    generator.gen_nft(1000)


# if the user ran this file directly, run the generate function
# like in java when it runs main, this is the main function
if __name__ == "__main__":
    gen()
