from datasets import load_dataset


def inspect_dataset():
    print("Loading PlantVillage dataset...")

    dataset = load_dataset(
        "mohanty/PlantVillage",
        "default"
    )

    print("\nDataset:")
    print(dataset)

    print("\nTrain:")
    print(dataset["train"])

    print("\nTest:")
    print(dataset["test"])

    print("\nFeatures:")
    print(dataset["train"].features)

    print("\nNumber of training images:")
    print(len(dataset["train"]))

    print("\nNumber of test images:")
    print(len(dataset["test"]))

    print("\nExample:")
    print(dataset["train"][0])


if __name__ == "__main__":
    inspect_dataset()