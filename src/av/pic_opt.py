import exifread


# 输入：文件名(filename)
# 输出：文件的拍摄时间:20181207_031034
# 失败: 空
def get_pic_time(fileabspath):
    timeFomrt = ""
    try:
        FIELD = "EXIF DateTimeOriginal"
        fd = open(fileabspath, "rb")
        tags = exifread.process_file(fd)
        if FIELD in tags:
            time = str(tags[FIELD])  # 获取到的结果格式类似为：2018:12:07 03:10:34
            timeFomrt = time.replace(":", "").replace(" ", "_")  # 获取结果格式类似为：20181207_031034
    except KeyError as e:
        print("error", fileabspath, e)
    finally:
        if fd:
            fd.close()

    # 显示图片所有的exif信息
    # print("showing res of getExif: \n")
    # print(tags)
    return timeFomrt
