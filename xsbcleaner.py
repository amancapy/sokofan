import os

def scrape_xsbs():
    for i in range(1, 16):
        if not os.path.exists("xsbs"):
            os.mkdir("xsbs")
        if not os.path.exists(f"xsbs/{i}"):
            os.mkdir(f"xsbs/{i}")
        xsb = open(f"levelfiles/level{i}.xsb", "r").read().split("\n\n;")

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
                        newfile = open(f"xsbs/{i}/{lname.split()[0]}.xsb", "w")
                        newfile.write("; " + lname + "\n\n" + newlevel)
                        newfile.close()

scrape_xsbs()