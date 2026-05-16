"""CLI: regenerate the synthetic dataset and retrain every cost pipeline."""

from ml.data_generator import generate_dataset
from ml.trainer import train_models


def main() -> None:
    generate_dataset()
    train_models()


if __name__ == "__main__":
    main()
