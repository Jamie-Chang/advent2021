from part1 import load, next_image, read


if __name__ == "__main__":
    algorithm, image = load(read())
    for _ in range(50):
        image = next_image(algorithm, image)

    print(image.count)
