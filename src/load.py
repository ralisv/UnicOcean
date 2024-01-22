from objects.config import FishConfig
from objects.fish import FISHES, FISHES_DIRECTORY, FishInfo
from objects.skin import MIRROR, MIRROR_PATH, load_skin


def load_objects() -> None:
    """Loads all objects from the objects directory, should be called before Ocean is instantiated"""
    load_fishes()


def load_fishes() -> None:
    """Loads all fishes"""
    global FISHES, FISHES_DIRECTORY

    for fish_dir in FISHES_DIRECTORY.iterdir():
        if not fish_dir.is_dir():
            continue
        config_file = fish_dir / "config.json"
        if not config_file.exists():
            continue
        config = FishConfig.parse_file(config_file)
        left, right = load_skin(fish_dir / "skin.txt", config.colors)
        FISHES[fish_dir.name] = FishInfo(
            name=fish_dir.name,
            skin_left=left,
            skin_right=right,
            min_speed=config.min_speed,
            max_speed=config.max_speed,
            carnivorous=config.carnivorous,
            rarity=config.rarity,
            colors=config.colors,
        )


def load_mirror() -> None:
    """Loads the mirroring characters from the assets/mirror.txt file"""
    global MIRROR

    with open(MIRROR_PATH) as mirror_file:
        for line in mirror_file:
            fst, snd = tuple(line[:2])

            MIRROR[fst] = snd
