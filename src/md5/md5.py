import hashlib


def get_fmd5(fpath):
    hash_md5 = hashlib.md5()
    with open(fpath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_fsha1(fpath):
    hash_sha1 = hashlib.sha1()
    with open(fpath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()


def md5(s):
    return hashlib.md5(s.encode(encoding="UTF-8", errors="ignore")).hexdigest()


def sha1(s):
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()
