import ffmpeg, os

course_name = input("Introduce el nombre del curso: ")
path = os.getcwd()
os.mkdir(path + f"/{course_name}")

with open("enlaces.txt", "r") as enlaces:
    counter = 1
    for url in enlaces.readlines():
        stream = ffmpeg.input(url.replace('\n', ''))
        dofirst = ffmpeg.output(stream, f"./{course_name}/video - {counter}.mp4", **{'bsf:a': 'aac_adtstoasc'})
        ffmpeg.run(dofirst)
        counter += 1