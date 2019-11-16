def write_indivisuals(pop,filename,mode="a"):
    dt_now = datetime.datetime.now().strftime('%Y年%m月%d日%H:%M:%S')
    with open(path + filename, mode=mode) as f:
        f.write("{}${}".format(dt_now,str(pop)))
        f.write("\n")
