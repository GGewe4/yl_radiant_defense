from PIL import Image

for x in range(18):
    add_str = str(x)
    if x < 10:
        add_str = "0" + add_str
    im = Image.open(f"data/enemies/minotaur/Walking/Minotaur_01_Walking_0" + add_str + ".png")
    im2 = im.crop((229, 57, 641, 452))
    im2.save(f"data/enemies/minotaur/Walking/Minotaur_01_Walking_0" + add_str + ".png")
