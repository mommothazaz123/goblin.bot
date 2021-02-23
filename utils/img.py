import pathlib


def crop_to_face(sprite_path, actor, out_path='cache/img/faces'):
    """
    Crops the image at ``sprite_path`` to the face specified in ``actor``. If ``out_path`` is provided, caches based
    on path.

    Returns the path of the cropped image.

    :type sprite_path: str or os.PathLike
    :type actor: goblin.actor.Actor
    :type out_path: str or os.PathLike
    """
    src_path = pathlib.PurePath(sprite_path)
    src_filename = src_path.name
    dest_path = pathlib.Path(out_path, src_filename)
    if dest_path.is_file():
        return str(dest_path)

    if not hasattr(actor, 'face'):
        return sprite_path

    # todo
    return sprite_path
