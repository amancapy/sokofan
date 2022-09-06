def scrape_xsbs():
    for i in range(1, 16):
        xsb = open(f"levelfiles/level{i}.xsb", "r").read().split(";")

        for levelchunk in xsb:
            if levelchunk:
                lsplit = levelchunk.split("\n\n")
                lname = lsplit[0][1:]
                level = lsplit[1]

                h = len(level.split("\n"))
                if h <= 26:
                    w = 0
                    for thing in level.split("\n"):
                        if thing:
                            if len(thing) > w:
                                w = len(thing)

                    newlevel = ""
                    for thing in level.split("\n"):
                        if thing:
                            thing += (w - len(thing)) * " "
                            newlevel += thing + "\n"

                    if w <= 26:
                        newfile = open(f"C:/Users/Aman/Desktop/Everything/CSD311/Sokoproject/xsbs/{i}/{lname}.xsb", "w")
                        newfile.write(newlevel)
                        newfile.close()

# scrape_xsbs()